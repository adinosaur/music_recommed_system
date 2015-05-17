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
