# VoiceTrace AI 작업 로그

## 2026-06-19

### 목표 시작

- GOAL: VoiceTrace AI를 React Native/Expo 기반으로 실제 APK 배포 가능한 수준까지 기획, 구현, 검증하고, 과정 기록과 제출 문서까지 정리한다.
- 기술 방향: React Native/Expo 앱 + Python/FastAPI 분석 서버.
- 앱 역할: 오디오/비디오 파일 선택, 업로드, 결과 표시, 제작자용 리포트 UI.
- 서버 역할: FFmpeg 오디오 추출, HNR/HF ratio 계산, 스펙트럼 특징 분석, JSON 리포트 생성.

### 완료한 일

- 기존 웹 데모 `voicetrace-ai` 유지.
- React Native/Expo 프로젝트 `voicetrace-mobile` 생성.
- `expo-document-picker` 설치.
- 모바일 MVP 화면 구현:
  - 파일 선택
  - FastAPI 서버 주소 입력
  - 실제 파일 업로드 분석
  - 파일이 없을 때 데모 분석 프로필
  - HNR/HF ratio/Upload readiness 카드
  - 리스크 요약과 개선 제안
- EAS 빌드 설정 `eas.json` 추가:
  - `preview`: APK
  - `production`: AAB
- FastAPI 분석 서버 `voicetrace-api` 추가:
  - `GET /health`
  - `POST /analyze`
  - 50MB MVP 업로드 제한
  - FFmpeg 기반 비-WAV/비디오 오디오 추출
  - WAV 파형 기반 HNR 근사치, HF ratio, 클리핑, 무음 비율 계산
  - 제작자용 분석 JSON 반환
- API 계약 문서 `04_프로토타입/API_CONTRACT.md` 추가.
- 보고서 윤문본에 다음 내용 반영:
  - khuthon 2026(경기 대학 연합 AI·SW 해커톤)
  - 모두의연구소 AIFFEL 딥러닝 리서처 과정 15기 수료
  - 기계학습/딥러닝 모델 구현 가능
  - Three.js, Unity 등 3D 툴과 게임 제작 학습 중
  - Expo 앱과 APK/AAB 빌드 목표
- 최종 제출 문서 재생성:
  - `02_최종본/문건호_VoiceTraceAI_프로젝트기획서_최종.docx`
  - `02_최종본/문건호_VoiceTraceAI_프로젝트기획서_최종.hwpx`
- 최종 제출 문서 양식 복구:
  - 기존 DOCX/HWPX가 Markdown 문단 형태로 풀려 제출 양식의 표 구조가 깨져 있던 문제를 수정.
  - 원본 `AI_실감미디어_프로젝트_기획서_양식.hwpx`의 9개 표 구조를 기준으로 HWPX를 재작성.
  - DOCX도 같은 9개 표 구조로 재작성.
- 제출 패키지 ZIP 갱신:
  - `02_최종본/문건호_VoiceTraceAI_최종제출_패키지.zip`
  - 최종 문서, 윤문본, 진행 기록, 정적 데모, Expo 앱, FastAPI 서버, APK, AAB 포함
  - `node_modules`, `.git`, `.expo`, 개인 도구 폴더, export 결과물, 캐시 폴더 제외
- EAS 프로젝트 생성 및 연결:
  - Expo 계정: `snoopy554`
  - 프로젝트: `@snoopy554/voicetrace-mobile`
  - projectId: `45e6911d-ef1b-4939-8d08-8a5ce5e0080f`
- 내부 테스트용 preview APK 빌드 성공:
  - Build ID: `b9958dd6-9c9d-423d-83e4-5246d7efc8ff`
  - Local artifact: `02_최종본/문건호_VoiceTraceAI_preview.apk`
- Google Play 제출용 production AAB 빌드 성공:
  - Build ID: `9e0ac3e7-3401-43b4-aad9-d6c37a66191c`
  - Local artifact: `02_최종본/문건호_VoiceTraceAI_production.aab`
  - App build version: `2`
- Google Play 준비 문서 추가:
  - `BUILD_NOTES.md`
  - `GOOGLE_PLAY_PREP.md`
  - `PRIVACY_POLICY_DRAFT.md`
  - `STORE_LISTING_DRAFT.md`
- Google Play 스토어 등록 이미지 생성:
  - `05_스토어등록_이미지/icons/play_icon_512.png`
  - `05_스토어등록_이미지/feature_graphic/feature_graphic_1024x500.png`
  - `05_스토어등록_이미지/screenshots_phone/01_input_1080x1920.png`
  - `05_스토어등록_이미지/screenshots_phone/02_upload_1080x1920.png`
  - `05_스토어등록_이미지/screenshots_phone/03_report_1080x1920.png`
  - `05_스토어등록_이미지/screenshots_phone/04_caveat_1080x1920.png`
- `imagegen`으로 생성한 feature graphic 배경을 프로젝트 폴더에 복사하고, 텍스트·아이콘·스크린샷은 Play 등록 규격에 맞춰 로컬 렌더링했다.
- Expo 기본 아이콘을 백업한 뒤 `voicetrace-mobile/assets/`의 앱 아이콘, 스플래시, Android adaptive icon 자산을 VoiceTrace AI 브랜드 이미지로 교체했다.
- 새 브랜드 아이콘 반영 후 EAS 재빌드 완료:
  - Preview APK Build ID: `fa6f498e-8936-4b5e-9527-653115333127`
  - Production AAB Build ID: `21af7cd5-fdbd-4592-9b44-9640e30260ac`
  - Production AAB App build version: `3`
- 프로토타입 추가 개선:
  - FastAPI `/health`가 `version`, `ffmpeg_available`, `max_upload_mb`를 반환하도록 개선.
  - 로컬 웹 데모가 FastAPI `/analyze`로 실제 파일 업로드 분석을 실행하도록 개선.
  - 웹 데모 연동을 위해 FastAPI localhost CORS 설정 추가.
  - 24-bit PCM WAV 분석 호환성 추가.
  - API 서버 unittest 7개 추가.
  - GitHub 저장소에 모바일 앱뿐 아니라 `server/`, `web-demo/`, `docs/API_CONTRACT.md`를 포함.
- 사용자 직접 작업용 체크리스트 추가:
  - `PROTOTYPE_IMPROVEMENT_CHECKLIST.md`

### 에이전트 조사 결과 반영

- 경쟁 분석 결론:
  - 딥페이크 판정기보다 제작자용 Creator Preflight Report로 포지셔닝.
  - HNR/HF ratio는 AI 여부를 단독 판정하지 않는다고 명시.
  - 개인정보, 음성 파일 보관/삭제 정책 필요.
- 기술 조사 결론:
  - 앱 내부 분석보다 서버 분석이 현실적.
  - Expo 앱은 `expo-document-picker`로 파일 선택.
  - EAS Build로 APK/AAB 생성.
  - Play Store에는 AAB, 설명, 스크린샷, 개인정보처리방침, Data Safety Form, 내부 테스트 필요.

### 다음 작업

- Expo 앱을 실제 Android 에뮬레이터 또는 휴대폰에서 서버 연결 테스트.
- Praat/Parselmouth 또는 librosa 기반 지표 추가 검토.
- 프로덕션 서버 HTTPS 배포.
- 개인정보처리방침 초안을 실제 공개 URL에 게시.
- Google Play Console 내부 테스트 트랙에 AAB 업로드.

### 검증

- `npx expo-doctor`: 21/21 통과.
- `npx expo export --platform android --output-dir dist-android`: Android JS 번들 생성 성공.
- `python -m py_compile app/main.py app/audio_analysis.py app/__init__.py`: FastAPI 코드 문법 검증 성공.
- `python -m unittest discover -s tests`: API/오디오 분석 테스트 7개 통과.
- `node --check app.js`: 웹 데모 JavaScript 문법 검증 통과.
- FastAPI `POST /analyze` 테스트:
  - WAV 샘플 업로드 200 응답 확인.
  - MP3 샘플 업로드 200 응답 확인.
  - `analysis_mode`, `duration_sec`, `sample_rate`, `hnr_db`, `hf_ratio`, `upload_readiness`, `risk_label` 반환 확인.
- DOCX/HWPX 내부 텍스트 검증:
  - `React Native/Expo`, `khuthon 2026(경기 대학 연합 AI·SW 해커톤)`, `AIFFEL 딥러닝 리서처 과정 15기`, `Three.js`, `Unity`, `APK`, `AAB` 포함 확인.
- ZIP 내부 목록 검증:
  - 최종 문서, 진행 기록, `voicetrace-ai`, `voicetrace-mobile`, `voicetrace-api` 포함 확인.
  - `node_modules`, `.git`, `.expo`, `dist-android`, `__pycache__` 미포함 확인.
- EAS Build:
  - `npx eas-cli whoami`: `snoopy554` 확인.
  - `npx eas build -p android --profile preview --non-interactive`: APK 빌드 완료.
  - `npx eas build -p android --profile production --non-interactive`: AAB 빌드 완료.
- APK/AAB artifact 검증:
  - APK 내부 `AndroidManifest.xml`, `classes.dex`, `resources.arsc`, `lib/` 확인.
  - AAB 내부 `base/manifest/AndroidManifest.xml`, `base/dex/classes.dex`, `BundleConfig.pb`, `base/lib/` 확인.
- 기기 설치 검증:
  - `adb devices` 실행 결과 연결된 Android 기기/에뮬레이터 없음. 실제 설치 실행 테스트는 다음 단계로 남김.
- 스토어 이미지 검증:
  - Play icon: 512x512 PNG 확인.
  - Feature graphic: 1024x500 PNG/JPG 확인.
  - 휴대폰 스크린샷 4장: 각 1080x1920 PNG 확인.
