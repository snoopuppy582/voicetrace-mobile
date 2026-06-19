import { useMemo, useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  Platform,
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import * as DocumentPicker from 'expo-document-picker';

const DEFAULT_API_BASE_URL = Platform.OS === 'android' ? 'http://10.0.2.2:8000' : 'http://127.0.0.1:8000';

const SAMPLES = {
  balanced: {
    label: 'AI 생성 음성 - 안정적',
    hnr: 15.2,
    hfRatio: 0.27,
    readiness: 82,
    risk: '양호',
    color: '#2468d8',
    series: [0.56, 0.64, 0.58, 0.68, 0.62, 0.66, 0.61],
    source: 'demo',
    durationSec: 0,
    summary:
      'AI 생성 음성이지만 비교적 안정적인 범위입니다. 일부 구간에서 가벼운 거칠음이 느껴질 수 있어 업로드 전 짧은 후처리를 권장합니다.',
    recommendations: ['짧은 노이즈 리덕션 적용', '고주파 대역 de-esser 약하게 적용', '최종 업로드 전 이어폰으로 재청취'],
    caveat: '데모 샘플입니다. 실제 파일을 선택하면 서버 분석 결과로 교체됩니다.',
  },
  noisy: {
    label: 'AI 생성 음성 - 잡음 의심',
    hnr: 9.8,
    hfRatio: 0.42,
    readiness: 54,
    risk: '잡음 의심',
    color: '#bd2f3a',
    series: [0.38, 0.48, 0.35, 0.44, 0.32, 0.46, 0.39],
    source: 'demo',
    durationSec: 0,
    summary:
      'HNR이 낮아 목소리 뒤에 거친 잡음이 섞여 들릴 가능성이 큽니다. 영상 몰입도를 떨어뜨릴 수 있어 재생성 또는 후처리를 먼저 검토해야 합니다.',
    recommendations: ['동일 프롬프트로 1회 재생성', '배경음과 음성 분리 후 노이즈 제거', '잡음 구간 타임라인 재확인'],
    caveat: '데모 샘플입니다. 실제 파일을 선택하면 서버 분석 결과로 교체됩니다.',
  },
  bright: {
    label: 'AI 생성 음성 - 고주파 과다',
    hnr: 12.4,
    hfRatio: 0.55,
    readiness: 63,
    risk: '고주파 과다',
    color: '#b76b00',
    series: [0.46, 0.51, 0.48, 0.58, 0.49, 0.61, 0.52],
    source: 'demo',
    durationSec: 0,
    summary:
      'HF ratio가 높게 나타나 금속성 또는 날카로운 음색으로 들릴 수 있습니다. 숏폼처럼 이어폰 시청 비율이 높은 콘텐츠에서는 피로감이 커질 수 있습니다.',
    recommendations: ['고주파 대역 EQ 완화', '치찰음 구간 de-esser 적용', '음성 모델 또는 보이스 프리셋 변경 테스트'],
    caveat: '데모 샘플입니다. 실제 파일을 선택하면 서버 분석 결과로 교체됩니다.',
  },
};

const DEFAULT_PROFILE = SAMPLES.balanced;

function getRiskColor(label) {
  if (label === '검토 필요' || label === '잡음 의심') return '#bd2f3a';
  if (label === '주의' || label === '고주파 과다') return '#b76b00';
  return '#2468d8';
}

function normalizeApiBaseUrl(value) {
  return value.trim().replace(/\/+$/, '');
}

function mapServerResult(result) {
  const risk = result.risk_label ?? '주의';
  return {
    label: result.filename ?? '업로드 파일',
    hnr: Number(result.hnr_db ?? 0),
    hfRatio: Number(result.hf_ratio ?? 0),
    readiness: Number(result.upload_readiness ?? 0),
    risk,
    color: getRiskColor(risk),
    series: Array.isArray(result.series) && result.series.length > 0 ? result.series : DEFAULT_PROFILE.series,
    source: result.analysis_mode ?? 'server',
    durationSec: Number(result.duration_sec ?? 0),
    summary: result.summary ?? '분석 결과 요약을 불러오지 못했습니다.',
    recommendations:
      Array.isArray(result.recommendations) && result.recommendations.length > 0
        ? result.recommendations
        : ['업로드 파일을 다시 확인', '서버 로그 확인'],
    caveat: result.caveat ?? 'HNR/HF ratio는 AI 생성 여부를 단독으로 증명하지 않습니다.',
  };
}

function MetricCard({ label, value, tone }) {
  return (
    <View style={styles.metricCard}>
      <Text style={styles.metricLabel}>{label}</Text>
      <Text style={[styles.metricValue, tone ? { color: tone } : null]}>{value}</Text>
    </View>
  );
}

function MiniChart({ series, color }) {
  return (
    <View style={styles.chart}>
      {series.map((value, index) => (
        <View key={`${value}-${index}`} style={styles.chartColumn}>
          <View style={[styles.chartBar, { height: `${Math.round(value * 100)}%`, backgroundColor: color }]} />
        </View>
      ))}
    </View>
  );
}

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [profileKey, setProfileKey] = useState('balanced');
  const [analysis, setAnalysis] = useState(DEFAULT_PROFILE);
  const [status, setStatus] = useState('파일을 선택하면 FastAPI 서버 분석을 실행합니다.');
  const [apiBaseUrl, setApiBaseUrl] = useState(DEFAULT_API_BASE_URL);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const activeProfile = SAMPLES[profileKey];

  const filename = useMemo(() => {
    if (!selectedFile) return '선택된 파일 없음';
    const sizeMb = selectedFile.size ? ` · ${(selectedFile.size / 1024 / 1024).toFixed(2)}MB` : '';
    return `${selectedFile.name}${sizeMb}`;
  }, [selectedFile]);

  const pickFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['audio/*', 'video/*'],
        copyToCacheDirectory: true,
        multiple: false,
      });

      if (result.canceled) return;
      const asset = result.assets?.[0];
      if (!asset) return;

      setSelectedFile(asset);
      setStatus('파일 선택 완료. 서버 주소를 확인한 뒤 분석 리포트를 생성하세요.');
    } catch (error) {
      Alert.alert('파일 선택 실패', error?.message ?? '파일을 선택하는 중 문제가 발생했습니다.');
    }
  };

  const runDemoAnalysis = () => {
    setAnalysis(activeProfile);
    setStatus('데모 리포트 생성 완료. 실제 파일 분석은 서버 업로드로 실행됩니다.');
  };

  const runAnalysis = async () => {
    if (!selectedFile) {
      runDemoAnalysis();
      return;
    }

    const baseUrl = normalizeApiBaseUrl(apiBaseUrl);
    if (!baseUrl) {
      Alert.alert('서버 주소 필요', 'FastAPI 서버 주소를 입력하세요.');
      return;
    }

    const formData = new FormData();
    formData.append('file', {
      uri: selectedFile.uri,
      name: selectedFile.name || 'upload-media',
      type: selectedFile.mimeType || 'application/octet-stream',
    });

    setIsAnalyzing(true);
    setStatus('서버로 파일을 업로드하고 음성 특징을 계산하는 중입니다.');

    try {
      const response = await fetch(`${baseUrl}/analyze`, {
        method: 'POST',
        body: formData,
      });
      const payload = await response.json().catch(() => null);
      if (!response.ok) {
        const detail = payload?.detail ?? `HTTP ${response.status}`;
        throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
      }

      setAnalysis(mapServerResult(payload));
      setStatus('서버 분석 리포트 생성 완료.');
    } catch (error) {
      const message = error?.message ?? '서버 분석 중 문제가 발생했습니다.';
      setStatus(`분석 실패: ${message}`);
      Alert.alert('분석 실패', message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" />
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.hero}>
          <Text style={styles.eyebrow}>Creator Preflight Report</Text>
          <Text style={styles.title}>VoiceTrace AI</Text>
          <Text style={styles.subtitle}>
            생성형 영상 속 인물 음성의 자연스러움, 잡음, 고주파 거칠음을 점검하는 제작자용 품질 리포트 앱
          </Text>
        </View>

        <View style={styles.panel}>
          <Text style={styles.sectionTitle}>분석 입력</Text>
          <Text style={styles.label}>FastAPI 서버 주소</Text>
          <TextInput
            value={apiBaseUrl}
            onChangeText={setApiBaseUrl}
            autoCapitalize="none"
            autoCorrect={false}
            keyboardType="url"
            placeholder="http://10.0.2.2:8000"
            style={styles.input}
          />

          <Text style={styles.label}>데모 분석 프로필</Text>
          <View style={styles.segmentRow}>
            {Object.entries(SAMPLES).map(([key, item]) => (
              <TouchableOpacity
                key={key}
                style={[styles.segment, profileKey === key && styles.segmentActive]}
                onPress={() => setProfileKey(key)}
              >
                <Text style={[styles.segmentText, profileKey === key && styles.segmentTextActive]}>{item.risk}</Text>
              </TouchableOpacity>
            ))}
          </View>

          <Text style={styles.label}>오디오/비디오 파일</Text>
          <TouchableOpacity style={styles.fileButton} onPress={pickFile} disabled={isAnalyzing}>
            <Text style={styles.fileButtonText}>파일 선택</Text>
          </TouchableOpacity>
          <Text style={styles.filename}>{filename}</Text>

          <TouchableOpacity
            style={[styles.primaryButton, isAnalyzing && styles.primaryButtonDisabled]}
            onPress={runAnalysis}
            disabled={isAnalyzing}
          >
            {isAnalyzing ? (
              <ActivityIndicator color="#ffffff" />
            ) : (
              <Text style={styles.primaryButtonText}>{selectedFile ? '서버 분석 리포트 생성' : '데모 리포트 생성'}</Text>
            )}
          </TouchableOpacity>
          <Text style={styles.status}>{status}</Text>
        </View>

        <View style={styles.panel}>
          <Text style={styles.sectionTitle}>분석 결과</Text>
          <View style={styles.metricGrid}>
            <MetricCard label="HNR" value={`${analysis.hnr.toFixed(1)} dB`} />
            <MetricCard label="HF ratio" value={analysis.hfRatio.toFixed(2)} />
            <MetricCard label="Upload readiness" value={`${analysis.readiness}/100`} tone={analysis.color} />
          </View>

          <MiniChart series={analysis.series} color={analysis.color} />

          <View style={styles.reportBox}>
            <Text style={styles.riskLabel}>{analysis.risk}</Text>
            <Text style={styles.reportText}>{analysis.summary}</Text>
          </View>

          <View style={styles.metaRow}>
            <Text style={styles.metaText}>분석 방식: {analysis.source}</Text>
            <Text style={styles.metaText}>
              {analysis.durationSec > 0 ? `길이: ${analysis.durationSec.toFixed(2)}초` : '데모 데이터'}
            </Text>
          </View>

          <Text style={styles.sectionTitleSmall}>개선 제안</Text>
          {analysis.recommendations.map((item) => (
            <View key={item} style={styles.recommendation}>
              <View style={[styles.dot, { backgroundColor: analysis.color }]} />
              <Text style={styles.recommendationText}>{item}</Text>
            </View>
          ))}
          <Text style={styles.caveat}>{analysis.caveat}</Text>
        </View>

        <View style={styles.notePanel}>
          <Text style={styles.noteTitle}>제품 설계 메모</Text>
          <Text style={styles.noteText}>
            MVP에서는 Expo 앱이 파일 선택과 결과 UI를 맡고, FFmpeg 기반 오디오 추출과 HNR/HF ratio 계산은 Python/FastAPI
            서버에서 처리합니다. HNR과 HF ratio는 AI 여부를 단독 판정하는 지표가 아니며, 제작 품질 개선을 위한 참고 리포트로
            사용합니다.
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#f5f7fb',
  },
  container: {
    padding: 20,
    paddingBottom: 36,
  },
  hero: {
    marginBottom: 18,
  },
  eyebrow: {
    color: '#2468d8',
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 8,
  },
  title: {
    color: '#121a24',
    fontSize: 40,
    fontWeight: '800',
    letterSpacing: 0,
  },
  subtitle: {
    color: '#5f6c7b',
    fontSize: 16,
    lineHeight: 24,
    marginTop: 12,
  },
  panel: {
    backgroundColor: '#ffffff',
    borderColor: '#d9e2ec',
    borderWidth: 1,
    marginTop: 14,
    padding: 18,
  },
  sectionTitle: {
    color: '#121a24',
    fontSize: 21,
    fontWeight: '800',
    marginBottom: 14,
  },
  sectionTitleSmall: {
    color: '#121a24',
    fontSize: 16,
    fontWeight: '800',
    marginTop: 18,
    marginBottom: 10,
  },
  label: {
    color: '#243447',
    fontSize: 14,
    fontWeight: '700',
    marginTop: 10,
    marginBottom: 8,
  },
  input: {
    borderColor: '#d9e2ec',
    borderWidth: 1,
    color: '#121a24',
    fontSize: 14,
    paddingHorizontal: 12,
    paddingVertical: 12,
  },
  segmentRow: {
    flexDirection: 'row',
    gap: 8,
  },
  segment: {
    flex: 1,
    borderColor: '#d9e2ec',
    borderWidth: 1,
    paddingHorizontal: 6,
    paddingVertical: 11,
    alignItems: 'center',
  },
  segmentActive: {
    backgroundColor: '#2468d8',
    borderColor: '#2468d8',
  },
  segmentText: {
    color: '#4c5b6b',
    fontSize: 12,
    fontWeight: '700',
  },
  segmentTextActive: {
    color: '#ffffff',
  },
  fileButton: {
    borderColor: '#2468d8',
    borderWidth: 1,
    paddingVertical: 13,
    alignItems: 'center',
  },
  fileButtonText: {
    color: '#2468d8',
    fontSize: 15,
    fontWeight: '800',
  },
  filename: {
    color: '#5f6c7b',
    fontSize: 13,
    lineHeight: 20,
    marginTop: 8,
  },
  primaryButton: {
    backgroundColor: '#2468d8',
    marginTop: 16,
    minHeight: 50,
    paddingVertical: 15,
    alignItems: 'center',
    justifyContent: 'center',
  },
  primaryButtonDisabled: {
    backgroundColor: '#789bd6',
  },
  primaryButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '800',
  },
  status: {
    color: '#5f6c7b',
    fontSize: 13,
    lineHeight: 20,
    marginTop: 10,
  },
  metricGrid: {
    flexDirection: 'row',
    gap: 8,
  },
  metricCard: {
    flex: 1,
    borderColor: '#d9e2ec',
    borderWidth: 1,
    minHeight: 78,
    padding: 12,
  },
  metricLabel: {
    color: '#6b7785',
    fontSize: 11,
    fontWeight: '700',
  },
  metricValue: {
    color: '#121a24',
    fontSize: 19,
    fontWeight: '800',
    marginTop: 8,
  },
  chart: {
    height: 150,
    borderColor: '#d9e2ec',
    borderWidth: 1,
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 10,
    marginTop: 16,
    paddingHorizontal: 18,
    paddingVertical: 16,
  },
  chartColumn: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'flex-end',
    height: '100%',
  },
  chartBar: {
    width: '68%',
    minHeight: 16,
    borderRadius: 999,
  },
  reportBox: {
    backgroundColor: '#f5f7fb',
    borderColor: '#d9e2ec',
    borderWidth: 1,
    marginTop: 16,
    padding: 14,
  },
  riskLabel: {
    color: '#121a24',
    fontSize: 16,
    fontWeight: '800',
    marginBottom: 8,
  },
  reportText: {
    color: '#4c5b6b',
    fontSize: 14,
    lineHeight: 22,
  },
  metaRow: {
    borderBottomColor: '#d9e2ec',
    borderBottomWidth: 1,
    borderTopColor: '#d9e2ec',
    borderTopWidth: 1,
    marginTop: 12,
    paddingVertical: 10,
  },
  metaText: {
    color: '#5f6c7b',
    fontSize: 12,
    lineHeight: 18,
  },
  recommendation: {
    flexDirection: 'row',
    gap: 8,
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginTop: 6,
  },
  recommendationText: {
    color: '#4c5b6b',
    flex: 1,
    fontSize: 14,
    lineHeight: 20,
  },
  caveat: {
    color: '#6b7785',
    fontSize: 12,
    lineHeight: 18,
    marginTop: 10,
  },
  notePanel: {
    backgroundColor: '#eef4ff',
    borderColor: '#c8d8f4',
    borderWidth: 1,
    marginTop: 14,
    padding: 16,
  },
  noteTitle: {
    color: '#1f4e79',
    fontSize: 15,
    fontWeight: '800',
    marginBottom: 8,
  },
  noteText: {
    color: '#405163',
    fontSize: 13,
    lineHeight: 21,
  },
});
