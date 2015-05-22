/*
 * 处理点赞功能的js代码
 * 2015年5月17日
 */
function praisetab(el){
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

function load(){
    var list = document.getElementById('comment-List');
    var lis = list.children;
    for(var i=0; i<lis.length;i++){
        lis[i].onclick = function (e){
            var el =e.srcElement;
            //document.write(el.className);
            switch(el.className){
                case 'glyphicon glyphicon-thumbs-up pull-right':
                    praisetab(el);
                    break;
            }
        }
    }
}

window.onload = function(){
    var textArea = document.getElementById('comment');
    var tj_button = document.getElementById('button')
    var word = document.getElementById('word');
    textArea.onkeyup=function(){
        var val = this.value;
        var len = val.length;
        if(len<=0||len>140){
            tj_button.disabled='disabled';
        }
        else
            tj_button.disabled='';
        word.innerHTML=len + '/140';
    }
    tj_button.onclick = function(){
            send_comment();
            load();
            textArea.value='';
            word.innerHTML='0/140';
    }
}

function share(){
    var textArea = document.getElementById('share_comment');
    var tj_button = document.getElementById('share_button')
    var word = document.getElementById('share_word');

    textArea.onfocus = function(){
        this.value = this.value == '说点什么吧' ? '' : this.value;
        textArea.onkeyup();
    }
    textArea.onblur = function(){
        this.value=this.value==''?'说点什么吧':this.value;
    }
    textArea.onkeyup=function(){
        var val = this.value;
        var len = val.length;
        if(len<=0||len>140){
            tj_button.disabled='disabled';
        }
        else
            tj_button.disabled='';
        word.innerHTML=len + '/140';
    }
}