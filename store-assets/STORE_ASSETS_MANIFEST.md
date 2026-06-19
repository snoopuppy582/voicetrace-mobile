# VoiceTrace AI Store Assets Manifest

## Google Play 규격 파일

- `icons/play_icon_512.png`: 512x512 PNG 앱 아이콘
- `feature_graphic/feature_graphic_1024x500.png`: 1024x500 PNG feature graphic
- `feature_graphic/feature_graphic_1024x500.jpg`: 1024x500 JPG feature graphic 백업
- `screenshots_phone/01_input_1080x1920.png`: 휴대폰 스크린샷 1
- `screenshots_phone/02_upload_1080x1920.png`: 휴대폰 스크린샷 2
- `screenshots_phone/03_report_1080x1920.png`: 휴대폰 스크린샷 3
- `screenshots_phone/04_caveat_1080x1920.png`: 휴대폰 스크린샷 4

## 생성 방식

- Feature graphic 배경은 Codex `imagegen` built-in tool로 생성한 이미지를 사용했다.
- 텍스트, 아이콘, 스크린샷은 Google Play 규격에 맞게 로컬 렌더링했다.
- 현재 연결된 Android 기기/에뮬레이터가 없어 `adb screencap` 실기기 촬영은 수행하지 못했다.

## 앱 자산 반영

- Expo 기본 아이콘은 `voicetrace-mobile/assets/original_expo_defaults/`에 백업했다.
- `assets/icon.png`, `splash-icon.png`, Android adaptive icon 자산을 VoiceTrace AI 브랜드 아이콘으로 교체했다.