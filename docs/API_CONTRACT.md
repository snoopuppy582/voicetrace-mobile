# VoiceTrace AI API Contract

## `POST /analyze`

Expo 앱이 오디오/비디오 파일을 `multipart/form-data`로 업로드하면 FastAPI 서버가 제작자용 음성 품질 리포트를 반환한다.

## `GET /health`

서버 상태와 시연 준비 상태를 확인한다.

```json
{
  "status": "ok",
  "version": "0.2.0",
  "ffmpeg_available": true,
  "max_upload_mb": 50
}
```

### Request

- Method: `POST`
- Path: `/analyze`
- Content-Type: `multipart/form-data`
- Field: `file`
- MVP limit: 50MB

```bash
curl -X POST http://127.0.0.1:8000/analyze ^
  -F "file=@sample.wav"
```

### Response

```json
{
  "filename": "sample.wav",
  "content_type": "audio/wav",
  "size_bytes": 88244,
  "analysis_mode": "signal_features_v1",
  "duration_sec": 2.0,
  "sample_rate": 16000,
  "hnr_db": 13.5,
  "hf_ratio": 0.18,
  "zero_crossing_rate": 0.08,
  "clipping_ratio": 0.0,
  "silence_ratio": 0.0,
  "upload_readiness": 85,
  "risk_label": "양호",
  "series": [0.84, 0.83, 0.85, 0.86],
  "summary": "HNR/HF ratio 기준의 제작자용 해석",
  "recommendations": ["최종 업로드 전 전체 영상 싱크와 음량만 확인"],
  "caveat": "HNR/HF ratio and spectral features are quality signals, not proof of AI generation."
}
```

### Error Cases

- `400`: 빈 파일
- `413`: 50MB 초과
- `422`: 오디오 디코딩 실패, 너무 짧은 파일, 무음 파일, FFmpeg 미설치 상태에서 비-WAV 파일 업로드

## App Mapping

- `hnr_db` -> HNR 카드
- `hf_ratio` -> HF ratio 카드
- `upload_readiness` -> Upload readiness 카드
- `risk_label`, `summary` -> 리포트 박스
- `series` -> 구간별 막대 차트
- `recommendations` -> 개선 제안 목록

## Product Caveat

이 API는 AI 생성 여부를 판정하는 도구가 아니라, 제작자가 업로드 전 음성 품질을 점검하기 위한 리포트 API다. HNR, HF ratio, 스펙트럼 특징은 품질 신호일 뿐 AI 생성의 법적 증거로 사용하면 안 된다.
