from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path
from typing import Any

import numpy as np


class AudioAnalysisError(ValueError):
    pass


def analyze_media_bytes(content: bytes, filename: str) -> dict[str, Any]:
    """Extract an audio waveform and calculate lightweight voice-quality metrics."""
    suffix = Path(filename).suffix or ".bin"
    with tempfile.TemporaryDirectory(prefix="voicetrace_") as tmpdir:
        tmp = Path(tmpdir)
        input_path = tmp / f"upload{suffix}"
        wav_path = tmp / "audio.wav"
        input_path.write_bytes(content)

        if _looks_like_wav(content):
            try:
                sample_rate, signal = _load_wav_mono(input_path)
            except AudioAnalysisError:
                _extract_wav(input_path, wav_path)
                sample_rate, signal = _load_wav_mono(wav_path)
        else:
            _extract_wav(input_path, wav_path)
            sample_rate, signal = _load_wav_mono(wav_path)

    return calculate_voice_metrics(signal, sample_rate)


def calculate_voice_metrics(signal: np.ndarray, sample_rate: int) -> dict[str, Any]:
    if signal.size < int(sample_rate * 0.25):
        raise AudioAnalysisError("Audio is too short for analysis. Use at least 0.25 seconds.")

    signal = np.asarray(signal, dtype=np.float32)
    signal = signal - float(np.mean(signal))
    peak = float(np.max(np.abs(signal))) if signal.size else 0.0
    if peak <= 1e-7:
        raise AudioAnalysisError("Audio signal is silent or unreadable.")

    duration_sec = round(float(signal.size / sample_rate), 2)
    frame_size = max(512, int(sample_rate * 0.04))
    hop_size = max(256, int(sample_rate * 0.02))
    frames = _frame_signal(signal, frame_size, hop_size)
    if frames.shape[0] == 0:
        raise AudioAnalysisError("Audio is too short after framing.")

    window = np.hanning(frame_size).astype(np.float32)
    rms_values = np.sqrt(np.mean(np.square(frames), axis=1))
    voiced_threshold = max(float(np.percentile(rms_values, 35)), 0.01)
    voiced_frames = frames[rms_values >= voiced_threshold]

    if voiced_frames.shape[0] == 0:
        voiced_frames = frames

    hnr_values = [_estimate_hnr_db(frame * window, sample_rate) for frame in voiced_frames]
    hnr_values = [value for value in hnr_values if math.isfinite(value)]
    hnr_db = round(float(np.median(hnr_values)) if hnr_values else 0.0, 1)

    hf_values = [_estimate_hf_ratio(frame * window, sample_rate) for frame in frames]
    hf_ratio = round(float(np.median(hf_values)) if hf_values else 0.0, 2)

    sign_changes = np.signbit(signal[:-1]) != np.signbit(signal[1:])
    zcr = round(float(np.mean(sign_changes)), 3)
    clipping_ratio = round(float(np.mean(np.abs(signal) >= 0.98)), 4)
    silence_ratio = round(float(np.mean(rms_values < 0.01)), 3)
    upload_readiness = _score_readiness(hnr_db, hf_ratio, clipping_ratio, silence_ratio)
    risk_label = _risk_label(hnr_db, hf_ratio, upload_readiness)
    series = _timeline_scores(frames, window, sample_rate)

    return {
        "analysis_mode": "signal_features_v1",
        "duration_sec": duration_sec,
        "sample_rate": sample_rate,
        "hnr_db": hnr_db,
        "hf_ratio": hf_ratio,
        "zero_crossing_rate": zcr,
        "clipping_ratio": clipping_ratio,
        "silence_ratio": silence_ratio,
        "upload_readiness": upload_readiness,
        "risk_label": risk_label,
        "series": series,
        "summary": _summary(risk_label, hnr_db, hf_ratio, clipping_ratio),
        "recommendations": _recommendations(risk_label, hnr_db, hf_ratio, clipping_ratio),
    }


def _looks_like_wav(content: bytes) -> bool:
    return len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WAVE"


def _extract_wav(input_path: Path, wav_path: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise AudioAnalysisError("FFmpeg is required for non-WAV audio/video files.")

    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-f",
        "wav",
        str(wav_path),
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, timeout=45)
    except subprocess.CalledProcessError as exc:
        message = (exc.stderr or exc.stdout or "FFmpeg could not decode the uploaded file.").strip()
        raise AudioAnalysisError(message) from exc
    except subprocess.TimeoutExpired as exc:
        raise AudioAnalysisError("FFmpeg decoding timed out.") from exc


def _load_wav_mono(path: Path) -> tuple[int, np.ndarray]:
    try:
        with wave.open(str(path), "rb") as wav:
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()
            frame_count = wav.getnframes()
            raw = wav.readframes(frame_count)
    except (wave.Error, EOFError) as exc:
        raise AudioAnalysisError("Uploaded WAV file could not be read.") from exc

    if sample_width == 1:
        data = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
    elif sample_width == 2:
        data = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    elif sample_width == 3:
        triples = np.frombuffer(raw, dtype=np.uint8)
        usable = (triples.size // 3) * 3
        values = triples[:usable].reshape(-1, 3).astype(np.int32)
        packed = values[:, 0] | (values[:, 1] << 8) | (values[:, 2] << 16)
        signed = np.where(packed & 0x800000, packed - 0x1000000, packed)
        data = signed.astype(np.float32) / 8388608.0
    elif sample_width == 4:
        data = np.frombuffer(raw, dtype="<i4").astype(np.float32) / 2147483648.0
    else:
        raise AudioAnalysisError(f"Unsupported WAV sample width: {sample_width} bytes.")

    if channels > 1:
        usable = (data.size // channels) * channels
        data = data[:usable].reshape(-1, channels).mean(axis=1)

    if sample_rate <= 0 or data.size == 0:
        raise AudioAnalysisError("Uploaded WAV file has no readable audio samples.")

    return sample_rate, data.astype(np.float32)


def _frame_signal(signal: np.ndarray, frame_size: int, hop_size: int) -> np.ndarray:
    if signal.size < frame_size:
        padded = np.zeros(frame_size, dtype=np.float32)
        padded[: signal.size] = signal
        return padded.reshape(1, frame_size)

    frame_count = 1 + (signal.size - frame_size) // hop_size
    frames = np.empty((frame_count, frame_size), dtype=np.float32)
    for index in range(frame_count):
        start = index * hop_size
        frames[index] = signal[start : start + frame_size]
    return frames


def _estimate_hnr_db(frame: np.ndarray, sample_rate: int) -> float:
    frame = frame - float(np.mean(frame))
    energy = float(np.dot(frame, frame))
    if energy <= 1e-8:
        return 0.0

    autocorr = np.correlate(frame, frame, mode="full")[frame.size - 1 :]
    autocorr = autocorr / max(float(autocorr[0]), 1e-8)
    min_lag = max(1, int(sample_rate / 350))
    max_lag = min(autocorr.size - 1, int(sample_rate / 60))
    if max_lag <= min_lag:
        return 0.0

    harmonicity = float(np.max(autocorr[min_lag:max_lag]))
    harmonicity = min(max(harmonicity, 0.01), 0.99)
    return 10.0 * math.log10(harmonicity / max(1.0 - harmonicity, 1e-6))


def _estimate_hf_ratio(frame: np.ndarray, sample_rate: int) -> float:
    spectrum = np.fft.rfft(frame)
    energy = np.square(np.abs(spectrum))
    total = float(np.sum(energy))
    if total <= 1e-8:
        return 0.0

    freqs = np.fft.rfftfreq(frame.size, d=1.0 / sample_rate)
    threshold = min(4000.0, sample_rate * 0.35)
    high = float(np.sum(energy[freqs >= threshold]))
    return min(max(high / total, 0.0), 1.0)


def _score_readiness(hnr_db: float, hf_ratio: float, clipping_ratio: float, silence_ratio: float) -> int:
    score = 100.0
    if hnr_db < 16:
        score -= min(35.0, (16.0 - hnr_db) * 2.7)
    if hf_ratio > 0.22:
        score -= min(30.0, (hf_ratio - 0.22) * 90.0)
    if clipping_ratio > 0.002:
        score -= min(20.0, clipping_ratio * 1000.0)
    if silence_ratio > 0.35:
        score -= min(12.0, (silence_ratio - 0.35) * 24.0)
    return int(round(min(max(score, 0.0), 100.0)))


def _risk_label(hnr_db: float, hf_ratio: float, readiness: int) -> str:
    if readiness < 62 or hnr_db < 10 or hf_ratio > 0.48:
        return "검토 필요"
    if readiness < 78 or hnr_db < 14 or hf_ratio > 0.34:
        return "주의"
    return "양호"


def _timeline_scores(frames: np.ndarray, window: np.ndarray, sample_rate: int) -> list[float]:
    if frames.shape[0] == 0:
        return [0.5]

    bucket_count = min(8, max(4, frames.shape[0]))
    buckets = np.array_split(frames, bucket_count)
    scores: list[float] = []
    for bucket in buckets:
        hnr_values = [_estimate_hnr_db(frame * window, sample_rate) for frame in bucket]
        hf_values = [_estimate_hf_ratio(frame * window, sample_rate) for frame in bucket]
        hnr = float(np.median(hnr_values)) if hnr_values else 0.0
        hf = float(np.median(hf_values)) if hf_values else 0.0
        readiness = _score_readiness(hnr, hf, 0.0, 0.0)
        scores.append(round(readiness / 100.0, 2))
    return scores


def _summary(risk_label: str, hnr_db: float, hf_ratio: float, clipping_ratio: float) -> str:
    if risk_label == "검토 필요":
        return (
            f"HNR {hnr_db:.1f} dB, HF ratio {hf_ratio:.2f} 기준으로 잡음성 또는 고주파 거칠음이 확인됩니다. "
            "업로드 전에 재생성, 노이즈 제거, EQ 조정을 먼저 비교하는 편이 좋습니다."
        )
    if risk_label == "주의":
        return (
            f"HNR {hnr_db:.1f} dB, HF ratio {hf_ratio:.2f}로 기본 사용은 가능하지만 일부 구간에서 거친 질감이 남을 수 있습니다. "
            "이어폰 환경에서 재청취하고 짧은 후처리를 적용하는 것을 권장합니다."
        )
    extra = " 클리핑도 낮게 측정되었습니다." if clipping_ratio < 0.002 else ""
    return (
        f"HNR {hnr_db:.1f} dB, HF ratio {hf_ratio:.2f}로 업로드 전 점검 기준에 비교적 안정적으로 들어옵니다."
        f"{extra} 최종 음량과 영상 싱크만 확인하면 됩니다."
    )


def _recommendations(risk_label: str, hnr_db: float, hf_ratio: float, clipping_ratio: float) -> list[str]:
    recommendations: list[str] = []
    if hnr_db < 12:
        recommendations.append("동일 프롬프트로 음성을 1회 재생성하고 HNR 변화를 비교")
        recommendations.append("노이즈 리덕션 전후 샘플을 5초 단위로 청취")
    elif hnr_db < 15:
        recommendations.append("호흡음과 배경 잡음이 겹치는 구간을 타임라인에서 재확인")

    if hf_ratio > 0.38:
        recommendations.append("4kHz 이상 고주파 대역 EQ를 완만하게 낮추기")
        recommendations.append("치찰음이 강한 구간에 de-esser 적용")
    elif hf_ratio > 0.28:
        recommendations.append("이어폰 환경에서 금속성 질감이 들리는지 재청취")

    if clipping_ratio > 0.002:
        recommendations.append("피크 음량을 낮추고 최종 음량 정규화 다시 적용")

    if risk_label == "양호":
        recommendations.append("최종 업로드 전 전체 영상 싱크와 음량만 확인")
        recommendations.append("리포트 수치를 제출 기록 또는 제작 로그에 저장")

    return recommendations[:4]
