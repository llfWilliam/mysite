function q(id) { return document.getElementById(id); }    //定义了一个函数，省的写长的要死的getElement。。。。

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

// 当前日志类型：admin或debug
let currentLogType = "admin";

async function loadLogs() {
  try {
    const logEndpoint = currentLogType === "admin" ? "/logs/admin" : "/logs/debug";
    const res = await fetch(logEndpoint);
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();
    
    // 根据日志类型处理显示方式
    if (currentLogType === "admin") {
      // 管理日志直接显示
      q("logs").innerText = Array.isArray(data) ? data.join("\n") : JSON.stringify(data);
    } else {
      // 调试日志需要格式化JSON
      q("logs").innerText = Array.isArray(data) 
        ? data.map(line => {
            try {
              const parsed = JSON.parse(line);
              return JSON.stringify(parsed, null, 2);
            } catch {
              return line;
            }
          }).join("\n\n")
        : JSON.stringify(data);
    }
  } catch (err) {
    console.error("loadLogs error:", err);
    q("logs").innerText = "❌ 无法获取日志：" + err.message;
  }
}

// 切换日志类型
function switchLogType(type) {
  currentLogType = type;
  q("log-type-indicator").innerText = type === "admin" ? "管理日志" : "调试日志";
  loadLogs();
}

document.addEventListener("DOMContentLoaded", () => {
  loadStatus();
  loadLogs();
  setInterval(loadLogs, 5000);
});