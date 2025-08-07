import boto3
import os
import pathlib
import mimetypes
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import urllib.parse
from config.settings import settings
import logging
import hashlib
import aiofiles
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        # Initialize R2 client (S3 compatible)
        self.r2_client = boto3.client(
            "s3",
            endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name="auto"
        )
        
        # Initialize S3 client as fallback
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        self.r2_bucket = settings.R2_BUCKET
        self.s3_bucket = settings.S3_BUCKET
        
        # Default to R2
        self.primary_client = self.r2_client
        self.primary_bucket = self.r2_bucket
    
    async def upload_file(
        self,
        file_path: pathlib.Path,
        key: str,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        public: bool = False
    ) -> Dict[str, Any]:
        """Upload file to CDN"""
        
        if not content_type:
            content_type, _ = mimetypes.guess_type(str(file_path))
            content_type = content_type or "application/octet-stream"
        
        # Prepare metadata
        file_metadata = metadata or {}
        file_metadata.update({
            "uploaded_at": datetime.utcnow().isoformat(),
            "original_filename": file_path.name,
            "file_size": str(file_path.stat().st_size)
        })
        
        # Calculate file hash
        file_hash = await self._calculate_file_hash(file_path)
        file_metadata["sha256"] = file_hash
        
        # Upload parameters
        extra_args = {
            "ContentType": content_type,
            "Metadata": file_metadata
        }
        
        if public:
            extra_args["ACL"] = "public-read"
        
        try:
            # Upload to primary storage
            with open(file_path, "rb") as f:
                self.primary_client.upload_fileobj(
                    f,
                    self.primary_bucket,
                    key,
                    ExtraArgs=extra_args
                )
            
            # Get URL
            if public:
                url = f"https://{self.primary_bucket}.r2.dev/{key}"
            else:
                url = await self.generate_presigned_url(key)
            
            logger.info(f"File uploaded successfully: {key}")
            
            return {
                "key": key,
                "url": url,
                "size": file_path.stat().st_size,
                "content_type": content_type,
                "hash": file_hash,
                "uploaded_at": datetime.utcnow().isoformat()
            }
            
        except ClientError as e:
            logger.error(f"Upload failed: {e}")
            raise
    
    async def upload_bytes(
        self,
        data: bytes,
        key: str,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Upload bytes data to CDN"""
        
        file_metadata = metadata or {}
        file_metadata.update({
            "uploaded_at": datetime.utcnow().isoformat(),
            "file_size": str(len(data))
        })
        
        # Calculate hash
        file_hash = hashlib.sha256(data).hexdigest()
        file_metadata["sha256"] = file_hash
        
        try:
            self.primary_client.put_object(
                Bucket=self.primary_bucket,
                Key=key,
                Body=data,
                ContentType=content_type,
                Metadata=file_metadata
            )
            
            url = await self.generate_presigned_url(key)
            
            return {
                "key": key,
                "url": url,
                "size": len(data),
                "content_type": content_type,
                "hash": file_hash,
                "uploaded_at": datetime.utcnow().isoformat()
            }
            
        except ClientError as e:
            logger.error(f"Upload bytes failed: {e}")
            raise
    
    async def generate_presigned_url(
        self,
        key: str,
        expiry_seconds: int = 3600,
        download_filename: Optional[str] = None
    ) -> str:
        """Generate presigned URL for private objects"""
        
        params = {"Bucket": self.primary_bucket, "Key": key}
        
        if download_filename:
            params["ResponseContentDisposition"] = f'attachment; filename="{download_filename}"'
        
        try:
            url = self.primary_client.generate_presigned_url(
                "get_object",
                Params=params,
                ExpiresIn=expiry_seconds
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise
    
    async def download_file(
        self,
        key: str,
        destination: pathlib.Path
    ) -> pathlib.Path:
        """Download file from CDN"""
        
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            self.primary_client.download_file(
                self.primary_bucket,
                key,
                str(destination)
            )
            
            logger.info(f"File downloaded: {key} -> {destination}")
            return destination
            
        except ClientError as e:
            logger.error(f"Download failed: {e}")
            raise
    
    async def delete_file(self, key: str) -> bool:
        """Delete file from CDN"""
        
        try:
            self.primary_client.delete_object(
                Bucket=self.primary_bucket,
                Key=key
            )
            logger.info(f"File deleted: {key}")
            return True
            
        except ClientError as e:
            logger.error(f"Delete failed: {e}")
            return False
    
    async def list_files(
        self,
        prefix: str = "",
        max_keys: int = 1000
    ) -> List[Dict[str, Any]]:
        """List files in CDN"""
        
        try:
            response = self.primary_client.list_objects_v2(
                Bucket=self.primary_bucket,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            files = []
            for obj in response.get("Contents", []):
                files.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat(),
                    "etag": obj["ETag"].strip('"')
                })
            
            return files
            
        except ClientError as e:
            logger.error(f"List files failed: {e}")
            raise
    
    async def get_file_info(self, key: str) -> Dict[str, Any]:
        """Get file metadata"""
        
        try:
            response = self.primary_client.head_object(
                Bucket=self.primary_bucket,
                Key=key
            )
            
            return {
                "key": key,
                "size": response["ContentLength"],
                "content_type": response.get("ContentType"),
                "last_modified": response["LastModified"].isoformat(),
                "etag": response["ETag"].strip('"'),
                "metadata": response.get("Metadata", {})
            }
            
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return None
            logger.error(f"Get file info failed: {e}")
            raise
    
    async def copy_file(
        self,
        source_key: str,
        destination_key: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Copy file within CDN"""
        
        copy_source = {"Bucket": self.primary_bucket, "Key": source_key}
        
        try:
            # Get source metadata
            source_info = await self.get_file_info(source_key)
            if not source_info:
                raise ValueError(f"Source file not found: {source_key}")
            
            # Prepare metadata
            new_metadata = source_info.get("metadata", {}).copy()
            if metadata:
                new_metadata.update(metadata)
            new_metadata["copied_at"] = datetime.utcnow().isoformat()
            new_metadata["source_key"] = source_key
            
            self.primary_client.copy_object(
                CopySource=copy_source,
                Bucket=self.primary_bucket,
                Key=destination_key,
                Metadata=new_metadata,
                MetadataDirective="REPLACE"
            )
            
            return await self.get_file_info(destination_key)
            
        except ClientError as e:
            logger.error(f"Copy file failed: {e}")
            raise
    
    async def create_multipart_upload(
        self,
        key: str,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """Initialize multipart upload for large files"""
        
        try:
            response = self.primary_client.create_multipart_upload(
                Bucket=self.primary_bucket,
                Key=key,
                ContentType=content_type,
                Metadata=metadata or {}
            )
            
            return response["UploadId"]
            
        except ClientError as e:
            logger.error(f"Create multipart upload failed: {e}")
            raise
    
    async def upload_video(
        self,
        video_path: pathlib.Path,
        folder: str = "videos"
    ) -> Dict[str, Any]:
        """Upload video file with optimized settings"""
        
        # Generate unique key
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_hash = await self._calculate_file_hash(video_path)
        key = f"{folder}/{timestamp}_{file_hash[:8]}_{video_path.name}"
        
        # Video-specific metadata
        metadata = {
            "content_type": "video",
            "original_name": video_path.name,
            "upload_timestamp": timestamp
        }
        
        # Upload with video content type
        return await self.upload_file(
            video_path,
            key,
            content_type="video/mp4",
            metadata=metadata
        )
    
    async def upload_audio(
        self,
        audio_data: bytes,
        filename: str,
        folder: str = "audio"
    ) -> Dict[str, Any]:
        """Upload audio data"""
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        key = f"{folder}/{timestamp}_{filename}"
        
        return await self.upload_bytes(
            audio_data,
            key,
            content_type="audio/mpeg",
            metadata={"content_type": "audio"}
        )
    
    async def get_storage_stats(self, prefix: str = "") -> Dict[str, Any]:
        """Get storage statistics"""
        
        try:
            total_size = 0
            file_count = 0
            file_types = {}
            
            # Use paginator for large buckets
            paginator = self.primary_client.get_paginator("list_objects_v2")
            
            for page in paginator.paginate(
                Bucket=self.primary_bucket,
                Prefix=prefix
            ):
                for obj in page.get("Contents", []):
                    total_size += obj["Size"]
                    file_count += 1
                    
                    # Track file types
                    ext = pathlib.Path(obj["Key"]).suffix.lower()
                    file_types[ext] = file_types.get(ext, 0) + 1
            
            return {
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "total_size_gb": round(total_size / (1024 * 1024 * 1024), 2),
                "file_count": file_count,
                "file_types": file_types,
                "prefix": prefix
            }
            
        except ClientError as e:
            logger.error(f"Get storage stats failed: {e}")
            raise
    
    async def _calculate_file_hash(self, file_path: pathlib.Path) -> str:
        """Calculate SHA256 hash of file"""
        
        sha256_hash = hashlib.sha256()
        
        async with aiofiles.open(file_path, "rb") as f:
            while chunk := await f.read(8192):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    def get_public_url(self, key: str) -> str:
        """Get public URL for R2 object"""
        return f"https://{self.r2_bucket}.r2.dev/{key}"
    
    def get_cdn_url(self, key: str, custom_domain: Optional[str] = None) -> str:
        """Get CDN URL with optional custom domain"""
        if custom_domain:
            return f"https://{custom_domain}/{key}"
        return self.get_public_url(key)

# Singleton instance
storage_service = StorageService()