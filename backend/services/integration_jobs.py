"""
Integration Jobs Tracker
Tracks medical data integration jobs with progress monitoring
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class JobStatus(str, Enum):
    """Integration job status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class IntegrationJob:
    """Represents a data integration job"""
    job_id: str
    status: JobStatus
    directory_path: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    progress: float = 0.0  # 0-100
    current_file: Optional[str] = None
    files_total: int = 0
    files_processed: int = 0
    entities_added: int = 0
    relations_added: int = 0
    errors: List[str] = None
    result: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "directory_path": self.directory_path,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "progress": self.progress,
            "current_file": self.current_file,
            "files_total": self.files_total,
            "files_processed": self.files_processed,
            "entities_added": self.entities_added,
            "relations_added": self.relations_added,
            "errors": self.errors,
            "result": self.result
        }


class IntegrationJobsManager:
    """
    Manages integration jobs with in-memory storage
    For production, consider using Redis or database
    """

    def __init__(self, cleanup_days: int = 7):
        self.jobs: Dict[str, IntegrationJob] = {}
        self.cleanup_days = cleanup_days
        self._cleanup_task = None

    def create_job(self, directory_path: str) -> IntegrationJob:
        """Create a new integration job"""
        job_id = str(uuid.uuid4())
        job = IntegrationJob(
            job_id=job_id,
            status=JobStatus.PENDING,
            directory_path=directory_path,
            started_at=datetime.utcnow()
        )
        self.jobs[job_id] = job
        logger.info(f"Created integration job {job_id} for {directory_path}")
        return job

    def get_job(self, job_id: str) -> Optional[IntegrationJob]:
        """Get job by ID"""
        return self.jobs.get(job_id)

    def update_job(
        self,
        job_id: str,
        status: Optional[JobStatus] = None,
        progress: Optional[float] = None,
        current_file: Optional[str] = None,
        files_total: Optional[int] = None,
        files_processed: Optional[int] = None,
        entities_added: Optional[int] = None,
        relations_added: Optional[int] = None,
        error: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None
    ) -> Optional[IntegrationJob]:
        """Update job status and progress"""
        job = self.jobs.get(job_id)
        if not job:
            return None

        if status:
            job.status = status
            if status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                job.completed_at = datetime.utcnow()

        if progress is not None:
            job.progress = progress

        if current_file:
            job.current_file = current_file

        if files_total is not None:
            job.files_total = files_total

        if files_processed is not None:
            job.files_processed = files_processed

        if entities_added is not None:
            job.entities_added = entities_added

        if relations_added is not None:
            job.relations_added = relations_added

        if error:
            job.errors.append(error)

        if result:
            job.result = result

        logger.debug(f"Updated job {job_id}: status={job.status}, progress={job.progress}%")
        return job

    def list_jobs(self, limit: int = 50, status_filter: Optional[JobStatus] = None) -> List[IntegrationJob]:
        """List all jobs, optionally filtered by status"""
        jobs = list(self.jobs.values())

        if status_filter:
            jobs = [j for j in jobs if j.status == status_filter]

        # Sort by started_at descending (newest first)
        jobs.sort(key=lambda j: j.started_at, reverse=True)

        return jobs[:limit]

    def delete_job(self, job_id: str) -> bool:
        """Delete a job"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            logger.info(f"Deleted job {job_id}")
            return True
        return False

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a running job"""
        job = self.jobs.get(job_id)
        if job and job.status == JobStatus.RUNNING:
            job.status = JobStatus.CANCELLED
            job.completed_at = datetime.utcnow()
            logger.info(f"Cancelled job {job_id}")
            return True
        return False

    async def cleanup_old_jobs(self):
        """Clean up jobs older than cleanup_days"""
        cutoff_date = datetime.utcnow() - timedelta(days=self.cleanup_days)
        deleted_count = 0

        jobs_to_delete = [
            job_id for job_id, job in self.jobs.items()
            if job.completed_at and job.completed_at < cutoff_date
        ]

        for job_id in jobs_to_delete:
            del self.jobs[job_id]
            deleted_count += 1

        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} old integration jobs")

    async def start_cleanup_task(self):
        """Start background task for periodic cleanup"""
        while True:
            try:
                await asyncio.sleep(86400)  # Run once per day
                await self.cleanup_old_jobs()
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics"""
        total_jobs = len(self.jobs)
        status_counts = {status.value: 0 for status in JobStatus}

        for job in self.jobs.values():
            status_counts[job.status.value] += 1

        total_entities = sum(job.entities_added for job in self.jobs.values())
        total_relations = sum(job.relations_added for job in self.jobs.values())

        return {
            "total_jobs": total_jobs,
            "status_counts": status_counts,
            "total_entities_integrated": total_entities,
            "total_relations_integrated": total_relations
        }


# Global instance
jobs_manager = IntegrationJobsManager()
