# VoiceTrace AI Google Play 준비 체크리스트

## 현재 준비 완료

- Google Play 제출용 AAB 생성: `02_최종본/문건호_VoiceTraceAI_production.aab`
- 내부 테스트/카톡 공유용 APK 생성: `02_최종본/문건호_VoiceTraceAI_preview.apk`
- Android package: `com.snoopuppy582.voicetraceai`
- Version: `1.0.0`
- Version code: `2`
- EAS project: https://expo.dev/accounts/snoopy554/projects/voicetrace-mobile
- 앱 기능 설명 초안: `STORE_LISTING_DRAFT.md`
- 개인정보처리방침 초안: `PRIVACY_POLICY_DRAFT.md`
- 앱 아이콘 512x512: `05_스토어등록_이미지/icons/play_icon_512.png`
- Feature graphic 1024x500: `05_스토어등록_이미지/feature_graphic/feature_graphic_1024x500.png`
- 휴대전화 스크린샷 4장: `05_스토어등록_이미지/screenshots_phone/`
- 스토어 자산 목록: `05_스토어등록_이미지/STORE_ASSETS_MANIFEST.md`

## Play Console에서 해야 할 일

1. 새 앱 생성
   - 앱 이름: `VoiceTrace AI`
   - 기본 언어: 한국어 또는 영어 중 선택
   - 앱/게임: 앱
   - 무료/유료: 무료

2. AAB 업로드
   - 내부 테스트 트랙에 `문건호_VoiceTraceAI_production.aab` 업로드
   - 테스트 계정 또는 이메일 리스트 지정
   - 내부 테스트에서 설치/실행 확인 후 프로덕션 제출 검토

3. 스토어 등록정보 작성
   - 짧은 설명
   - 전체 설명
   - 앱 아이콘 512x512: `play_icon_512.png` 업로드
   - Feature graphic 1024x500: `feature_graphic_1024x500.png` 업로드
   - 휴대전화 스크린샷: 1080x1920 PNG 4장 업로드
   - 필요하면 태블릿 스크린샷 추가

4. 개인정보처리방침 URL 등록
   - `PRIVACY_POLICY_DRAFT.md`를 GitHub Pages, Notion 공개 페이지, Google Sites 등 URL이 있는 곳에 게시
   - Play Console의 App content > Privacy policy에 URL 입력

5. Data Safety Form 작성
   - 사용자가 선택한 오디오/비디오 파일은 분석 서버로 전송됨
   - 목적: 앱 기능, 음성 품질 분석 리포트 제공
   - 공유: 제3자 공유 없음으로 설계
   - 보관: MVP 서버는 임시 파일로 처리 후 삭제
   - 운영 배포 시 HTTPS 적용 필수

6. 콘텐츠 등급과 정책
   - 사용자 생성 음성/영상 파일을 다루므로 개인정보, 초상권, 음성권 안내 필요
   - AI 생성 여부를 단정하지 않는다는 한계 문구 유지
   - 법적 증거, 보안 탐지, 의료 진단처럼 오해될 표현 금지

## 공식 문서 기준 확인 사항

- Google Play는 Data safety 섹션에서 앱의 데이터 수집, 공유, 보호 방식을 개발자가 직접 신고하도록 요구한다.  
  https://support.google.com/googleplay/android-developer/answer/10787469
- Google Play 신규 앱/업데이트는 Android 15(API 35) 이상 target API 요구를 충족해야 한다.  
  https://developer.android.com/google/play/requirements/target-sdk
- 스토어 등록에는 feature graphic, screenshots, short description 등 preview assets가 필요하다.  
  https://support.google.com/googleplay/android-developer/answer/9866151

## 아직 남은 작업

- 실제 Android 기기에서 APK 설치 후 서버 주소 입력, 파일 업로드, 결과 표시 확인
- 프로덕션 서버 HTTPS 배포
- 개인정보처리방침 URL 공개
- 실제 Android 기기 또는 에뮬레이터에서 앱 설치 후 스크린샷 교체 여부 확인
- 새 아이콘이 반영된 APK/AAB 재빌드 여부 확인
- Play Console 내부 테스트 제출
