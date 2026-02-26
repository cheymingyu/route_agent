const state = {
  sessionId: null,
};

const el = {
  apiBase: document.getElementById("apiBase"),
  query: document.getElementById("query"),
  startBtn: document.getElementById("startBtn"),
  nextBtn: document.getElementById("nextBtn"),
  status: document.getElementById("status"),
  output: document.getElementById("output"),
  meta: document.getElementById("meta"),
};

function setStatus(text) {
  el.status.textContent = text;
}

function renderResult(data) {
  const restaurant = data.selected_restaurant || {};

  el.output.textContent = data.final_output || "응답 없음";
  el.output.classList.remove("muted");

  const x = restaurant.x ?? "-";
  const y = restaurant.y ?? "-";
  el.meta.innerHTML = `
    <div><dt>이름</dt><dd>${restaurant.name || "-"}</dd></div>
    <div><dt>정거장</dt><dd>${restaurant.nearest_station_name || "-"}</dd></div>
    <div><dt>도보(분)</dt><dd>${restaurant.estimated_walk_min ?? "-"}</dd></div>
    <div><dt>좌표</dt><dd>${x}, ${y}</dd></div>
    <div><dt>session_id</dt><dd class="mono">${state.sessionId || "-"}</dd></div>
  `;
}

async function postJson(path, payload) {
  const base = el.apiBase.value.trim().replace(/\/$/, "");
  const res = await fetch(`${base}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${text}`);
  }

  return res.json();
}

el.startBtn.addEventListener("click", async () => {
  try {
    el.startBtn.disabled = true;
    el.nextBtn.disabled = true;
    setStatus("추천 생성 중...");

    const data = await postJson("/chat/start", {
      text: el.query.value.trim(),
    });

    state.sessionId = data.session_id;
    renderResult(data);
    el.nextBtn.disabled = !state.sessionId;
    setStatus("완료: 다른 후보 보기를 눌러 재추천 테스트 가능");
  } catch (err) {
    setStatus(`오류: ${err.message}`);
  } finally {
    el.startBtn.disabled = false;
  }
});

el.nextBtn.addEventListener("click", async () => {
  if (!state.sessionId) {
    setStatus("먼저 추천 시작을 눌러 주세요.");
    return;
  }

  try {
    el.nextBtn.disabled = true;
    setStatus("다음 후보 생성 중...");

    const data = await postJson("/chat/next", {
      session_id: state.sessionId,
    });

    renderResult(data);
    if (data.exhausted) {
      setStatus("후보를 모두 소진했습니다.");
      el.nextBtn.disabled = true;
      return;
    }

    setStatus("완료: 다음 후보로 갱신됨");
    el.nextBtn.disabled = false;
  } catch (err) {
    setStatus(`오류: ${err.message}`);
    el.nextBtn.disabled = false;
  }
});
