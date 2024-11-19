"""Audio processing utilities"""

from typing import Any

import numpy as np
from pydub import AudioSegment


def process_audio_segments(segments: list[np.ndarray], crossfade: int = 100) -> np.ndarray:
    """Process audio segments with crossfade"""
    if not segments:
        return np.array([])

    if len(segments) == 1:
        return segments[0]

    result = segments[0]
    for segment in segments[1:]:
        if crossfade > 0:
            xf_samples = int(crossfade * 44.1)
            result = np.concatenate(
                (
                    result[:-xf_samples],
                    result[-xf_samples:] * np.linspace(1, 0, xf_samples)
                    + segment[:xf_samples] * np.linspace(0, 1, xf_samples),
                    segment[xf_samples:],
                ),
            )
        else:
            result = np.concatenate((result, segment))

    return result


def apply_audio_effects(
    audio: np.ndarray | AudioSegment,
    effects: dict[str, Any],
) -> np.ndarray | AudioSegment:
    """Apply effects to audio data"""
    result = audio

    if isinstance(result, np.ndarray):
        if effects.get("normalize", False):
            result = result / np.max(np.abs(result))

        if "fade_in" in effects or "fade_out" in effects:
            fade_in = effects.get("fade_in", 0)
            fade_out = effects.get("fade_out", 0)
            samples = len(result)

            if fade_in:
                fade_in_samples = int(fade_in * 44.1)
                result[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)

            if fade_out:
                fade_out_samples = int(fade_out * 44.1)
                result[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)

        if "speed" in effects:
            speed = float(effects["speed"])
            if speed != 1.0:
                samples = len(result)
                result = np.interp(
                    np.linspace(0, samples, int(samples / speed)),
                    np.arange(samples),
                    result,
                )

        if effects.get("reverse", False):
            result = np.flip(result)

    elif isinstance(result, AudioSegment):
        if effects.get("normalize", False):
            peak_amplitude = result.max
            if peak_amplitude > 0:
                result = result.apply_gain(-peak_amplitude)

        if "fade_in" in effects:
            result = result.fade_in(int(effects["fade_in"] * 1000))

        if "fade_out" in effects:
            result = result.fade_out(int(effects["fade_out"] * 1000))

        if "speed" in effects:
            speed = float(effects["speed"])
            if speed != 1.0:
                result = result._spawn(
                    result.raw_data,
                    overrides={"frame_rate": int(result.frame_rate * speed)},
                )

        if effects.get("reverse", False):
            result = result.reverse()

    return result 