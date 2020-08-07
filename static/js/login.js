function checkUser(value) {
    if (value.length < 6 || value.length > 11) {
        document.getElementById('username').setAttribute('class','loginError');
        alert('请输入6~11位之间的用户名！')
    } else {
        document.getElementById('username').setAttribute('class','login');
        return 'ok'
    }
}
function checkPassword(value){
    if (value.length < 6 || value.length > 11) {
        document.getElementById('password').setAttribute('class','loginError');
        alert('请输入6~11位之间的密码！')
    } else {
        document.getElementById('password').setAttribute('class','login');
        return 'ok'
    }
}
function checkRe(box) {
    if (box.checked == true) {
        alert('本站已为你记住密码,三天免密登录！')
    } else {
        
    }  
}
function loginCheck() {
    var user = document.getElementById('username').value;
    var password = document.getElementById('username').value;
    if (checkUser(user) == 'ok' && checkPassword(password) == 'ok') {
        return true
    } else {
        return false
    }
}
function userTip() {
    document.getElementById('username').setAttribute('placeholder','用户名在6~11位之间！')
}
function passwordTip() {
    document.getElementById('password').setAttribute('placeholder','密码在6~11位之间！')
}