// chat.js 
// 处理用户与ChatGPT交互

// 获取状态栏和消息对话框的引用
const messageInput = document.getElementById('user_input');

window.globalMessageElement = null;

// 初始化 session
currentSession = {}
sessionId = 999999

// 发送消息到服务器
function sendUserMessage() {
    const message = messageInput.value;

    // 检查用户输入是否为空
    if (!message.trim()) {
        messageBox("User input is empty. Please enter a question.")
        return false;
    }
    // 检查是否已经登录
    if (isEmptyDict(UserInf)) {
        messageBox("Please log in before use.")
        return false
    }
    // 检查会话
    if (isEmptyDict(currentSession)) {
        currentSession[sessionId] = {
            'title': 'None',
            'user': UserInf.name,
            'password': UserInf.password,
            'proxy': UserInf.proxy_url,
            'apiKey': UserInf.current_key,
            'model': UserInf.default_model,
            'messages': [
                {"system": "You are a helpful assistant. You can help me by answering my questions. You can also ask me questions."},
                {'user': message}]
        };
    } else {
        currentSession[sessionId]['messages']=[{'user': message}];
    }
    addUserMessageUi(message ,'user');
    sendMessagetoChat(currentSession);
    return true;
}

// 收到服务器消息
function receiveServerMessage(serverMessage){
    const formattedMessage = formartHtml(serverMessage);
    addUserMessageUi(formattedMessage ,'assistant');
}

// 格式化反馈的消息
function formartHtml(response) {
    return response.replace(/\n/g, '<br>')
}

// 清除对话框，结束对话
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
