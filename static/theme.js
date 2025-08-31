// theme.js - 主题切换功能

// 保存用户主题选择到本地存储
function setTheme(themeName) {
    // 更新样式表链接
    document.getElementById('theme-link').href = themeName;
    
    // 保存用户选择到本地存储
    localStorage.setItem('theme', themeName);
}

// 页面加载时检查并应用保存的主题
document.addEventListener('DOMContentLoaded', () => {
    // 从本地存储获取保存的主题
    const savedTheme = localStorage.getItem('theme');
    
    // 如果有保存的主题，则应用它
    if (savedTheme) {
        document.getElementById('theme-link').href = savedTheme;
    }
});