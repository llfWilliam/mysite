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

async function loadLogs() {
  try {
    const res = await fetch("/logs/admin");//res 是一个 Response 对象，里面有 status、ok、json() 等属性和方法。
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();          // 你的后端这里返回的是一个字符串数组
    q("logs").innerText = Array.isArray(data) ? data.join("\n") : JSON.stringify(data);//Array.isArray(data) → 判断 data 是否为数组：
//如果是数组，就 join("\n")，拼成一整个多行字符串，展示在页面里。
//如果不是数组，就直接 JSON.stringify(data)，转成 JSON 字符串显示。
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