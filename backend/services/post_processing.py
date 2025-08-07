import os
import pathlib
import subprocess
import shutil
import tempfile
from typing import Optional, Dict, Any, List, Tuple
from pydantic import BaseModel
from config.settings import settings
import logging
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import ffmpeg

logger = logging.getLogger(__name__)

class PostProcessConfig(BaseModel):
    interpolation_factor: int = 2
    upscale_factor: int = 2
    target_fps: int = 60
    output_format: str = "mp4"
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    crf: int = 23  # Quality (0-51, lower is better)
    preset: str = "medium"  # Encoding speed/quality tradeoff
    audio_bitrate: str = "192k"
    normalize_audio: bool = True
    target_loudness: float = -14.0  # LUFS
    add_watermark: bool = False
    watermark_text: Optional[str] = None

class PostProcessingService:
    def __init__(self):
        self.rife_bin = settings.RIFE_BIN
        self.esrgan_bin = settings.ESRGAN_BIN
        self.temp_dir = pathlib.Path(settings.TEMP_DIR)
        self.temp_dir.mkdir(exist_ok=True)
    
    async def process_video(
        self,
        input_path: pathlib.Path,
        config: PostProcessConfig
    ) -> pathlib.Path:
        """Full post-processing pipeline for video"""
        
        # Create temporary directory for this job
        job_dir = self.temp_dir / f"job_{int(time.time())}"
        job_dir.mkdir(exist_ok=True)
        
        try:
            current_path = input_path
            
            # Step 1: Frame interpolation
            if config.interpolation_factor > 1:
                logger.info(f"Interpolating frames by {config.interpolation_factor}x")
                current_path = await self.interpolate_frames(
                    current_path,
                    config.interpolation_factor,
                    job_dir
                )
            
            # Step 2: Upscaling
            if config.upscale_factor > 1:
                logger.info(f"Upscaling video by {config.upscale_factor}x")
                current_path = await self.upscale_video(
                    current_path,
                    config.upscale_factor,
                    job_dir
                )
            
            # Step 3: Final encoding with audio
            logger.info("Final encoding and audio processing")
            output_path = await self.encode_final(
                current_path,
                config,
                job_dir
            )
            
            return output_path
            
        finally:
            # Cleanup temporary files
            if job_dir.exists():
                shutil.rmtree(job_dir)
    
    async def interpolate_frames(
        self,
        input_path: pathlib.Path,
        factor: int,
        work_dir: pathlib.Path
    ) -> pathlib.Path:
        """Interpolate frames using RIFE"""
        
        output_path = work_dir / f"interpolated_{factor}x.mp4"
        
        # Check if RIFE binary exists
        if not os.path.exists(self.rife_bin):
            logger.warning("RIFE binary not found, using ffmpeg interpolation")
            return await self._ffmpeg_interpolate(input_path, factor, output_path)
        
        cmd = [
            self.rife_bin,
            "-i", str(input_path),
            "-o", str(output_path),
            "-f", str(factor),
            "-m", "rife4.6",
            "-n", "4",  # Number of threads
            "-x"  # Export as video
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(f"RIFE interpolation completed: {result.stdout}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"RIFE interpolation failed: {e.stderr}")
            # Fallback to ffmpeg
            return await self._ffmpeg_interpolate(input_path, factor, output_path)
    
    async def _ffmpeg_interpolate(
        self,
        input_path: pathlib.Path,
        factor: int,
        output_path: pathlib.Path
    ) -> pathlib.Path:
        """Fallback frame interpolation using ffmpeg"""
        
        # Get input video info
        probe = ffmpeg.probe(str(input_path))
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        fps = eval(video_info['r_frame_rate'])
        target_fps = fps * factor
        
        # Use minterpolate filter
        stream = ffmpeg.input(str(input_path))
        stream = ffmpeg.filter(stream, 'minterpolate', fps=target_fps)
        stream = ffmpeg.output(stream, str(output_path), vcodec='libx264', crf=18)
        
        ffmpeg.run(stream, overwrite_output=True)
        return output_path
    
    async def upscale_video(
        self,
        input_path: pathlib.Path,
        scale: int,
        work_dir: pathlib.Path
    ) -> pathlib.Path:
        """Upscale video using Real-ESRGAN"""
        
        output_path = work_dir / f"upscaled_{scale}x.mp4"
        
        # Check if ESRGAN binary exists
        if not os.path.exists(self.esrgan_bin):
            logger.warning("Real-ESRGAN binary not found, using ffmpeg scaling")
            return await self._ffmpeg_upscale(input_path, scale, output_path)
        
        cmd = [
            self.esrgan_bin,
            "-i", str(input_path),
            "-o", str(output_path),
            "-s", str(scale),
            "-n", "realesrgan-x4plus",
            "-f", "mp4"
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(f"Real-ESRGAN upscaling completed: {result.stdout}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Real-ESRGAN upscaling failed: {e.stderr}")
            # Fallback to ffmpeg
            return await self._ffmpeg_upscale(input_path, scale, output_path)
    
    async def _ffmpeg_upscale(
        self,
        input_path: pathlib.Path,
        scale: int,
        output_path: pathlib.Path
    ) -> pathlib.Path:
        """Fallback video upscaling using ffmpeg"""
        
        # Get input dimensions
        probe = ffmpeg.probe(str(input_path))
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        width = int(video_info['width'])
        height = int(video_info['height'])
        
        # Calculate new dimensions
        new_width = width * scale
        new_height = height * scale
        
        # Use lanczos scaling
        stream = ffmpeg.input(str(input_path))
        stream = ffmpeg.filter(stream, 'scale', width=new_width, height=new_height, flags='lanczos')
        stream = ffmpeg.output(stream, str(output_path), vcodec='libx264', crf=18)
        
        ffmpeg.run(stream, overwrite_output=True)
        return output_path
    
    async def encode_final(
        self,
        video_path: pathlib.Path,
        config: PostProcessConfig,
        work_dir: pathlib.Path
    ) -> pathlib.Path:
        """Final encoding with audio processing"""
        
        output_path = work_dir / f"final.{config.output_format}"
        
        # Build ffmpeg command
        stream = ffmpeg.input(str(video_path))
        
        # Video encoding options
        video_opts = {
            'vcodec': config.video_codec,
            'crf': config.crf,
            'preset': config.preset,
            'r': config.target_fps
        }
        
        # Audio options
        audio_opts = {
            'acodec': config.audio_codec,
            'b:a': config.audio_bitrate
        }
        
        # Apply filters if needed
        if config.normalize_audio:
            # Audio normalization filter
            audio_opts['af'] = f'loudnorm=I={config.target_loudness}:TP=-1.5:LRA=11'
        
        # Add watermark if requested
        if config.add_watermark and config.watermark_text:
            stream = ffmpeg.drawtext(
                stream,
                text=config.watermark_text,
                x='10',
                y='10',
                fontsize=24,
                fontcolor='white@0.5'
            )
        
        # Output
        stream = ffmpeg.output(
            stream,
            str(output_path),
            **video_opts,
            **audio_opts
        )
        
        ffmpeg.run(stream, overwrite_output=True)
        return output_path
    
    async def merge_audio_video(
        self,
        video_path: pathlib.Path,
        audio_path: pathlib.Path,
        output_path: pathlib.Path,
        normalize: bool = True
    ) -> pathlib.Path:
        """Merge audio and video tracks"""
        
        video = ffmpeg.input(str(video_path))
        audio = ffmpeg.input(str(audio_path))
        
        if normalize:
            # Normalize audio to broadcast standards
            audio = ffmpeg.filter(audio, 'loudnorm', I=-14, TP=-1.5, LRA=11)
        
        stream = ffmpeg.output(
            video,
            audio,
            str(output_path),
            vcodec='copy',
            acodec='aac',
            strict='experimental'
        )
        
        ffmpeg.run(stream, overwrite_output=True)
        return output_path
    
    async def extract_frames(
        self,
        video_path: pathlib.Path,
        output_dir: pathlib.Path,
        fps: Optional[int] = None
    ) -> List[pathlib.Path]:
        """Extract frames from video"""
        
        output_dir.mkdir(exist_ok=True)
        pattern = str(output_dir / "frame_%05d.png")
        
        cmd = ['ffmpeg', '-i', str(video_path)]
        
        if fps:
            cmd.extend(['-r', str(fps)])
        
        cmd.extend([
            '-q:v', '2',  # High quality
            pattern
        ])
        
        subprocess.run(cmd, check=True)
        
        # Return sorted list of frame paths
        frames = sorted(output_dir.glob("frame_*.png"))
        return frames
    
    async def create_video_from_frames(
        self,
        frames_dir: pathlib.Path,
        output_path: pathlib.Path,
        fps: int = 24,
        codec: str = "libx264"
    ) -> pathlib.Path:
        """Create video from frame sequence"""
        
        pattern = str(frames_dir / "frame_%05d.png")
        
        stream = ffmpeg.input(pattern, framerate=fps)
        stream = ffmpeg.output(
            stream,
            str(output_path),
            vcodec=codec,
            crf=18,
            pix_fmt='yuv420p'
        )
        
        ffmpeg.run(stream, overwrite_output=True)
        return output_path
    
    async def add_transitions(
        self,
        clips: List[pathlib.Path],
        output_path: pathlib.Path,
        transition_duration: float = 0.5
    ) -> pathlib.Path:
        """Add transitions between video clips"""
        
        # Load clips with moviepy
        video_clips = [VideoFileClip(str(clip)) for clip in clips]
        
        # Add crossfade transitions
        final_clips = []
        for i, clip in enumerate(video_clips):
            if i > 0:
                # Add crossfade from previous clip
                clip = clip.crossfadein(transition_duration)
            if i < len(video_clips) - 1:
                # Add crossfade to next clip
                clip = clip.crossfadeout(transition_duration)
            final_clips.append(clip)
        
        # Concatenate with transitions
        final_video = concatenate_videoclips(final_clips, method="compose")
        
        # Write output
        final_video.write_videofile(
            str(output_path),
            codec='libx264',
            audio_codec='aac'
        )
        
        # Cleanup
        for clip in video_clips:
            clip.close()
        
        return output_path
    
    def get_video_info(self, video_path: pathlib.Path) -> Dict[str, Any]:
        """Get detailed video information"""
        
        probe = ffmpeg.probe(str(video_path))
        
        video_stream = next(
            (s for s in probe['streams'] if s['codec_type'] == 'video'),
            None
        )
        audio_stream = next(
            (s for s in probe['streams'] if s['codec_type'] == 'audio'),
            None
        )
        
        info = {
            "duration": float(probe['format']['duration']),
            "size": int(probe['format']['size']),
            "bit_rate": int(probe['format']['bit_rate']),
        }
        
        if video_stream:
            info["video"] = {
                "codec": video_stream['codec_name'],
                "width": video_stream['width'],
                "height": video_stream['height'],
                "fps": eval(video_stream['r_frame_rate']),
                "bit_rate": int(video_stream.get('bit_rate', 0))
            }
        
        if audio_stream:
            info["audio"] = {
                "codec": audio_stream['codec_name'],
                "channels": audio_stream['channels'],
                "sample_rate": int(audio_stream['sample_rate']),
                "bit_rate": int(audio_stream.get('bit_rate', 0))
            }
        
        return info

# Singleton instance
post_processing_service = PostProcessingService()