// chat.js 负责用户消息与ChatGPT消息交互后的 WebUI 页面更新

// 获取状态栏和消息对话框的引用
const messageInput = document.getElementById('user_input');

window.globalMessageElement = null;

// 发送消息到服务器
function sendUserMessage() {
    const message = messageInput.value;

    // 检查用户输入是否为空
    if (!message.trim()) {
        console.log("User input is empty. Please enter a question.");
        return false;
    }
    console.log(message)
    addMessage(message ,'user');
    sendMessage(message);
    messageInput.value = "";
    return true;
}

// 收到服务器消息
function receiveServerMessage(serverMessage){
    const formattedMessage = formartHtml(serverMessage);
    addMessage(formattedMessage ,'server');
}

// 格式化反馈的消息
function formartHtml(response) {
    return response.replace(/\n/g, '<br>')
}


// 在页面加载时动态设置消息栏的高度
window.addEventListener('DOMContentLoaded', function() {
    adjustMessageBoxHeight();
  });

// 在窗口大小改变时重新调整消息栏的高度
window.addEventListener('resize', function() {
adjustHeight('chatHistory', 127);
adjustHeight('messagelist', 169); // 填入其他div的id和对应的高度
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


// 添加消息到对话框
function addMessage(message, messageType) {
    const messageBox = document.getElementById('chatHistory');

    if (['$START.', '$END.'].includes(message)) {
        // 控制状态栏和输入框状态
        if (message === '$START.'){
            set_user_input(true)
        }else{
            set_user_input(false)
        }
        console.log(message);
        return;
    }

    // 持续更新来自服务器的消息
    if (window.globalMessageElement!==null && messageType==='server') {
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
    messageBox.appendChild(messageElement);
    window.globalMessageElement = messageType === 'user' ? null : messageElement;

}

function set_user_input(status) {
    console.log('disabled user input state: ', status)
    document.getElementById('user_input').disabled = status;
    document.getElementById('user_input_but').disabled = status;
    document.getElementById('user_clear_but').disabled = status;
}

// Function to clear the chat history
function clearChat() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/clear_chat', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('chatHistory').innerHTML = '';
        }
    };
    xhr.send();
}
