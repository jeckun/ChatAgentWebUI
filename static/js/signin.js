var userLoggedIn = false;
var UserInf = {};

document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    const response = await fetch("/signin", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById("message").innerText = `Login succeeded!`;

        UserInf = data.user;
        setUserInf();

        // 清除登录信息
        document.getElementById('username').value = ""
        document.getElementById('password').value = ""
        
        // 界面调整
        userLoggedIn = true;
        hideContent('sign-in-content');
        showContent('user-inf-content');

        // 触发页面重新加载
        location.reload();

    } else {
        const errorMessage = await response.json(); // 获取错误消息文本
        document.getElementById("message").innerText = `Login failed! ${errorMessage.message}`;
        userLoggedIn = false;
        showContent('sign-in-content');
        hideContent('sign-up-content');
        hideContent('user-inf-content');
    }
});


document.getElementById("registerForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    var username = document.getElementById('registerUsername').value;
    var email = document.getElementById('registerEmail').value;
    var password = document.getElementById('registerPassword').value;

    const response = await fetch("/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&email=${encodeURIComponent(email)}`
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById("registerMessage").innerText = `Register succeeded!`;
        
        UserInf = data.user;
        setUserInf();

        // 清除登录信息
        document.getElementById('registerUsername').value = "";
        document.getElementById('registerPassword').value = "";
        document.getElementById('registerEmail').value = "";

        // 界面调整
        userLoggedIn = true;
        hideContent('sign-up-content');
        showContent('user-inf-content');

        // 触发页面重新加载
        location.reload();
    } else {
        const errorMessage = await response.json(); // 获取错误消息文本
        document.getElementById("registerMessage").innerText = `Register failed! ${errorMessage.message}`;
        userLoggedIn = false;
        hideContent('sign-in-content');
        showContent('sign-up-content');
        hideContent('user-inf-content');
    }
});

function checkLoginState() {
    // 检查用户登录状态，网页加载时调用
    var storedUserInf = localStorage.getItem('UserInf');
    if (storedUserInf) {
        UserInf = JSON.parse(storedUserInf);
        // 用户已登录，显示用户信息页面
        document.getElementById('name').innerText = UserInf.name;
        document.getElementById('email').innerText = UserInf.email;
        document.getElementById('key').value = UserInf.current_key;
        document.getElementById('proxy').value = UserInf.proxy_url;
        document.getElementById('model').value = UserInf.default_model;
        
        showContent('user-inf-content');
        hideContent('sign-in-content');
        hideContent('sign-up-content');
        disabled_user_input(false);
    }
}

function signUpShow() {
    // 点击按钮时切换到注册
    userLoggedIn = false;
    hideContent('sign-in-content');
    showContent('sign-up-content');
    hideContent('user-inf-content');
}

function signInShow() {
    // 点击按钮时切换到登录
    userLoggedIn = false;
    showContent('sign-in-content');
    hideContent('sign-up-content');
    hideContent('user-inf-content');
}

// 辅助函数用于显示内容
function showContent(contentId) {
    document.getElementById(contentId).classList.remove('hidden');
}

// 辅助函数用于隐藏内容
function hideContent(contentId) {
    document.getElementById(contentId).classList.add('hidden');
}

// 注销时清除本地用户信息
function userLogout() {

    const response = fetch("/signout", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `username=${encodeURIComponent(UserInf.name)}`
    });
    UserInf = {}

    localStorage.removeItem('UserInf');
    userLoggedIn = false;

    showContent('sign-in-content');
    hideContent('sign-up-content');
    hideContent('user-inf-content');

    // 触发页面重新加载
    location.reload();
}

// 保存用户信息
async function saveUserInf() {

    var key = document.getElementById('key').value;
    var proxy = document.getElementById('proxy').value;
    var model = document.getElementById('model').value;

    UserInf.current_key = key;
    UserInf.proxy_url = proxy;
    UserInf.default_model = model;

    setUserInf();

    const response = await fetch("/saveuserinf", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `username=${encodeURIComponent(UserInf.name)}&key=${encodeURIComponent(key)}&proxy=${encodeURIComponent(proxy)}&model=${encodeURIComponent(model)}`
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById("usermessage").innerText = `Save succeeded!`;
    }else {
        const errorMessage = await response.json();
        document.getElementById("usermessage").innerText = `Save failed! ${errorMessage.message}`;
    }

    // 保存完成，设置用户信息控件
    lockById('key');
    lockById('proxy');
    lockById('model');

    hideContent('save-user-inf');
    showContent('edit-user-inf');
    showContent('user-logout');
}

// 设置用户信息
function setUserInf() {
    document.getElementById('name').innerText = UserInf.name;
    document.getElementById('email').innerText = UserInf.email;
    document.getElementById('key').value = UserInf.current_key;
    document.getElementById('proxy').value = UserInf.proxy_url;
    document.getElementById('model').value = UserInf.default_model;

    localStorage.setItem('UserInf', JSON.stringify(UserInf));
}

// 编辑用户信息
function editUserInf() {
    unlockById('key');
    unlockById('proxy');
    unlockById('model');

    showContent('save-user-inf');
    hideContent('edit-user-inf');
    hideContent('user-logout');
}

function lockById(id) {
    var input = document.getElementById(id);
    input.setAttribute('readonly', 'readonly');
}

function unlockById(id) {
    var input = document.getElementById(id);
    input.removeAttribute('readonly');
}