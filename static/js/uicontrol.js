// 加载页面初始化设置
// 并动态控制页面控件

// 页面加载
window.addEventListener('DOMContentLoaded', function() {
    disabled_user_input(true);
    // 登录检查
    checkLoginState();
    // 页面调整
    adjustHeight('chatHistory', 15);
    adjustHeight('messagelist', 60);
  });

// main-body 禁止滚动
document.getElementById("main-body").addEventListener("mouseenter", function (e) {
    document.body.style.overflow = 'hidden';
});

// 在窗口大小改变时重新调整消息栏的高度
window.addEventListener('resize', function() {
    adjustHeight('chatHistory', 15);
    adjustHeight('messagelist', 60); // 填入其他div的id和对应的高度
});

// 动态设置高度
function adjustHeight(elementId, offset) {
    const element = document.getElementById(elementId);
    const windowHeight = window.innerHeight;
    const navbarHeight = document.querySelector('.navbar').offsetHeight;
    const footerHeight = document.querySelector('.fixed-bottom').offsetHeight;
    const newHeight = windowHeight - navbarHeight - footerHeight - offset;
    element.style.height = `${newHeight}px`;
}

// 设置用户输入框状态
function disabled_user_input(status) {
    // status = true :表示禁止使用
    // status = false :表示允许使用
    document.getElementById('user_input').disabled = status;
    document.getElementById('user_input_but').disabled = status;
    document.getElementById('user_clear_but').disabled = status;
}

// 添加消息到对话框
function addUserMessageUi(message, messageType) {
    const chatBox = document.getElementById('chatHistory');

    if (['$START.', '$END.', 'ping'].includes(message)) {
        // 控制状态栏和输入框状态
        if (message === '$START.'){
            disabled_user_input(true);
        }else{
            disabled_user_input(false);
        }
        if (message === 'ping') {
            return;
        }
        console.log(message);
        return;
    }

    // 持续更新来自服务器的消息
    if (window.globalMessageElement!==null && messageType==='assistant') {
        messageHtml = formartHtml(message);
        const childElements = window.globalMessageElement.getElementsByClassName('message-content');
        childElements[0].innerHTML += messageHtml;
        return ;
    }

    // 创建新的服务器消息
    const messageElement = document.createElement('div');
    messageElement.className = messageType === 'user' ? 'user-message' : 'server-message';

    // 创建新的服务器消息头像
    const avatarContainer = document.createElement('div');
    avatarContainer.className = 'avatar-container';
    // 设置服务器消息头像
    const avatar = document.createElement('img');
    avatar.className = 'avatar';
    var discordlogourl = 'https://pub-ea398b99a11f43da9bf5018ccba88f05.r2.dev/discord-logo.webp';
    var chatgptlogourl = 'https://pub-ea398b99a11f43da9bf5018ccba88f05.r2.dev/ChatGPT-logo.webp';
    avatar.src = messageType === 'user' ? discordlogourl : chatgptlogourl;
    
    avatarContainer.appendChild(avatar);

    // 创建新的服务器消息内容对象
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageHtml = formartHtml(message);
    messageContent.innerHTML = messageHtml;

    // 将头像容器和消息内容容器追加到消息元素
    messageElement.appendChild(avatarContainer);
    messageElement.appendChild(messageContent);

    // 将消息元素追加到消息对话框
    chatBox.appendChild(messageElement);
    window.globalMessageElement = messageType === 'user' ? null : messageElement;

    messageInput.value = "";
}