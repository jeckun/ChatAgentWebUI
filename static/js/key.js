// 从浏览器 localStorage 中获取 API Key
function getApiKey() {
  var storedApiKey = localStorage.getItem('openai_api_key');

  if (storedApiKey) {
    // 解析 API Key 对象
    var apiKeyObject = JSON.parse(storedApiKey);
    // 检查 API Key 是否过期
    if (apiKeyObject.expiration > new Date().getTime()) {
      // API Key 仍然有效，使用 apiKeyObject.key
      return apiKeyObject.key;
    } else {
      // API Key 已过期，清除保存的内容
      localStorage.removeItem('openai_api_key');
      return ''
    }
  }
}

$(document).ready(function () {
  var setting = $('#settingItem');

  // 点击设置图标时触发事件
  setting.click(function () {
    // 从 localStorage 中获取 API Key
    apiKey = getApiKey();
    const apiKeyInput = document.getElementById('apiKeyInput');
    apiKeyInput.text = apiKey;
    apiKeyInput.value = apiKey;
    apiKeyInput.type = 'password'
    // 弹出模态框
    $('#apiKeyModal').modal('show');
  });

  // 点击模态框中的保存按钮时触发事件
  $('#saveApiKeyBtn').click(function () {
    // 获取用户输入的 API Key
    var apiKey = $('#apiKeyInput').val();
    console.log("OpenAi API Key : "+apiKey)

    // 设置 API Key 到 localStorage，并记录保存时间
    var apiKeyObject = {
      key: apiKey,
      expiration: new Date().getTime() + 7 * 24 * 60 * 60 * 1000, // 设置有效期为7天
    };

    // 将 API Key 对象保存到 localStorage
    localStorage.setItem('openai_api_key', JSON.stringify(apiKeyObject));

    // 关闭模态框
    $('#apiKeyModal').modal('hide');
    
    // 刷新当前页面
    location.reload();
  });
});

// 将 api key 发送到服务端用于聊天对话
function setOpenAiApiKey(api_key) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/set_key', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            console.log("response:"+response.server_response);
            statusBar.textContent = response.server_response;
        }
    };
    // 将数据转换为 JSON 字符串
    var data = JSON.stringify({ 'openai_api_key': api_key });
    xhr.send(data);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 定义一个从浏览器获取 API Key异步函数
async function init() {
    apiKey = getApiKey();
    console.log(apiKey)
    if (apiKey) {
        // setOpenAiApiKey(apiKey);
        // 使用 await 需要在 async 函数内部
        await sleep(2000);  // 暂停 2 秒
        statusBar.textContent = 'Please enter your question.';
    }
}

// 页面加载时调用异步函数
$(document).ready(function () {
    init();
});