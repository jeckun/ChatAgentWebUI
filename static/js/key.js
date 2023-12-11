document.addEventListener('DOMContentLoaded', function () {
  var setting = document.getElementById('settingItem');
  var apiKeyModal = document.getElementById('apiKeyModal');
  var apiKeyInput = document.getElementById('apiKeyInput');
  var apiProxyInput = document.getElementById('apiproxyInput');
  var saveApiKeyBtn = document.getElementById('saveApiKeyBtn');
  
  // 添加点击设置图标时触发的事件
  setting.addEventListener('click', function () {
      // 从 localStorage 中获取 API Key
      var cache = getApiKey();
      // console.log('setting click get stored: ',cache);
      apiKeyInput.value = cache.key;
      apiProxyInput.value = cache.proxy;
      apiKeyInput.type = 'text';
      apiProxyInput.type = 'text';
      // 弹出模态框
      apiKeyModal.classList.add('show');
      apiKeyModal.style.display = 'block';
  });

  // 添加点击模态框中的保存按钮时触发的事件
  saveApiKeyBtn.addEventListener('click', function () {
      // 获取用户输入的 API Key
      var apiKey = apiKeyInput.value;
      var apiProxy = apiProxyInput.value;

      // 设置 API Key 到 localStorage，并记录保存时间
      if (apiKey) {
        var apiKeyObject = {
            key: apiKey,
            expiration: new Date().getTime() + 7 * 24 * 60 * 60 * 1000, // 设置有效期为7天
        };
        localStorage.setItem('openai_api_key', JSON.stringify(apiKeyObject));
        setOpenAiApiKey({'key': apiKey})
      }

      if (apiProxy) {
          var apiProxyObject = {
            proxy: apiProxy,
            expiration: new Date().getTime() + 7 * 24 * 60 * 60 * 1000, // 设置有效期为7天
        };
        localStorage.setItem('openai_api_proxy', JSON.stringify(apiProxyObject));
        setOpenAiApiKey({'proxy': apiProxy})
      }

      // 关闭模态框
      apiKeyModal.classList.remove('show');
      apiKeyModal.style.display = 'none';

      // 刷新当前页面
      location.reload();
  });

  // 添加点击模态框外围区域或关闭按钮时关闭模态框
  apiKeyModal.addEventListener('click', function (event) {
      if (event.target === apiKeyModal) {
          // console.log('点击模态框外围')
          apiKeyModal.classList.remove('show');
          apiKeyModal.style.display = 'none';
      }
  });

  // 添加点击取消按钮时关闭模态框
  var cancelBtn = document.getElementById('cancelBtn');
  cancelBtn.addEventListener('click', function () {
    // console.log('点击关闭按钮')
    apiKeyModal.classList.remove('show');
    apiKeyModal.style.display = 'none';
  });

  // 点击关闭按钮
  var closeBtn = document.getElementById('closeBtn');
  closeBtn.addEventListener('click', function () {
    // console.log('点击模态框关闭图标')
    apiKeyModal.classList.remove('show');
    apiKeyModal.style.display = 'none';
  })
});

// 将 api key 发送到服务端用于聊天对话
function setOpenAiApiKey(apiObject) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/set_key', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
          var response = JSON.parse(xhr.responseText);
          // console.log("response:"+response.server_response);
          statusBar.textContent = response.server_response;
      }
  };

  // 将数据转换为 JSON 字符串
  var data = JSON.stringify({
    'openai_api_key': apiObject['key'],
    'openai_api_proxy': apiObject['proxy']
   });
  // console.log('send to server, ', data)
  xhr.send(data);
}

// 从浏览器 localStorage 中获取 API Key
function getApiKey() {
  var storedApiKey = localStorage.getItem('openai_api_key');
  var storedApiProxy = localStorage.getItem('openai_api_proxy');

  // console.log('get_cache_set:', storedApiKey, storedApiProxy);

  if (storedApiKey) {
      // 解析 API Key 对象
      var apiKeyObject = JSON.parse(storedApiKey);
      var apiProxyObject = JSON.parse(storedApiProxy);
      // 检查 API Key 是否过期
      if (apiKeyObject.expiration > new Date().getTime()) {
          // API Key 仍然有效，使用 apiKeyObject.key
          return {'proxy': apiProxyObject['proxy'], 'key': apiKeyObject['key'] };
      } else {
          // API Key 已过期，清除保存的内容
          localStorage.removeItem('openai_api_key');
          return { 'key': '', 'proxy': '' };
      }
  }

  return { apiKey: '', apiProxy: '' }; // 如果没有存储的 API Key，则返回空字符串
}


// 切换密码框是否可见
function toggleProxyInputVisibility() {
  var apiproxyInput = document.getElementById('apiproxyInput');
  apiproxyInput.type = apiproxyInput.type === 'password' ? 'text' : 'password';
  var showOpenAiApiProxy = document.getElementById('basic-addon1');
  showOpenAiApiProxy.style.backgroundColor = showOpenAiApiProxy.style.backgroundColor === 'white' ? '#e9ecef' : 'white';
}

function toggleKeyInputVisibility() {
  var apiKeyInput = document.getElementById('apiKeyInput');
  apiKeyInput.type = apiKeyInput.type === 'password' ? 'text' : 'password';
  var showOpenAiApiKey = document.getElementById('basic-addon2');
  showOpenAiApiKey.style.backgroundColor = showOpenAiApiKey.style.backgroundColor === 'white' ? '#e9ecef' : 'white';
}
