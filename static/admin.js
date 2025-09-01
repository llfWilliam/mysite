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

// 用户管理功能
async function loadUsers() {
  try {
    const res = await fetch("/admin/list");
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();
    
    if (data.success && Array.isArray(data.users)) {
      // 创建表格显示用户列表
      let html = '<table>';
      html += '<tr><th>用户名</th><th>管理员状态</th></tr>';
      
      data.users.forEach(user => {
        const isAdmin = user.is_admin === 1 || user.is_admin === true;
        html += `<tr>
          <td>${user.username}</td>
          <td>${isAdmin ? '✅ 是' : '❌ 否'}</td>
        </tr>`;
      });
      
      html += '</table>';
      q("users-list").innerHTML = html;
    } else {
      q("users-list").innerText = "获取用户列表失败: " + (data.message || "未知错误");
    }
  } catch (err) {
    console.error("loadUsers error:", err);
    q("users-list").innerText = "❌ 无法获取用户列表：" + err.message;
  }
}

async function grantAdmin() {
  const username = q("username-input").value.trim();
  if (!username) {
    alert("请输入用户名");
    return;
  }
  
  try {
    const res = await fetch("/admin/grant", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });
    
    const data = await res.json();
    alert(data.message || "操作完成");
    if (data.success) {
      loadUsers(); // 刷新用户列表
    }
  } catch (err) {
    console.error("grantAdmin error:", err);
    alert("授予管理员权限失败: " + err.message);
  }
}

async function revokeAdmin() {
  const username = q("username-input").value.trim();
  if (!username) {
    alert("请输入用户名");
    return;
  }
  
  try {
    const res = await fetch("/admin/revoke", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });
    
    const data = await res.json();
    alert(data.message || "操作完成");
    if (data.success) {
      loadUsers(); // 刷新用户列表
    }
  } catch (err) {
    console.error("revokeAdmin error:", err);
    alert("撤销管理员权限失败: " + err.message);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadStatus();
  loadLogs();
  loadUsers();
  // 移除自动刷新逻辑，只保留手动刷新
});