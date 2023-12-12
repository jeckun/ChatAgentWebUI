// ws.js 负责用户消息与ChatGPT消息交互

// WebSocket连接地址
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const host = window.location.host;
const wsEndpoint = `${protocol}//${host}/ws`;

let ws;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;
const reconnectDelay = 3000; // 毫秒

// 连接 WebSocket 的函数
function connectWebSocket() {
    ws = new WebSocket(wsEndpoint);

    // 添加连接成功的事件处理程序
    ws.addEventListener('open', (event) => {
        console.log('WebSocket连接已打开', event);
        // 重置尝试次数
        reconnectAttempts = 0;
    });

    // 添加连接关闭的事件处理程序
    ws.addEventListener('close', (event) => {
        console.log('WebSocket连接已关闭:', event);
        // 在连接关闭时重新连接，但限制尝试次数
        if (reconnectAttempts < maxReconnectAttempts) {
            reconnectAttempts++;
            console.log(`尝试重新连接，次数：${reconnectAttempts}`);
            setTimeout(connectWebSocket, reconnectDelay);
        } else {
            console.error('达到最大尝试次数，停止重新连接。');
        }
    });

    // 添加发生错误的事件处理程序
    ws.addEventListener('error', (error) => {
        console.error('WebSocket发生错误:', error);
    });

    // 收到服务器消息的事件处理程序
    ws.addEventListener('message', (event) => {
        receiveServerMessage(event.data);
    });
}

// 调用连接函数
connectWebSocket();

// 发送消息到服务器
function sendMessage(message) {
    // 检查 WebSocket 的 readyState，如果为 OPEN，则发送消息
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(message);
    } else {
        console.warn('WebSocket连接未打开，无法发送消息。');
        connectWebSocket();
    }
}
