# VoiceTrace AI Prototype

생성형 AI 영상 또는 음성 파일을 업로드 전 점검하는 제작자용 품질 리포트 프로토타입입니다. React Native/Expo 모바일 앱, FastAPI 분석 서버, 브라우저 웹 데모를 함께 포함합니다.

## 현재 구현 범위

- Expo SDK 56 기반 Android/iOS 공통 앱
- `expo-document-picker`를 사용한 오디오/비디오 파일 선택
- FastAPI `/analyze` 업로드 연동
- HNR, HF ratio, Upload readiness 서버 지표 표시
- 잡음 리스크와 개선 제안 카드 표시
- 파일이 없을 때는 데모 리포트로 UI 흐름 확인
- `server/`: FastAPI 분석 서버와 unittest
- `web-demo/`: 브라우저에서 바로 여는 데모 화면. 서버가 켜져 있으면 실제 `/analyze` 업로드 분석도 실행

## 실행

```bash
npm install
npm start
```

Android 기기 또는 에뮬레이터가 준비되어 있으면:

```bash
npm run android
```

서버는 별도 터미널에서 실행합니다.

```bash
cd server
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Android 에뮬레이터는 기본값 `http://10.0.2.2:8000`으로 PC의 FastAPI 서버에 접근합니다. 실제 휴대폰에서 Expo Go로 테스트할 때는 앱의 서버 주소 입력칸에 PC의 같은 와이파이 IP를 넣어야 합니다.

웹 데모는 `web-demo/index.html`을 브라우저에서 열면 됩니다. FastAPI 서버를 켠 상태에서 파일을 선택하면 실제 분석 요청을 보내고, 파일이 없으면 데모 샘플로 시연합니다.

## 검증

```bash
npx expo-doctor
npx expo export --platform android --output-dir dist-android
cd server
python -m py_compile app/main.py app/audio_analysis.py app/__init__.py
python -m unittest discover -s tests
cd ..\web-demo
node --check app.js
```

## 빌드 계획

EAS 로그인이 필요합니다.

```bash
npx eas login
npm run build:apk
npm run build:aab
```

- `build:apk`: 기기에 직접 설치하는 내부 테스트용 APK
- `build:aab`: Google Play 제출용 Android App Bundle

## 제품 구조

```text
Expo 앱
  파일 선택, 업로드, 결과 표시
      |
      v
FastAPI 분석 서버
  FFmpeg 오디오 추출
  Python HNR/HF ratio 근사 계산
  리포트 JSON 생성
      |
      v
Expo 앱
  구간별 리스크, 개선 제안, 업로드 준비도 표시
```

## 중요한 한계

HNR과 HF ratio는 AI 생성 여부를 단독으로 증명하는 지표가 아닙니다. 이 앱은 법적 증거 또는 100% 탐지 도구가 아니라, 제작자가 음성 품질을 점검하고 개선 방향을 잡기 위한 참고용 리포트 도구입니다.

## Google Play 준비 메모

- Expo SDK 56은 Android targetSdkVersion 36 기준이라 Google Play의 Android 15(API 35)+ 요구를 충족하는 방향입니다.
- Google Play 등록에는 AAB, 앱 설명, 아이콘, feature graphic, 스크린샷, 개인정보처리방침 URL, Data Safety Form, 콘텐츠 등급, 내부 테스트가 필요합니다.
- 음성/영상 파일 업로드 기능은 개인정보·초상권·생체정보 이슈가 있을 수 있으므로 보관 기간과 삭제 정책을 명확히 안내해야 합니다.

## 제출 자료

- `docs/`: 제품 명세, 빌드 노트, Google Play 준비 체크리스트, 스토어 문구, 개인정보처리방침 초안
- `store-assets/`: Play Console 업로드용 512x512 아이콘, 1024x500 feature graphic, 1080x1920 휴대폰 스크린샷 4장
- `assets/original_expo_defaults/`: 교체 전 Expo 기본 아이콘 백업
