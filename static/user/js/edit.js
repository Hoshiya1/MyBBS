
function upload() {
    var obj = document.getElementById('uploadavatar');
    obj.click();
}

function doupload() {
    var avatarform = document.getElementById("avatarform");
    var fd = new FormData(avatarform);
    var xhr = new XMLHttpRequest();
    xhr.open('post', '/user/upavatar/');
    xhr.send(fd);
    xhr.onreadystatechange = function () {
        if(xhr.readyState==4){
            if(xhr.status==200 || xhr.status==304) {
                var ret = JSON.parse(xhr.responseText);
                var obj = document.getElementById('avatar');
                obj.src = "/media/" + ret.avatar;
            }
        }
    }
}