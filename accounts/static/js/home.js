function change (userID) {
    var focus = document.getElementById('focus');
    var text =focus.innerHTML;
    if(text == '<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>关注')
    {
     	focus.innerHTML='<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>取消关注';
     	follow(userID);
    }
    else{ 
    	focus.innerHTML='<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>关注';
    	unfollow(userID);
    }
  }