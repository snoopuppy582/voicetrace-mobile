from __future__ import annotations

import math
import struct
import unittest
import wave
from io import BytesIO

from app.audio_analysis import AudioAnalysisError, analyze_media_bytes


def make_wav(
    *,
    seconds: float = 1.0,
    sample_rate: int = 16000,
    frequency: float = 180.0,
    amplitude: float = 0.35,
    sample_width: int = 2,
) -> bytes:
    buffer = BytesIO()
    frame_count = int(sample_rate * seconds)

    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(sample_width)
        wav.setframerate(sample_rate)
        frames = bytearray()
        for index in range(frame_count):
            sample = amplitude * math.sin(2 * math.pi * frequency * index / sample_rate)
            if sample_width == 2:
                frames.extend(struct.pack("<h", int(sample * 32767)))
            elif sample_width == 3:
                value = int(sample * 8388607)
                if value < 0:
                    value += 1 << 24
                frames.extend(bytes((value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF)))
            else:
                raise ValueError("unsupported sample_width")
        wav.writeframes(bytes(frames))

    return buffer.getvalue()


class AudioAnalysisTests(unittest.TestCase):
    def test_analyzes_16_bit_wav(self) -> None:
        result = analyze_media_bytes(make_wav(), "tone.wav")

        self.assertEqual(result["analysis_mode"], "signal_features_v1")
        self.assertEqual(result["sample_rate"], 16000)
        self.assertGreaterEqual(result["duration_sec"], 1.0)
        self.assertGreaterEqual(result["upload_readiness"], 0)
        self.assertLessEqual(result["upload_readiness"], 100)
        self.assertGreaterEqual(len(result["series"]), 4)

    def test_analyzes_24_bit_wav(self) -> None:
        result = analyze_media_bytes(make_wav(sample_width=3), "tone_24bit.wav")

        self.assertEqual(result["sample_rate"], 16000)
        self.assertGreaterEqual(result["duration_sec"], 1.0)
        self.assertIn(result["risk_label"], {"양호", "주의", "검토 필요"})

    def test_rejects_too_short_audio(self) -> None:
        with self.assertRaises(AudioAnalysisError):
            analyze_media_bytes(make_wav(seconds=0.1), "short.wav")

    def test_rejects_silent_audio(self) -> None:
        with self.assertRaises(AudioAnalysisError):
            analyze_media_bytes(make_wav(amplitude=0.0), "silent.wav")


if __name__ == "__main__":
    unittest.main()
