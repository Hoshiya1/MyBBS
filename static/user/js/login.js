
$("img.captcha").click(function(){   //更新验证码图片ajax
    console.log('click');
    $.getJSON("/captcha/refresh/",function(data){
        $("img.captcha").attr("src",data.image_url);
        $("#id_captcha_0").attr("value",data.key);
    });
});
