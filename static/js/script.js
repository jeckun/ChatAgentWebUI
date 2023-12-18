// // 获取所有带有下拉菜单的链接
// var dropdowns = document.querySelectorAll('.dropdown-toggle');

// // 遍历每个下拉菜单链接
// dropdowns.forEach(function(dropdown) {
// // 监听点击事件
// dropdown.addEventListener('click', function(event) {
//     event.preventDefault();
//     event.stopPropagation();
    
//     // 切换下拉菜单的显示状态
//     var dropdownMenu = dropdown.nextElementSibling;
//     dropdownMenu.classList.toggle('show');
// });
// });

// // 监听文档的点击事件，隐藏下拉菜单
// document.addEventListener('click', function(event) {
// var target = event.target;

// // 如果点击的不是下拉菜单链接或下拉菜单本身，则隐藏下拉菜单
// if (!target.classList.contains('dropdown-toggle') && !target.classList.contains('dropdown-menu')) {
//     dropdowns.forEach(function(dropdown) {
//     var dropdownMenu = dropdown.nextElementSibling;
//     dropdownMenu.classList.remove('show');
//     });
// }
// });