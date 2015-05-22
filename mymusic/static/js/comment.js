/*
 * 处理评论功能的js代码
 * 2015年5月18日
 */
function formateDate(date) {
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    var d = date.getDate();
    var h = date.getHours();
    var mi = date.getMinutes();
    m = m > 9 ? m : '0' + m;
    return y + '日' + m + '月' + d + '日 ' + h + ':' + mi;
}

/*function load(){
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
}*/

function reply(comment) {
    var commentList = document.getElementById('comment-List');  
    var textArea = document.getElementById('comment');
    var commentBox = document.createElement('li');
    commentBox.className = 'media';
    commentBox.innerHTML =
        '<div class="media-left">' +
        '<a href="">' +
            '<img class="media-object" src="{{ MEDIA_URL }}heads/{{head}}" alt="..."></a>' +
        '</div>' +
        '<div class="media-body">' + 
            '<a herf="">{{user}}</a>:' + comment +
            '<div>' +
            formateDate(new Date()) +
            '<a  calss="praise"   href="javascript:void(0);"><span class="glyphicon glyphicon-thumbs-up pull-right" id="{{comment.id}}" total="0" aria-hidden="true">贊(0)</span></a>'+
            '</div>' +
        '</div>'
    commentList.appendChild(commentBox);
}
