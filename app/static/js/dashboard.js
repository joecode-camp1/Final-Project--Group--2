/* ============================================================
   AttendanceMS — REAL-TIME Dashboard JS (FINAL CLEAN VERSION)
   Chart.js + Live polling + Search + Controls + UI sync
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
  initAttendanceChart();
  initSearch();
  initNotificationToggle();
  initNavDate();
  initLiveUpdates();
  initRangeToggle();
});

let attendanceChart = null;
let currentMode = "week";
let pollInterval = null;


/* ================= CHART INIT ================= */

function initAttendanceChart() {
  const canvas = document.getElementById("attendanceChart");
  if (!canvas || typeof Chart === "undefined") return;

  const initial = window.ATTENDANCE_CHART_DATA || {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    values: [70, 80, 65, 90, 85, 60, 75],
  };

  const ctx = canvas.getContext("2d");

  const gradient = ctx.createLinearGradient(0, 0, 0, 300);
  gradient.addColorStop(0, "rgba(79, 141, 255, 0.35)");
  gradient.addColorStop(1, "rgba(79, 141, 255, 0)");

  attendanceChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: initial.labels,
      datasets: [{
        data: initial.values,
        borderColor: "#4f8dff",
        borderWidth: 2.5,
        tension: 0.4,
        fill: true,
        backgroundColor: gradient,
        pointRadius: 4,
        pointBackgroundColor: "#fff",
        pointBorderColor: "#4f8dff"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          grid: { display: false }
        },
        y: {
          min: 0,
          max: 100,
          ticks: {
            callback: v => v + "%"
          }
        }
      }
    }
  });
}


/* ================= 🔥 REAL-TIME LIVE UPDATES ================= */

function initLiveUpdates() {
  if (pollInterval) clearInterval(pollInterval);

  pollInterval = setInterval(() => {
    fetch(`/dashboard/data?mode=${currentMode}`)
      .then(res => res.json())
      .then(data => {
        if (!data || !attendanceChart) return;

        // update chart
        attendanceChart.data.labels = data.chart.labels;
        attendanceChart.data.datasets[0].data = data.chart.values;
        attendanceChart.update();

        // update counters safely
        updateCounters(data);

      })
      .catch(err => console.log("Live update error:", err));
  }, 10000);
}


/* ================= RANGE SWITCH (DAY/WEEK/MONTH) ================= */

function initRangeToggle() {
  const buttons = document.querySelectorAll(".toggle-btn");
  if (!buttons.length) return;

  buttons.forEach(btn => {
    btn.addEventListener("click", function () {

      buttons.forEach(b => b.classList.remove("active"));
      this.classList.add("active");

      currentMode = this.dataset.range || "week";

      fetch(`/dashboard/data?mode=${currentMode}`)
        .then(res => res.json())
        .then(data => {
          if (!data || !attendanceChart) return;

          attendanceChart.data.labels = data.chart.labels;
          attendanceChart.data.datasets[0].data = data.chart.values;
          attendanceChart.update();

          updateCounters(data);
        })
        .catch(err => console.log(err));
    });
  });
}


/* ================= COUNTERS ================= */

function updateCounters(data) {
  const totalEl = document.getElementById("totalRecords");
  const presentEl = document.getElementById("presentCount");
  const absentEl = document.getElementById("absentCount");

  if (totalEl) totalEl.textContent = data.total ?? 0;
  if (presentEl) presentEl.textContent = data.present ?? 0;
  if (absentEl) absentEl.textContent = data.absent ?? 0;
}


/* ================= SEARCH ================= */

function initSearch() {
  const form = document.querySelector(".search-form");
  const input = document.getElementById("searchInput");
  const results = document.getElementById("searchResults");

  if (!form || !input || !results) return;

  let debounce = null;
  let controller = null;

  input.addEventListener("input", () => {
    clearTimeout(debounce);

    const q = input.value.trim();
    if (!q) return close();

    debounce = setTimeout(() => run(q), 250);
  });

  function run(query) {
    if (controller) controller.abort();
    controller = new AbortController();

    fetch(`/search?query=${encodeURIComponent(query)}`, {
      signal: controller.signal
    })
      .then(res => res.json())
      .then(data => render(data.results || []))
      .catch(() => render([]));
  }

  function render(items) {
    results.innerHTML = "";

    if (!items.length) {
      results.innerHTML = `<div class="search-empty">No results</div>`;
    } else {
      items.forEach(i => {
        const a = document.createElement("a");
        a.href = i.href || "#";
        a.className = "search-item";
        a.textContent = i.label;
        results.appendChild(a);
      });
    }

    results.classList.add("open");
  }

  function close() {
    results.classList.remove("open");
    results.innerHTML = "";
  }
}


/* ================= NOTIFICATION ================= */

function initNotificationToggle() {
  const bell = document.querySelector(".notification-wrapper");
  if (!bell) return;

  bell.addEventListener("click", () => {
    document.querySelector(".activity-section")
      ?.scrollIntoView({ behavior: "smooth" });
  });
}


/* ================= NAV DATE ================= */

function initNavDate() {
  const nav = document.querySelector(".nav-right");
  if (!nav) return;

  if (document.getElementById("navDate")) return;

  const el = document.createElement("span");
  el.id = "navDate";
  el.className = "nav-date";

  const now = new Date();
  el.textContent = now.toDateString();

  nav.prepend(el);
}