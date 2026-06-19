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
- Build ID: `b9958dd6-9c9d-423d-83e4-5246d7efc8ff`
- Build URL: https://expo.dev/accounts/snoopy554/projects/voicetrace-mobile/builds/b9958dd6-9c9d-423d-83e4-5246d7efc8ff
- Artifact URL: https://expo.dev/artifacts/eas/_5r8SJ1lyscRyy7CAqZgMc565EpYUA9yBZkPoF4gOGk.apk
- Local artifact: `02_최종본/문건호_VoiceTraceAI_preview.apk`
- Local size: 67,549,557 bytes
- Verification: APK ZIP 구조에서 `AndroidManifest.xml`, `classes.dex`, `resources.arsc`, `lib/` 항목 확인.

## Production AAB

- Build profile: `production`
- Distribution: `STORE`
- Build ID: `9e0ac3e7-3401-43b4-aad9-d6c37a66191c`
- Build URL: https://expo.dev/accounts/snoopy554/projects/voicetrace-mobile/builds/9e0ac3e7-3401-43b4-aad9-d6c37a66191c
- Artifact URL: https://expo.dev/artifacts/eas/V8M-iioSmB8pRLVO-ZmDfhrPbnOcl-ws_QXpnCYSqbk.aab
- Local artifact: `02_최종본/문건호_VoiceTraceAI_production.aab`
- Local size: 46,331,075 bytes
- App build version: `2`
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
- Preview APK와 production AAB 모두 EAS Build 성공.
- 현재 PC에 `adb devices`로 연결된 Android 기기/에뮬레이터가 없어 실제 설치 실행 테스트는 아직 못 했다.

## Store Asset Status

- Google Play용 512x512 앱 아이콘, 1024x500 feature graphic, 1080x1920 휴대폰 스크린샷 4장을 생성했다.
- 산출물 위치: `05_스토어등록_이미지/`
- Feature graphic 배경은 Codex `imagegen` built-in tool 결과물을 사용했고, 최종 문구와 스크린샷 UI는 로컬 렌더링으로 규격에 맞췄다.
- `voicetrace-mobile/assets/`의 Expo 기본 아이콘은 `assets/original_expo_defaults/`에 백업했고, VoiceTrace AI 브랜드 아이콘으로 교체했다.
- 주의: 기존 APK/AAB는 아이콘 교체 전 빌드다. 새 브랜드 아이콘까지 앱 바이너리에 반영하려면 EAS preview/production 빌드를 한 번 더 실행해야 한다.
