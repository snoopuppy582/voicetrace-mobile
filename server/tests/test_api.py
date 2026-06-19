from __future__ import annotations

import math
import struct
import unittest
import wave
from io import BytesIO

from fastapi.testclient import TestClient

from app.main import MAX_UPLOAD_MB, app


def make_wav() -> bytes:
    buffer = BytesIO()
    sample_rate = 16000
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = bytearray()
        for index in range(sample_rate):
            value = int(0.35 * 32767 * math.sin(2 * math.pi * 180 * index / sample_rate))
            frames.extend(struct.pack("<h", value))
        wav.writeframes(bytes(frames))
    return buffer.getvalue()


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_reports_runtime_requirements(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["max_upload_mb"], MAX_UPLOAD_MB)
        self.assertIn("ffmpeg_available", payload)

    def test_analyze_accepts_wav_upload(self) -> None:
        response = self.client.post(
            "/analyze",
            files={"file": ("sample.wav", make_wav(), "audio/wav")},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["filename"], "sample.wav")
        self.assertEqual(payload["analysis_mode"], "signal_features_v1")
        self.assertIn(payload["risk_label"], {"양호", "주의", "검토 필요"})
        self.assertGreaterEqual(payload["upload_readiness"], 0)
        self.assertLessEqual(payload["upload_readiness"], 100)

    def test_analyze_rejects_empty_upload(self) -> None:
        response = self.client.post(
            "/analyze",
            files={"file": ("empty.wav", b"", "audio/wav")},
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
