const profiles = {
  human: {
    hnr: 18.7,
    hf: 0.18,
    badge: "기준 범위",
    color: "#16805b",
    series: [0.92, 0.94, 0.91, 0.95, 0.93, 0.94, 0.92],
    report:
      "인간 발화 기준 샘플에 가까운 안정적인 패턴입니다. HNR이 높고 HF ratio가 낮아 잡음성 고주파 성분이 적은 편입니다.",
  },
  "ai-balanced": {
    hnr: 15.2,
    hf: 0.27,
    badge: "양호",
    color: "#2468d8",
    series: [0.82, 0.79, 0.84, 0.81, 0.8, 0.83, 0.82],
    report:
      "AI 생성 음성이지만 비교적 안정적인 범위에 있습니다. 다만 인간 발화 기준보다 HNR이 낮아 일부 구간에서 가벼운 거칠음이 느껴질 수 있습니다.",
  },
  "ai-noisy": {
    hnr: 9.8,
    hf: 0.42,
    badge: "잡음 의심",
    color: "#bd2f3a",
    series: [0.62, 0.45, 0.55, 0.52, 0.48, 0.58, 0.54],
    report:
      "HNR이 낮아 음성 뒤에 잡음이 섞여 들릴 가능성이 큽니다. 영상 자체가 자연스럽더라도 목소리 품질 때문에 몰입감이 떨어질 수 있어 재생성이나 후처리를 권장합니다.",
  },
  "ai-bright": {
    hnr: 12.4,
    hf: 0.55,
    badge: "고주파 과다",
    color: "#b76b00",
    series: [0.65, 0.67, 0.61, 0.69, 0.64, 0.7, 0.66],
    report:
      "HF ratio가 높게 나타나 금속성 또는 날카로운 음색으로 들릴 수 있습니다. 프롬프트 조정이나 고주파 대역 후처리를 검토하는 것이 좋습니다.",
  },
};

const sample = document.querySelector("#sample");
const apiBase = document.querySelector("#apiBase");
const file = document.querySelector("#file");
const button = document.querySelector("#analyze");
const statusText = document.querySelector("#status");
const hnr = document.querySelector("#hnr");
const hf = document.querySelector("#hf");
const badge = document.querySelector("#badge");
const filename = document.querySelector("#filename");
const reportText = document.querySelector("#reportText");
const chart = document.querySelector("#chart");
const ctx = chart.getContext("2d");

function riskColor(label) {
  if (label === "검토 필요" || label === "잡음 의심") return "#bd2f3a";
  if (label === "주의" || label === "고주파 과다") return "#b76b00";
  return "#2468d8";
}

function normalizeApiBaseUrl(value) {
  return value.trim().replace(/\/+$/, "");
}

function mapServerResult(result) {
  const risk = result.risk_label || "주의";
  return {
    hnr: Number(result.hnr_db || 0),
    hf: Number(result.hf_ratio || 0),
    badge: risk,
    color: riskColor(risk),
    series: Array.isArray(result.series) && result.series.length > 0 ? result.series.map(Number) : [0.5, 0.5, 0.5, 0.5],
    report: result.summary || "분석 결과 요약을 불러오지 못했습니다.",
  };
}

function drawChart(profile) {
  ctx.clearRect(0, 0, chart.width, chart.height);
  const padding = 46;
  const width = chart.width - padding * 2;
  const height = chart.height - padding * 2;
  const max = 1;
  const min = 0;

  ctx.strokeStyle = "#d8dee8";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i += 1) {
    const y = padding + (height / 4) * i;
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(chart.width - padding, y);
    ctx.stroke();
  }

  ctx.fillStyle = "#66717d";
  ctx.font = "14px Malgun Gothic, sans-serif";
  ctx.fillText("구간별 업로드 준비도 추이", padding, 28);
  ctx.fillText("낮음", 10, chart.height - padding);
  ctx.fillText("높음", 10, padding + 6);

  const points = profile.series.map((value, index) => {
    const x = padding + (width / (profile.series.length - 1)) * index;
    const clamped = Math.min(Math.max(Number(value), min), max);
    const y = padding + height - ((clamped - min) / (max - min)) * height;
    return { x, y };
  });

  ctx.strokeStyle = profile.color;
  ctx.lineWidth = 4;
  ctx.beginPath();
  points.forEach((point, index) => {
    if (index === 0) ctx.moveTo(point.x, point.y);
    else ctx.lineTo(point.x, point.y);
  });
  ctx.stroke();

  ctx.fillStyle = profile.color;
  points.forEach((point) => {
    ctx.beginPath();
    ctx.arc(point.x, point.y, 6, 0, Math.PI * 2);
    ctx.fill();
  });
}

function renderResult(profile, sourceLabel) {
  hnr.textContent = `${profile.hnr.toFixed(1)} dB`;
  hf.textContent = profile.hf.toFixed(2);
  badge.textContent = profile.badge;
  badge.style.color = profile.color;
  filename.textContent = sourceLabel;
  reportText.textContent = profile.report;
  drawChart(profile);
}

async function runAnalysis() {
  const selectedFile = file.files[0];
  if (!selectedFile) {
    const profile = profiles[sample.value];
    statusText.textContent = "데모 샘플 기준 리포트를 표시했습니다.";
    renderResult(profile, "데모 샘플 기준 분석");
    return;
  }

  const baseUrl = normalizeApiBaseUrl(apiBase.value);
  if (!baseUrl) {
    statusText.textContent = "FastAPI 서버 주소를 입력하세요.";
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile);

  button.disabled = true;
  button.textContent = "분석 중...";
  statusText.textContent = "서버로 파일을 업로드하고 음성 특징을 계산하는 중입니다.";

  try {
    const response = await fetch(`${baseUrl}/analyze`, {
      method: "POST",
      body: formData,
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      const detail = payload?.detail || `HTTP ${response.status}`;
      throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }

    renderResult(mapServerResult(payload), `선택 파일: ${payload.filename || selectedFile.name}`);
    statusText.textContent = "서버 분석 리포트 생성 완료.";
  } catch (error) {
    statusText.textContent = `분석 실패: ${error.message || "서버 연결 또는 파일 분석 중 문제가 발생했습니다."}`;
  } finally {
    button.disabled = false;
    button.textContent = "분석 리포트 생성";
  }
}

button.addEventListener("click", runAnalysis);
drawChart(profiles.human);
