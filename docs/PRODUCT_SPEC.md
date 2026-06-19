# VoiceTrace AI 제품 명세

## 한 줄 정의

생성형 AI 영상/음성 제작자가 업로드 전 음성의 자연스러움, 잡음, 고주파 거칠음, 업로드 준비도를 점검하는 모바일 품질 리포트 앱.

## 타깃 사용자

- 생성형 AI 영상 제작자
- 숏폼 콘텐츠 제작자
- AI 아바타/가상 캐릭터 콘텐츠 제작자
- 강의, 광고, 리뷰 영상의 AI 음성을 점검하려는 사용자

## 핵심 문제

AI 영상은 화면이 자연스러워도 음성에서 잡음, 금속성, 고주파 피로감이 생기면 몰입감이 떨어진다. 제작자는 업로드 전에 이 문제를 빠르게 확인하고, 재생성 또는 후처리 여부를 결정해야 한다.

## 핵심 기능

1. 오디오/비디오 파일 선택
2. 파일 형식, 용량, 길이 기본 검증
3. 분석 서버 업로드
4. HNR, HF ratio, 스펙트럼 특징 분석
5. 구간별 리스크 표시
6. 제작자용 리포트 생성
7. 개선 제안 표시
8. PDF/이미지 리포트 공유

## MVP 범위

- Expo 앱:
  - 파일 선택
  - FastAPI 서버 업로드
  - 서버 분석 결과 표시
  - 파일이 없을 때 데모 분석 결과 표시
  - 리포트 UI
  - APK/AAB 빌드 설정
- 서버:
  - FastAPI 업로드 엔드포인트
  - FFmpeg 기반 비-WAV/비디오 오디오 추출
  - WAV 파형 기반 HNR 근사치, HF ratio, 클리핑, 무음 비율 계산
  - 제작자용 JSON 리포트 반환

## 현재 API 계약

- `POST /analyze`
- 입력: `multipart/form-data`의 `file`
- 제한: 50MB
- 출력:
  - `hnr_db`
  - `hf_ratio`
  - `upload_readiness`
  - `risk_label`
  - `series`
  - `summary`
  - `recommendations`
  - `caveat`

## 비범위

- 100% AI 음성 탐지
- 법적 증거 제공
- 질병/의학적 음성 진단
- 사용자 음성 영구 보관

## 안전 문구

HNR과 HF ratio는 AI 생성 여부를 단독으로 증명하지 않는다. VoiceTrace AI는 제작 품질 개선을 위한 참고용 리포트이며, 법적 증거나 완전한 딥페이크 판정 도구가 아니다.

## 기술 구조

```text
React Native/Expo 앱
  - expo-document-picker
  - 파일 선택
  - 업로드/결과 표시
  - 리포트 UX

FastAPI 분석 서버
  - 파일 수신
  - FFmpeg 오디오 추출
  - Python 신호 분석
  - JSON 리포트 생성

클라우드/Colab
  - 기준 데이터 확장
  - 모델별 샘플 분석
  - 실험 노트북
```

## Google Play 준비 항목

- AAB: `02_최종본/문건호_VoiceTraceAI_production.aab` 생성 완료
- 내부 테스트 APK: `02_최종본/문건호_VoiceTraceAI_preview.apk` 생성 완료
- 앱 이름, 짧은 설명, 전체 설명
- 아이콘 512x512
- Feature graphic 1024x500
- 스크린샷 최소 2장
- 개인정보처리방침 URL: 초안 작성 완료, 공개 URL 게시 필요
- Data Safety Form: 작성 기준 정리 완료, Play Console 입력 필요
- 콘텐츠 등급
- 내부 테스트
