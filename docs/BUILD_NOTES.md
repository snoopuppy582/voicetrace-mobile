# VoiceTrace AI 빌드 노트

## EAS 프로젝트

- Expo 계정: `snoopy554`
- 프로젝트: `@snoopy554/voicetrace-mobile`
- 프로젝트 URL: https://expo.dev/accounts/snoopy554/projects/voicetrace-mobile
- EAS projectId: `45e6911d-ef1b-4939-8d08-8a5ce5e0080f`
- Android package: `com.snoopuppy582.voicetraceai`
- App version: `1.0.0`

## Preview APK

- Build profile: `preview`
- Distribution: `INTERNAL`
- Build ID: `fa6f498e-8936-4b5e-9527-653115333127`
- Build URL: https://expo.dev/accounts/snoopy554/projects/voicetrace-mobile/builds/fa6f498e-8936-4b5e-9527-653115333127
- Artifact URL: https://expo.dev/artifacts/eas/cruimZnynM7jFx6_BniFTk7v5_TRohiUcPhs8M4klSY.apk
- Local artifact: `02_최종본/문건호_VoiceTraceAI_preview.apk`
- Local size: 67,350,817 bytes
- Verification: APK ZIP 구조에서 `AndroidManifest.xml`, `classes.dex`, `resources.arsc`, `lib/` 항목 확인.

## Production AAB

- Build profile: `production`
- Distribution: `STORE`
- Build ID: `21af7cd5-fdbd-4592-9b44-9640e30260ac`
- Build URL: https://expo.dev/accounts/snoopy554/projects/voicetrace-mobile/builds/21af7cd5-fdbd-4592-9b44-9640e30260ac
- Artifact URL: https://expo.dev/artifacts/eas/bwi4fbJXwJaOKicy6SGKSxQ5E52gvtjhx6WKUD_MC4M.aab
- Local artifact: `02_최종본/문건호_VoiceTraceAI_production.aab`
- Local size: 46,126,964 bytes
- App build version: `3`
- Verification: AAB ZIP 구조에서 `base/manifest/AndroidManifest.xml`, `base/dex/classes.dex`, `BundleConfig.pb`, `base/lib/` 항목 확인.

## Commands

```bash
cd 글로벌 프로젝트 준비/AI_실감미디어_프로젝트/내_최종제출_준비/04_프로토타입/voicetrace-mobile
npm install
npx eas-cli whoami
npm run build:apk
npm run build:aab
```

비Git 폴더에서 빌드할 때는 다음 환경변수를 사용했다.

```powershell
$env:EAS_NO_VCS='1'
```

## Runtime Test Status

- `npx expo-doctor`: 21/21 통과.
- `npx expo export --platform android --output-dir dist-android`: Android JS 번들 생성 성공.
- `python -m unittest discover -s tests`: FastAPI 분석 서버 테스트 7개 통과.
- `node --check app.js`: 정적 웹 데모 JavaScript 문법 검증 통과.
- 새 브랜드 아이콘이 반영된 preview APK와 production AAB 모두 EAS Build 성공.
- 현재 PC에 `adb devices`로 연결된 Android 기기/에뮬레이터가 없어 실제 설치 실행 테스트는 아직 못 했다.

## Store Asset Status

- Google Play용 512x512 앱 아이콘, 1024x500 feature graphic, 1080x1920 휴대폰 스크린샷 4장을 생성했다.
- 산출물 위치: `05_스토어등록_이미지/`
- Feature graphic 배경은 Codex `imagegen` built-in tool 결과물을 사용했고, 최종 문구와 스크린샷 UI는 로컬 렌더링으로 규격에 맞췄다.
- `voicetrace-mobile/assets/`의 Expo 기본 아이콘은 `assets/original_expo_defaults/`에 백업했고, VoiceTrace AI 브랜드 아이콘으로 교체했다.
- 새 브랜드 아이콘을 앱 바이너리에 반영한 APK/AAB 재빌드까지 완료했다.
