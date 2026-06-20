# VoiceTrace AI Play Console 빠른 입력 가이드

## 1. 설치 테스트

- 이번 제출에서는 생략한다.
- 단, Play Console 내부 테스트 단계에서 실제 설치 확인을 요구하면 `문건호_VoiceTraceAI_preview.apk` 또는 내부 테스트 링크로 확인한다.

## 2. 개인정보처리방침 URL

입력 URL:

```text
https://snoopuppy582.github.io/voicetrace-mobile/privacy-policy.html
```

Play Console 위치:

1. Google Play Console 접속
2. 앱 선택: `VoiceTrace AI`
3. 왼쪽 메뉴 `Policy and programs` 또는 `App content`
4. `Privacy policy`
5. 위 URL 붙여넣기
6. Save

## 3. 내부 테스트 제출

1. `Create app`
   - App name: `VoiceTrace AI`
   - Default language: Korean 또는 English
   - App or game: App
   - Free or paid: Free

2. `Testing > Internal testing`
   - 새 release 생성
   - AAB 업로드:
     - `02_최종본/문건호_VoiceTraceAI_production.aab`
   - Version code: `3`

3. Store listing 입력
   - 앱 이름: `VoiceTrace AI`
   - 짧은 설명: `생성형 영상·음성 업로드 전 잡음, 고주파 거칠음, 업로드 준비도를 점검하는 제작자용 품질 리포트 앱.`
   - 전체 설명: `STORE_LISTING_DRAFT.md` 내용 사용
   - 앱 아이콘: `05_스토어등록_이미지/icons/play_icon_512.png`
   - Feature graphic: `05_스토어등록_이미지/feature_graphic/feature_graphic_1024x500.png`
   - 휴대폰 스크린샷: `05_스토어등록_이미지/screenshots_phone/`의 PNG 4장

4. Data Safety Form 권장 답변
   - 앱이 데이터를 수집하거나 공유하나요?: 파일 분석 기능 때문에 `Yes`
   - 수집 데이터 유형: Audio files, Videos, Files and docs 또는 Play Console 선택지 중 가장 가까운 항목
   - 목적: App functionality
   - 공유: 제3자 판매/공유 없음
   - 처리 방식: 사용자가 선택한 파일을 분석 서버로 전송하고 임시 처리 후 삭제
   - 암호화 전송: 정식 운영 서버는 HTTPS 사용. 로컬 테스트 서버는 개발용이라고 설명
   - 계정 삭제: 앱에 계정 생성 기능 없음

5. 콘텐츠 등급
   - 사용자 생성 음성/영상 파일을 다루지만, 앱 자체가 폭력·성인·도박 콘텐츠를 제공하지 않음
   - 의료 진단, 보안 인증, 법적 증거 제공 앱이 아님

## 4. 제출 전 최종 확인

- ZIP 제출 파일:
  - `02_최종본/문건호_VoiceTraceAI_최종제출_패키지.zip`
- GitHub:
  - https://github.com/snoopuppy582/voicetrace-mobile
- Privacy policy:
  - https://snoopuppy582.github.io/voicetrace-mobile/privacy-policy.html
