// login.js
document.addEventListener("DOMContentLoaded", function () {
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const loginBtn = document.getElementById("login-btn");
    const registerBtn = document.getElementById("register-btn");

    // 注册事件
    registerBtn.addEventListener("click", async function () {
        const res = await fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
                username: usernameInput.value,
                password: passwordInput.value
            })
        });
        const data = await res.json();
        alert(data.message); // 提示注册结果
    });

    // 登录事件
    loginBtn.addEventListener("click", async function () {
        const res = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
                username: usernameInput.value,
                password: passwordInput.value
            })
        });
        const data = await res.json();
        alert(data.message); // 提示登录结果
        if (data.success) {
            // 登录成功跳转到 index.html
            window.location.href = "index.html";
        }
    });
});