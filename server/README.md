# VoiceTrace AI API

VoiceTrace AI 모바일 앱과 연결할 FastAPI 분석 서버입니다.

## 역할

- 오디오/비디오 파일 업로드 수신
- FFmpeg 기반 오디오 추출
- WAV 파형 기반 HNR 근사치, HF ratio, 클리핑, 무음 비율 계산
- 제작자용 분석 JSON 반환

현재 구현은 실제 파일 내용을 읽어 신호 특징을 계산합니다. HNR은 Praat 수준의 정밀 측정이 아니라 MVP용 autocorrelation 기반 근사치입니다. HF ratio와 클리핑/무음 비율은 업로드 전 품질 점검 지표로 사용합니다.

## 실행

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

비디오, mp3, m4a 같은 WAV 외 포맷을 분석하려면 `ffmpeg`가 PATH에 잡혀 있어야 합니다.

## API

### `GET /health`

서버 상태와 로컬 실행 조건 확인.

```json
{
  "status": "ok",
  "version": "0.2.0",
  "ffmpeg_available": true,
  "max_upload_mb": 50
}
```

### `POST /analyze`

`multipart/form-data`로 `file` 필드를 업로드하면 분석 JSON을 반환합니다.

```bash
curl -X POST http://127.0.0.1:8000/analyze ^
  -F "file=@sample.wav"
```

주요 응답 필드:

- `analysis_mode`: 현재 분석 엔진 이름
- `duration_sec`, `sample_rate`: 추출된 오디오 기본 정보
- `hnr_db`: harmonic-to-noise ratio 근사치
- `hf_ratio`: 고주파 에너지 비율
- `upload_readiness`: 업로드 준비도 0-100
- `risk_label`: `양호`, `주의`, `검토 필요`
- `series`: 앱 차트에 쓰는 구간별 준비도
- `summary`, `recommendations`: 제작자용 해석과 개선 제안

## 다음 구현 후보

- Parselmouth 또는 Praat 기반 HNR 정밀 계산
- librosa 기반 구간별 spectral centroid, rolloff, noise floor 추가
- 파일 보관 기간과 삭제 정책 적용
- Cloud Run/Render/Fly.io 등 배포 환경 구성

## 검증

```bash
python -m py_compile app/main.py app/audio_analysis.py app/__init__.py
python -m unittest discover -s tests
```
