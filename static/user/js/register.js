
// function check() {
//     regform = document.getElementById('regform');
//     var name = regform.name.value;
//     if(name.indexOf('@') != -1) {
//         var obj = document.getElementById('message2');
//         obj.innerHTML = "用户名不合法";
//     }
//     else {
//         var pwd1 = regform.password1.value;
//         var pwd2 = regform.password2.value;
//         if(pwd1 != pwd2) {
//             var obj = document.getElementById('message3');
//             obj.innerHTML = "两次输入的密码不一致";
//         }
//         else {
//             var obj = document.getElementById('doreg');
//             obj.click();
//         }
//     }
// }

$("img.captcha").click(function(){   //更新验证码图片ajax
    console.log('click');
    $.getJSON("/captcha/refresh/",function(data){
        $("img.captcha").attr("src",data.image_url);
        $("#id_captcha_0").attr("value",data.key);
    });
});