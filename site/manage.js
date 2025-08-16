function q(id) { return document.getElementById(id); }

async function loadStatus() {
  try {
    const res = await fetch("/status");
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();
    q("status").innerText =
      `服务器状态: ${data.status}, 启动时间: ${data.start_time}, 已运行: ${data.uptime_seconds} 秒`;
  } catch (err) {
    console.error("loadStatus error:", err);
    q("status").innerText = "❌ 无法获取服务器状态：" + err.message;
  }
}

async function loadLogs() {
  try {
    const res = await fetch("/logs/admin");
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();          // 你的后端这里返回的是一个字符串数组
    q("logs").innerText = Array.isArray(data) ? data.join("\n") : JSON.stringify(data);
  } catch (err) {
    console.error("loadLogs error:", err);
    q("logs").innerText = "❌ 无法获取日志：" + err.message;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadStatus();
  loadLogs();
  setInterval(loadLogs, 5000);
});