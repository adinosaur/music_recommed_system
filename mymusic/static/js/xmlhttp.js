/*
 * 2015年5月17日
 * 使用ajax异步发送请求
 */

//全局变量xmlhttp
var xmlhttp;
    
function createxmlhttp(){
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
}

function addURLParam(url, name, value){
    url += (url.indexOf("?") == -1 ? "?" : "&")
    url += encodeURIComponent(name) + "=" + encodeURIComponent(value);
    return url;
}

function send_request(method, url, value){
    createxmlhttp();
    if (method == "post"){
        xmlhttp.open("post", url, true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send(value);
    }
    else{
        xmlhttp.open("get", url, true);
        xmlhttp.send();
    }
}

function send_get_request(url){
    send_request("get", url);
}

function send_post_request(url, value){
    send_request("post", url, value);
}

// mymusic.templates.play.html文件
function send_playmusic_request(value){
    url = "/mymusic/playmusic";
    url = addURLParam(url, "id", value);
    send_get_request(url);
}

function send_comment(){ 
    var comment = document.getElementById("comment").value;
    if (comment != ""){
        url = "/mymusic/comment";
        var songId = document.getElementById("song_id").value;
        var queryString = "comment=" + comment +"&song_id=" + songId;
        send_post_request(url, queryString);
        reply(comment);
        return false;
    }
}

function favourComment(commentID){ 
    url = "/mymusic/favour-comment";
    url = addURLParam(url, "id", commentID);
    send_get_request(url);
    return false;
}

function cancelFavourComment(commentID){ 
    createxmlhttp();
    url = "/mymusic/cancel-favour-comment";
    url = addURLParam(url, "id", commentID);
    send_get_request(url);
    return false;
}

// accounts.templates.home.html文件
function follow(uid){ 
    url = "/social-music/follow/";
    value = "uid=" + uid
    send_post_request(url, value);
    return false;
}

function unfollow(uid){
    url = "/social-music/unfollow/";
    value = "uid=" + uid
    send_post_request(url, value);
    return false;
}


function isFollowTab(el){
    var oldtotal = parseInt(el.getAttribute('total'));
    var text =el.innerHTML;
    var newtotal;
    if(text == ('贊('+oldtotal+')')){ 
        newtotal = oldtotal+1;
        favourComment(el.getAttribute('id'));
        el.innerHTML='取消贊('+newtotal+')';
    }
    else{
        newtotal = oldtotal-1;
        cancelFavourComment(el.getAttribute('id'));
        el.innerHTML='贊('+newtotal+')';
    }
    el.setAttribute('total',newtotal);
}
