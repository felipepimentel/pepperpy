"""Audio file handler implementation"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment

from ..base import FileHandler
from ..exceptions import FileError
from ..types import AudioInfo


class AudioHandler(FileHandler):
    """Handler for audio files"""

    SUPPORTED_FORMATS = {
        ".wav": "WAV",
        ".mp3": "MP3",
        ".ogg": "OGG",
        ".flac": "FLAC",
        ".m4a": "M4A",
        ".aac": "AAC",
    }

    async def read(self, path: Path, return_type: str = "array") -> Union[np.ndarray, AudioSegment]:
        """Read audio file"""
        try:
            if return_type == "array":
                data, sample_rate = sf.read(path)
                return data
            elif return_type == "segment":
                return AudioSegment.from_file(str(path))
            else:
                raise FileError(f"Invalid return type: {return_type}")
        except Exception as e:
            raise FileError(f"Failed to read audio: {str(e)}", cause=e)

    async def write(
        self,
        path: Path,
        content: Union[np.ndarray, AudioSegment],
        sample_rate: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """Write audio file"""
        try:
            if isinstance(content, np.ndarray):
                if not sample_rate:
                    raise FileError("Sample rate required for numpy array")
                sf.write(path, content, sample_rate, **kwargs)
            elif isinstance(content, AudioSegment):
                content.export(str(path), format=path.suffix[1:], **kwargs)
            else:
                raise FileError(f"Unsupported content type: {type(content)}")
        except Exception as e:
            raise FileError(f"Failed to write audio: {str(e)}", cause=e)

    async def get_info(self, path: Path) -> AudioInfo:
        """Get audio file information"""
        try:
            y, sr = librosa.load(path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)

            return AudioInfo(
                duration=duration,
                sample_rate=sr,
                channels=y.shape[1] if len(y.shape) > 1 else 1,
                format=path.suffix[1:].upper(),
                bit_depth=y.dtype.itemsize * 8,
                num_samples=len(y),
            )
        except Exception as e:
            raise FileError(f"Failed to get audio info: {str(e)}", cause=e)

    async def convert(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Convert audio format"""
        try:
            audio = await self.read(input_path, return_type="segment")
            await self.write(output_path, audio, **kwargs)
        except Exception as e:
            raise FileError(f"Failed to convert audio: {str(e)}", cause=e)

    async def split(
        self, path: Path, output_dir: Path, segment_length: float, overlap: float = 0.0
    ) -> List[Path]:
        """Split audio into segments"""
        try:
            y, sr = librosa.load(path, sr=None)
            segment_samples = int(segment_length * sr)
            overlap_samples = int(overlap * sr)
            hop_length = segment_samples - overlap_samples

            segments = []
            for i in range(0, len(y), hop_length):
                segment = y[i : i + segment_samples]
                if len(segment) < segment_samples:
                    break

                output_path = output_dir / f"segment_{i//hop_length}.wav"
                sf.write(output_path, segment, sr)
                segments.append(output_path)

            return segments

        except Exception as e:
            raise FileError(f"Failed to split audio: {str(e)}", cause=e)

    async def merge(self, paths: List[Path], output_path: Path, crossfade: float = 0.0) -> None:
        """Merge multiple audio files"""
        try:
            segments = [await self.read(path, return_type="segment") for path in paths]

            result = segments[0]
            for segment in segments[1:]:
                result = result.append(segment, crossfade=int(crossfade * 1000))

            await self.write(output_path, result)

        except Exception as e:
            raise FileError(f"Failed to merge audio: {str(e)}", cause=e)

    async def extract_features(self, path: Path) -> Dict[str, np.ndarray]:
        """Extract audio features"""
        try:
            y, sr = librosa.load(path, sr=None)

            return {
                "mfcc": librosa.feature.mfcc(y=y, sr=sr),
                "spectral_centroid": librosa.feature.spectral_centroid(y=y, sr=sr),
                "chroma": librosa.feature.chroma_stft(y=y, sr=sr),
                "tempo": librosa.beat.tempo(y=y, sr=sr),
                "onset_env": librosa.onset.onset_strength(y=y, sr=sr),
                "pitch": librosa.yin(y=y, sr=sr, fmin=20, fmax=2000),
            }

        except Exception as e:
            raise FileError(f"Failed to extract features: {str(e)}", cause=e)

    async def apply_effects(self, path: Path, output_path: Path, effects: Dict[str, Any]) -> None:
        """Apply audio effects"""
        try:
            audio = await self.read(path, return_type="segment")

            for effect, params in effects.items():
                if effect == "normalize":
                    audio = audio.normalize(**params)
                elif effect == "fade":
                    audio = audio.fade(**params)
                elif effect == "speed":
                    audio = audio.speedup(**params)
                elif effect == "reverse":
                    audio = audio.reverse()
                elif effect == "volume":
                    audio = audio + params  # dB adjustment
                else:
                    raise FileError(f"Unknown effect: {effect}")

            await self.write(output_path, audio)

        except Exception as e:
            raise FileError(f"Failed to apply effects: {str(e)}", cause=e)

    async def validate(self, path: Path) -> bool:
        """Validate audio file"""
        try:
            if path.suffix.lower() not in self.SUPPORTED_FORMATS:
                return False

            # Try to read file
            await self.read(path)
            return True

        except Exception:
            return False
