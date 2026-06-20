# VoiceTrace AI 프로토타입 개선·점검 체크리스트

## Codex가 이번에 처리한 항목

- FastAPI `/health` 응답 개선
  - `version`, `ffmpeg_available`, `max_upload_mb`를 반환하도록 수정했다.
- FastAPI 브라우저 연동 개선
  - 로컬 웹 데모에서 API를 호출할 수 있도록 localhost CORS를 추가했다.
- 오디오 분석 호환성 개선
  - 24-bit PCM WAV 입력을 처리하도록 `audio_analysis.py`를 보강했다.
- 서버 회귀 테스트 추가
  - 16-bit WAV 분석, 24-bit WAV 분석, 너무 짧은 파일, 무음 파일, `/health`, `/analyze`, 빈 파일 업로드 오류를 unittest로 검증한다.
- 정적 웹 데모 개선
  - 파일이 없으면 데모 샘플로 시연한다.
  - 파일을 선택하고 FastAPI 서버가 켜져 있으면 실제 `/analyze` 업로드 분석을 실행한다.
- GitHub 저장소 구성 개선
  - 모바일 앱뿐 아니라 `server/`, `web-demo/`, `docs/API_CONTRACT.md`를 저장소에 포함했다.
- 새 브랜드 아이콘 반영 APK/AAB 재빌드
  - Preview APK: `fa6f498e-8936-4b5e-9527-653115333127`
  - Production AAB: `21af7cd5-fdbd-4592-9b44-9640e30260ac`
  - Production AAB versionCode: `3`
- 검증 완료
  - `python -m py_compile app/main.py app/audio_analysis.py app/__init__.py`
  - `python -m unittest discover -s tests`
  - `node --check app.js`
  - `npx expo-doctor`
  - `npx expo export --platform android --output-dir dist-android`

## 로컬에서 다시 검증하는 방법

### 1. API 서버 검증

```powershell
cd "글로벌 프로젝트 준비\AI_실감미디어_프로젝트\내_최종제출_준비\04_프로토타입\voicetrace-api"
python -m py_compile app\main.py app\audio_analysis.py app\__init__.py
python -m unittest discover -s tests
```

성공 기준:

- `Ran 7 tests`
- `OK`

### 2. API 서버 실행

```powershell
cd "글로벌 프로젝트 준비\AI_실감미디어_프로젝트\내_최종제출_준비\04_프로토타입\voicetrace-api"
pip install -r requirements.txt
uvicorn app.main:app --reload
```

브라우저에서 확인:

- http://127.0.0.1:8000/health
- `ffmpeg_available`가 `true`면 mp3, m4a, mp4 같은 비-WAV 파일 분석까지 준비된 상태다.

### 3. 웹 데모 실행

```powershell
cd "글로벌 프로젝트 준비\AI_실감미디어_프로젝트\내_최종제출_준비\04_프로토타입\voicetrace-ai"
```

`index.html`을 브라우저로 연다.

성공 기준:

- 파일을 선택하지 않으면 데모 샘플 리포트가 표시된다.
- API 서버를 켠 뒤 파일을 선택하면 `서버 분석 리포트 생성 완료.`가 표시된다.

### 4. 모바일 앱 검증

```powershell
cd "글로벌 프로젝트 준비\AI_실감미디어_프로젝트\내_최종제출_준비\04_프로토타입\voicetrace-mobile"
npx expo-doctor
npx expo export --platform android --output-dir dist-android
```

성공 기준:

- `21/21 checks passed`
- Android bundle export 완료

## 사용자 직접 작업 체크리스트

### 1. 실제 Android 기기 또는 에뮬레이터 테스트

필요한 이유:

- 현재 PC에 연결된 Android 기기/에뮬레이터가 없어 실제 설치, 파일 선택, 서버 업로드 테스트는 자동으로 끝낼 수 없다.

방법:

1. Android 휴대폰에서 개발자 옵션과 USB 디버깅을 켠다.
2. USB로 PC에 연결하고 휴대폰에 뜨는 디버깅 허용 창을 승인한다.
3. PowerShell에서 확인한다.

```powershell
adb devices
```

4. 기기가 보이면 APK를 설치한다.

```powershell
adb install -r "글로벌 프로젝트 준비\AI_실감미디어_프로젝트\내_최종제출_준비\02_최종본\문건호_VoiceTraceAI_preview.apk"
```

5. FastAPI 서버를 PC에서 켠다.
6. 휴대폰과 PC가 같은 Wi-Fi에 있으면 앱의 서버 주소에 PC 내부 IP를 넣는다.

예:

```text
http://192.168.0.12:8000
```

7. 3초 이상 길이의 WAV, MP3, MP4 샘플을 선택해 분석한다.

성공 기준:

- 파일 선택 후 `서버 분석 리포트 생성 완료.`가 표시된다.
- HNR, HF ratio, Upload readiness 값이 바뀐다.

### 2. 실제 기기 스크린샷 교체 여부 결정

필요한 이유:

- 현재 스토어 스크린샷은 앱 UI를 기준으로 규격 렌더링한 이미지다. Play Console에 실제 기기 캡처를 선호한다면 교체하면 된다.

방법:

```powershell
adb shell screencap -p /sdcard/voicetrace_screen.png
adb pull /sdcard/voicetrace_screen.png "글로벌 프로젝트 준비\AI_실감미디어_프로젝트\내_최종제출_준비\05_스토어등록_이미지\screenshots_phone"
```

성공 기준:

- 1080px 이상 고해상도 세로 스크린샷 확보
- 앱 화면 텍스트가 잘리지 않음

### 3. 개인정보처리방침 공개 URL 만들기

필요한 이유:

- Google Play Console은 개인정보처리방침 URL을 요구한다.

방법:

1. `PRIVACY_POLICY_DRAFT.md` 내용을 GitHub Pages, Notion 공개 페이지, Google Sites 중 하나에 게시한다.
2. 공개 브라우저에서 로그인 없이 열리는지 확인한다.
3. URL을 `GOOGLE_PLAY_PREP.md`와 Play Console에 입력한다.

성공 기준:

- 시크릿 창에서 URL 접속 가능
- 앱 이름, 수집 데이터, 보관/삭제 정책, 문의 연락처가 들어 있음

### 4. Google Play Console 내부 테스트 제출

방법:

1. 새 앱 생성: `VoiceTrace AI`
2. Android package 확인: `com.snoopuppy582.voicetraceai`
3. 내부 테스트 트랙에 production AAB 업로드
4. 스토어 등록정보 입력
   - 앱 아이콘: `05_스토어등록_이미지/icons/play_icon_512.png`
   - Feature graphic: `05_스토어등록_이미지/feature_graphic/feature_graphic_1024x500.png`
   - 휴대폰 스크린샷 4장: `05_스토어등록_이미지/screenshots_phone/`
5. Data Safety Form 작성
   - 오디오/비디오 파일은 앱 기능 제공을 위해 서버로 전송
   - 제3자 판매/공유 없음
   - MVP 서버는 임시 파일 처리 후 삭제
6. 콘텐츠 등급 설문 작성
7. 테스트 사용자 이메일 등록

성공 기준:

- 내부 테스트 검토 제출 완료
- 테스트 링크 또는 설치 가능 상태 확인

### 5. 실제 분석 샘플 준비

필요한 이유:

- 발표나 내부 테스트에서 빈 데모보다 실제 샘플을 쓰면 설득력이 높다.

방법:

1. 본인 목소리 또는 사용 허락을 받은 3~10초 음성 샘플 1개 준비
2. AI 생성 음성 또는 AI 영상 음성 샘플 1개 준비
3. 개인정보가 들어간 음성은 사용하지 않는다.
4. 같은 문장 또는 비슷한 길이로 맞추면 비교가 쉽다.

성공 기준:

- 두 파일 모두 앱에서 선택 가능
- 분석 결과의 HNR/HF ratio 차이를 발표에서 설명 가능

## 다음 개발 후보

- 분석 서버 HTTPS 배포
- 서버에 파일 보관 기간/삭제 로그 명시
- Parselmouth 또는 Praat 기반 정밀 HNR 추가
- spectral centroid, spectral rolloff, noise floor 추가
- 앱에 최근 분석 기록 저장
- 앱에서 분석 결과를 이미지 또는 JSON으로 내보내기
