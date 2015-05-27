 window.onscroll=function(){
        var a = document.documentElement.clientHeight;
        var b = document.documentElement.scrollTop==0? document.body.scrollTop : document.documentElement.scrollTop;
        var c = document.documentElement.scrollHeight;
        if(a+b==c)
            alert('a:'+a+'b:'+b+'c:'+c);
}