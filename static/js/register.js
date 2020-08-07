// 用户名验证
function checkUser(value) {
    if (value.length < 6 || value.length > 11) {
        document.getElementById('user').setAttribute('class','loginError');
        alert('请输入6~11位之间的注册用户名！')
    } else {
        document.getElementById('user').setAttribute('class','login');
        return true
    }
}
// 邮箱验证
function checkEmail(value) {
    var myReg = /^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/;
    if (myReg.test(value)==false) {
        document.getElementById('email').setAttribute('class','loginError');
        alert('请输入正确的邮箱格式！')
    } else {
        document.getElementById('email').setAttribute('class','login');
        return true
    }
}
// 手机号验证
function checkPhone(value) {
    var myReg = /^1[3|4|5|6|7|8|9][0-9]{9}$/;
    if (myReg.test(value)==false) {
        document.getElementById('phone').setAttribute('class','loginError');
        alert('请输入正确的手机号！');
    }else{
        document.getElementById('phone').setAttribute('class','login');
        return true
    }    
}
// 密码检验
function checkPassword(value){
    if (value.length < 6 || value.length > 11) {
        document.getElementById('password').setAttribute('class','loginError');
        alert('请输入6~11位之间的密码！')
    } else {
        document.getElementById('password').setAttribute('class','login');
        return true
    }
}
// 密码确认校验
function checkRePassword(value){
    var pass1 = document.getElementById('password').value
    if (pass1 != value) {
        document.getElementById('passwordRepeat').setAttribute('class','loginError');
        alert('前后两次密码不一致，请重新输入确认密码！')
    } else {
        document.getElementById('passwordRepeat').setAttribute('class','login');
        return true
    }
}
function checkRe(box) {
    if (box.checked == false) {
        alert('请同意本站协议！')
    } else {
        return true
    }  
}
function  registerCheck() {
    var user = document.getElementById('user').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;
    var password = document.getElementById('password').value;
    var repassword = document.getElementById('passwordRepeat').value;
    var box = document.getElementById('reader-me1')
    if (checkUser(user) && checkEmail(email) && checkPhone(phone) && checkPassword(password) && checkRePassword(repassword) && checkRe(box)) {
        return true
    } else {
        return false
    }
}
function userTip() {
    document.getElementById('user').setAttribute('placeholder','注册用户名在6~11位之间！')
}
function passwordTip() {
    document.getElementById('password').setAttribute('placeholder','密码在6~11位之间！')
}