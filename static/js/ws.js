// ws.js 负责用户消息与ChatGPT消息交互

// WebSocket连接地址
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const host = window.location.host;
const wsEndpoint = `${protocol}//${host}/ws`;

const ws = new WebSocket(wsEndpoint);

ws.onopen = function (event) {
    console.log("WebSocket connected.")
};

ws.onclose = function (event){
    console.log("WebSocket closed.")
};

// 收到服务器消息
ws.onmessage = function (event) {
    receiveServerMessage(event.data);
};

// 发送消息到服务器
function sendMessage(message) {
    ws.send(message);
};
