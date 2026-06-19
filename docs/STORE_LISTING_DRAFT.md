# VoiceTrace AI 스토어 등록 문구 초안

## 앱 이름

VoiceTrace AI

## 짧은 설명

생성형 영상·음성 업로드 전 잡음, 고주파 거칠음, 업로드 준비도를 점검하는 제작자용 품질 리포트 앱.

## 전체 설명

VoiceTrace AI는 생성형 AI 영상과 음성 콘텐츠를 만드는 제작자를 위한 업로드 전 품질 점검 앱입니다.

AI 영상은 화면이 자연스러워도 음성에서 잡음, 금속성 질감, 고주파 피로감이 남으면 몰입도가 떨어질 수 있습니다. VoiceTrace AI는 사용자가 선택한 오디오 또는 비디오 파일을 분석하고, HNR, HF ratio, 클리핑, 무음 비율 같은 신호 특징을 바탕으로 제작자용 리포트를 제공합니다.

주요 기능:

- 오디오/비디오 파일 선택
- 음성 품질 지표 분석
- HNR, HF ratio, 업로드 준비도 표시
- 잡음 또는 고주파 거칠음 리스크 요약
- 재생성, EQ, de-esser, 노이즈 리덕션 등 개선 제안
- 제작 로그로 활용 가능한 품질 리포트

VoiceTrace AI는 딥페이크를 100% 판정하는 앱이 아닙니다. 분석 지표는 AI 생성 여부를 법적으로 증명하기 위한 것이 아니라, 제작자가 업로드 전에 음성 품질을 점검하고 후처리 방향을 정하는 데 도움을 주기 위한 참고 정보입니다.

## 이번 버전

- React Native/Expo 기반 Android MVP
- 오디오/비디오 파일 선택 기능
- FastAPI 분석 서버 연동 구조
- HNR/HF ratio 기반 품질 리포트
- 내부 테스트용 APK와 Google Play 제출용 AAB 빌드 완료

## 스크린샷 파일

- 1번: `05_스토어등록_이미지/screenshots_phone/01_input_1080x1920.png`
- 2번: `05_스토어등록_이미지/screenshots_phone/02_upload_1080x1920.png`
- 3번: `05_스토어등록_이미지/screenshots_phone/03_report_1080x1920.png`
- 4번: `05_스토어등록_이미지/screenshots_phone/04_caveat_1080x1920.png`

## 등록 이미지 파일

- 앱 아이콘: `05_스토어등록_이미지/icons/play_icon_512.png`
- Feature graphic: `05_스토어등록_이미지/feature_graphic/feature_graphic_1024x500.png`
- Feature graphic 백업 JPG: `05_스토어등록_이미지/feature_graphic/feature_graphic_1024x500.jpg`

## 금지하거나 피해야 할 표현

- AI 음성을 100% 탐지
- 딥페이크를 완벽 판정
- 법적 증거 제공
- 의료적 음성 진단
- 보안 인증 또는 신원 확인
