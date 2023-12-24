// toast.js

function messageBox(message, type = 'warning') {
    // 获取 Toast 元素
    var myToast = document.getElementById('myToast');

    // 更新 Toast 的消息和类型
    myToast.querySelector('.toast-body').innerText = message;
    updateToastType(myToast, type);

    // 利用 Bootstrap 的 Toast JS 方法显示 Toast
    var toast = new bootstrap.Toast(myToast);
    toast.show();
}

// 更新 Toast 类型
function updateToastType(toastElement, type) {
    var alertHeader = toastElement.querySelector('.toast-header');
    var alertIcon = alertHeader.querySelector('img');

    // 根据类型更新图标和样式
    switch (type) {
        case 'success':
            alertIcon.src = 'success-icon.png';
            alertHeader.classList.remove('bg-warning');
            alertHeader.classList.add('bg-success', 'text-white');
            break;
        case 'error':
            alertIcon.src = 'error-icon.png';
            alertHeader.classList.remove('bg-warning');
            alertHeader.classList.add('bg-danger', 'text-white');
            break;
        // 默认为警告类型
        case 'warning':
        default:
            alertIcon.src = 'static/img/exclamation-triangle-fill.svg';
            alertHeader.classList.remove('bg-success', 'bg-danger', 'text-white');
            alertHeader.classList.add('bg-warning');
            break;
    }
}

// 初始化 Toast 容器
function initializeToastContainer() {
    var toastContainer = document.createElement('div');
    toastContainer.classList.add('toast-container', 'position-fixed', 'top-0', 'end-0', 'p-3');
    toastContainer.style.zIndex = '9999';

    // 添加 hide 类，使 Toast 默认隐藏
    var toastElement = `
    <div class="toast-container position-static">
        <div id="myToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="5000" data-bs-autohide="true">
            <div class="toast-header">
                <img src="#" class="rounded mr-2" alt="Warning Icon" width="20" height="20">
                <strong class="mr-auto">警告</strong>
                <button type="button" class="btn-close mb-1 ms-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                This is a warning message!
            </div>
        </div>
    </div>
    `;

    toastContainer.innerHTML = toastElement;

    // 将 Toast 容器添加到 body 中
    document.body.appendChild(toastContainer);
}

// 调用初始化函数
initializeToastContainer();
