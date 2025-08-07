import os
import pathlib
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel
import openai
import cv2
import numpy as np
from config.settings import settings
import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class QCIssue(BaseModel):
    type: str  # "content", "technical", "compliance", "quality"
    severity: str  # "critical", "warning", "info"
    description: str
    timestamp: Optional[float] = None
    frame_number: Optional[int] = None
    suggestion: Optional[str] = None

class QCResult(BaseModel):
    passed: bool
    issues: List[QCIssue]
    metadata: Dict[str, Any]
    checked_at: datetime
    duration_seconds: float
    frame_count: int
    compliance_score: float  # 0-100

class QualityControlService:
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        if self.openai_key:
            openai.api_key = self.openai_key
        
        # Content policy keywords
        self.banned_keywords = [
            "violence", "explicit", "hate", "illegal", "copyright",
            "trademark", "brand", "logo"
        ]
        
        # Technical requirements
        self.tech_requirements = {
            "min_fps": 24,
            "max_fps": 60,
            "min_resolution": (640, 480),
            "max_resolution": (3840, 2160),  # 4K
            "max_duration": 60,  # seconds
            "min_duration": 5,
            "acceptable_codecs": ["h264", "h265", "vp9"],
            "max_bitrate": 50000000,  # 50 Mbps
        }
    
    async def check_video(
        self,
        video_path: pathlib.Path,
        prompt: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> QCResult:
        """Comprehensive video quality control check"""
        
        issues = []
        start_time = datetime.utcnow()
        
        # Technical checks
        tech_issues = await self._check_technical_requirements(video_path)
        issues.extend(tech_issues)
        
        # Content moderation
        if prompt:
            content_issues = await self._check_content_moderation(prompt)
            issues.extend(content_issues)
        
        # Visual quality checks
        visual_issues = await self._check_visual_quality(video_path)
        issues.extend(visual_issues)
        
        # Frame analysis
        frame_issues = await self._analyze_frames(video_path)
        issues.extend(frame_issues)
        
        # Calculate compliance score
        critical_count = sum(1 for i in issues if i.severity == "critical")
        warning_count = sum(1 for i in issues if i.severity == "warning")
        
        compliance_score = max(0, 100 - (critical_count * 20) - (warning_count * 5))
        
        # Get video info
        cap = cv2.VideoCapture(str(video_path))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps if fps > 0 else 0
        cap.release()
        
        result = QCResult(
            passed=critical_count == 0 and compliance_score >= 70,
            issues=issues,
            metadata=metadata or {},
            checked_at=datetime.utcnow(),
            duration_seconds=duration,
            frame_count=frame_count,
            compliance_score=compliance_score
        )
        
        logger.info(f"QC completed: {'PASSED' if result.passed else 'FAILED'} "
                   f"(Score: {compliance_score}, Issues: {len(issues)})")
        
        return result
    
    async def _check_technical_requirements(
        self,
        video_path: pathlib.Path
    ) -> List[QCIssue]:
        """Check technical video requirements"""
        
        issues = []
        
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            # Check FPS
            if fps < self.tech_requirements["min_fps"]:
                issues.append(QCIssue(
                    type="technical",
                    severity="critical",
                    description=f"Frame rate too low: {fps} fps (minimum: {self.tech_requirements['min_fps']})",
                    suggestion="Increase frame rate or use frame interpolation"
                ))
            elif fps > self.tech_requirements["max_fps"]:
                issues.append(QCIssue(
                    type="technical",
                    severity="warning",
                    description=f"Frame rate too high: {fps} fps (maximum: {self.tech_requirements['max_fps']})",
                    suggestion="Consider reducing frame rate for better compatibility"
                ))
            
            # Check resolution
            min_w, min_h = self.tech_requirements["min_resolution"]
            max_w, max_h = self.tech_requirements["max_resolution"]
            
            if width < min_w or height < min_h:
                issues.append(QCIssue(
                    type="technical",
                    severity="critical",
                    description=f"Resolution too low: {width}x{height} (minimum: {min_w}x{min_h})",
                    suggestion="Upscale video or regenerate at higher resolution"
                ))
            elif width > max_w or height > max_h:
                issues.append(QCIssue(
                    type="technical",
                    severity="warning",
                    description=f"Resolution too high: {width}x{height} (maximum: {max_w}x{max_h})",
                    suggestion="Consider downscaling for better compatibility"
                ))
            
            # Check duration
            if duration < self.tech_requirements["min_duration"]:
                issues.append(QCIssue(
                    type="technical",
                    severity="critical",
                    description=f"Video too short: {duration:.1f}s (minimum: {self.tech_requirements['min_duration']}s)",
                    suggestion="Extend video duration or add more content"
                ))
            elif duration > self.tech_requirements["max_duration"]:
                issues.append(QCIssue(
                    type="technical",
                    severity="critical",
                    description=f"Video too long: {duration:.1f}s (maximum: {self.tech_requirements['max_duration']}s)",
                    suggestion="Trim video or split into multiple parts"
                ))
            
            # Check file size
            file_size = video_path.stat().st_size
            if file_size == 0:
                issues.append(QCIssue(
                    type="technical",
                    severity="critical",
                    description="Video file is empty",
                    suggestion="Regenerate video"
                ))
            
            cap.release()
            
        except Exception as e:
            issues.append(QCIssue(
                type="technical",
                severity="critical",
                description=f"Failed to read video file: {str(e)}",
                suggestion="Check video file integrity"
            ))
        
        return issues
    
    async def _check_content_moderation(self, prompt: str) -> List[QCIssue]:
        """Check content against moderation policies"""
        
        issues = []
        
        # Check for banned keywords
        prompt_lower = prompt.lower()
        for keyword in self.banned_keywords:
            if keyword in prompt_lower:
                issues.append(QCIssue(
                    type="content",
                    severity="critical",
                    description=f"Banned keyword detected: '{keyword}'",
                    suggestion="Remove or rephrase content"
                ))
        
        # OpenAI moderation check
        if self.openai_key:
            try:
                response = openai.Moderation.create(
                    model="text-moderation-latest",
                    input=prompt
                )
                
                results = response["results"][0]
                categories = results["categories"]
                scores = results["category_scores"]
                
                # Check each category
                for category, flagged in categories.items():
                    if flagged:
                        score = scores[category]
                        severity = "critical" if score > 0.8 else "warning"
                        
                        issues.append(QCIssue(
                            type="content",
                            severity=severity,
                            description=f"Content flagged for {category} (score: {score:.2f})",
                            suggestion="Review and modify content to comply with policies"
                        ))
                
            except Exception as e:
                logger.error(f"OpenAI moderation error: {e}")
                issues.append(QCIssue(
                    type="content",
                    severity="warning",
                    description="Could not perform content moderation check",
                    suggestion="Manual review recommended"
                ))
        
        return issues
    
    async def _check_visual_quality(
        self,
        video_path: pathlib.Path
    ) -> List[QCIssue]:
        """Check visual quality of video"""
        
        issues = []
        
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            # Sample frames throughout the video
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            sample_interval = max(1, total_frames // 10)  # Sample 10 frames
            
            dark_frames = 0
            blurry_frames = 0
            
            for i in range(0, total_frames, sample_interval):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Check brightness
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                mean_brightness = np.mean(gray)
                
                if mean_brightness < 20:  # Very dark
                    dark_frames += 1
                
                # Check blur using Laplacian variance
                laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                blur_score = laplacian.var()
                
                if blur_score < 100:  # Blurry
                    blurry_frames += 1
            
            cap.release()
            
            # Report issues
            if dark_frames > 2:
                issues.append(QCIssue(
                    type="quality",
                    severity="warning",
                    description=f"Multiple dark frames detected ({dark_frames} frames)",
                    suggestion="Check lighting in generated content"
                ))
            
            if blurry_frames > 2:
                issues.append(QCIssue(
                    type="quality",
                    severity="warning",
                    description=f"Multiple blurry frames detected ({blurry_frames} frames)",
                    suggestion="Improve video quality or use enhancement"
                ))
            
        except Exception as e:
            logger.error(f"Visual quality check error: {e}")
        
        return issues
    
    async def _analyze_frames(
        self,
        video_path: pathlib.Path
    ) -> List[QCIssue]:
        """Analyze individual frames for issues"""
        
        issues = []
        
        try:
            cap = cv2.VideoCapture(str(video_path))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Check for duplicate/frozen frames
            prev_frame = None
            duplicate_count = 0
            max_duplicates = 5  # Threshold for frozen video
            
            # Sample every 10th frame for efficiency
            for i in range(0, total_frames, 10):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                if prev_frame is not None:
                    # Calculate frame difference
                    diff = cv2.absdiff(frame, prev_frame)
                    diff_sum = np.sum(diff)
                    
                    if diff_sum < 1000:  # Very similar frames
                        duplicate_count += 1
                    else:
                        duplicate_count = 0
                    
                    if duplicate_count >= max_duplicates:
                        issues.append(QCIssue(
                            type="quality",
                            severity="critical",
                            description=f"Frozen video detected at frame {i}",
                            frame_number=i,
                            suggestion="Check video generation for stuck frames"
                        ))
                        break
                
                prev_frame = frame.copy()
            
            cap.release()
            
        except Exception as e:
            logger.error(f"Frame analysis error: {e}")
        
        return issues
    
    async def check_prompt_compliance(
        self,
        prompt: str
    ) -> Tuple[bool, List[str]]:
        """Quick compliance check for prompts"""
        
        issues = []
        
        # Length check
        if len(prompt) > 5000:
            issues.append("Prompt too long (max 5000 characters)")
        
        # Banned content check
        prompt_lower = prompt.lower()
        for keyword in self.banned_keywords:
            if keyword in prompt_lower:
                issues.append(f"Contains banned keyword: {keyword}")
        
        # Special character check
        if re.search(r'[<>{}|\[\]]', prompt):
            issues.append("Contains potentially unsafe characters")
        
        return len(issues) == 0, issues
    
    async def generate_qc_report(
        self,
        result: QCResult,
        output_path: Optional[pathlib.Path] = None
    ) -> Dict[str, Any]:
        """Generate detailed QC report"""
        
        report = {
            "summary": {
                "status": "PASSED" if result.passed else "FAILED",
                "compliance_score": result.compliance_score,
                "checked_at": result.checked_at.isoformat(),
                "duration": result.duration_seconds,
                "frame_count": result.frame_count
            },
            "issues": {
                "critical": [],
                "warning": [],
                "info": []
            },
            "statistics": {
                "total_issues": len(result.issues),
                "critical_count": 0,
                "warning_count": 0,
                "info_count": 0
            }
        }
        
        # Categorize issues
        for issue in result.issues:
            issue_dict = issue.dict()
            report["issues"][issue.severity].append(issue_dict)
            report["statistics"][f"{issue.severity}_count"] += 1
        
        # Add metadata
        report["metadata"] = result.metadata
        
        # Save to file if requested
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
        
        return report
    
    def calculate_video_hash(self, video_path: pathlib.Path) -> str:
        """Calculate hash of video file for integrity checking"""
        
        sha256_hash = hashlib.sha256()
        with open(video_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()

# Singleton instance
qc_service = QualityControlService()