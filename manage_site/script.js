async function loadStatus() {
    try {
        const res = await fetch("http://127.0.0.1:9000/status");
        const data = await res.json();
        document.getElementById("status").innerText =
            `服务器状态: ${data.status}, 启动时间: ${data.start_time}, 已运行: ${data.uptime_seconds} 秒`;
    } catch (err) {
        document.getElementById("status").innerText = "❌ 无法获取服务器状态";
        console.error("loadStatus error:", err);
    }
}
async function loadLogs() {
    try {
        const res = await fetch("http://127.0.0.1:9000/logs/admin");
        const data = await res.json();
        document.getElementById("logs").innerText = data.join("\n");
    } catch (err) {
        document.getElementById("logs").innerText = "❌ 无法获取日志";
        console.error("loadLogs error:", err);
    }
}
window.onload = function () {
    loadStatus();
    loadLogs();
    // 每隔 5 秒自动刷新日志
    setInterval(loadLogs, 5000);
};