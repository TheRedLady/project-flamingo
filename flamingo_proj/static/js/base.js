$(function () {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
});


makePost = function(data) {
  return new Post(data['id'], data['url'], data['posted_by'], data['content'],
                  data['created'], data['share'], data['like_count'], data['liked']);
}

getId = function () {
    var loc = String(window.location).split("/");
    var id = loc[loc.length - 2];
    return id;
}

function Post(id, url, postedBy, content, created, share, likes, liked) {
    var self = this;
    self.id = id;
    self.url = url;
    self.posted_by = postedBy;
    self.content = content;
    self.created = created;
    self.likes = ko.observable(likes);
    self.liked = ko.observable(liked);

    self.likeUnlike = function() {
      url = "/api/posts/" + self.id + "/like/";
      method = "POST";
      if(self.liked()){
        method = "DELETE";
        self.likes(self.likes() - 1);
      }
      else{
        self.likes(self.likes() + 1);
      }
      $.ajax({
        url: url,
        method: method
      }).done(function(data) {
        self.liked(data['liked']);  
      });
    };

    if (share == null) {
      self.is_shared = false;
      self.share = null;
    }
    else {
      self.is_shared = true;
      self.share = share;
    }

    self.removePost = function() {
      $.ajax({
          url: "/api/posts/" + self.id,
          type: "delete"
        });
    }
}



/*
function like_dislike(el, postId) {
       jQuery.ajax({
            type:"POST", //post data
            url:'/posts/' + postId + '/like/' // your url that u write in action in form tag
      }).done(function(result){
            if (result.liked_by_user){
                el.value = "Dislike";
                console.log("Likes: " + result.liked_by_user)
            } else {
                el.value = "Like";
                console.log("Likes: " + result.liked_by_user)
            }
            $("#like_count" + postId).load(location.href + " #like_count" + postId, function() {
                $(this).children(':first').unwrap();
            });
      });
}

function follow_user(el, userId){
    jQuery.ajax({
        type:"POST",
        url:'/profile/' + userId + '/follow/'
    }).done(function(result){
        if (result.followed_by_user){
            el.value = "Unfollow";
        } else {
            el.value = "Follow";
        }
    });
}

function post_delete(el, postId) {
    if (confirm('Are you sure you want to delete this post?')){
        jQuery.ajax({
            type:"POST",
            url:'/posts/' + postId + '/delete/'
        }).done(function(result){
                var toDelete = $("#post" + postId);
                toDelete.remove();
                console.log("You deleted this post: " + toDelete);
        });
    }
}


function post_share(el, postId) {
  jQuery.ajax({
    type:"POST",
    url:'/posts/' + postId + '/share/'
  }).done(function(result){
    var $shared_post = $("<div>", {class: "post", id: "post" + result.postId});
    $("#posts").prepend($shared_post);
    $shared_post.load(location.href + " #post" + result.postId, function() {
      $(this).children(':first').unwrap();
    });
    console.log($shared_post);
  });
}


function submit_post(){
    jQuery.ajax({
        type: "POST",
        url: "/posts/create/",
        data: $('#content').serialize()
    }).done(function(result){
        var $new_post = $("<div>", {class: "post", id: "post" + result.postId});
        $("#posts").prepend($new_post);
        $new_post.load(location.href + " #post" + result.postId, function() {
                $(this).children(':first').unwrap();
            });
        console.log($new_post);
    });
}

function submit_message(recipientId){
    var message = prompt("Message: ");
    if (message != null) {
      jQuery.ajax({
        type: "POST",
        url: "/messages/compose/",
        data: {
          message_body: message,
          recipient: recipientId,
        }
      }).done(function(result){
        $("#sent_li").load(location.href + " #sent_li");
        $("#trash_li").load(location.href + " #trash_li");
      });
    }
}


function auto_refresh() {
    setTimeout( function () {
      console.log(location.href);
        $('#posts').fadeOut('slow').load(location.href + " #posts").fadeIn('slow');
        auto_refresh();
    }, 10000);
}

function delete_message(el, messageId){
    if (confirm('Are you sure you want to delete this message?')){
        jQuery.ajax({
            type:"POST",
            url:'/messages/' + messageId + '/delete/'
        }).done(function(result){
                var toDelete = $("#message" + messageId);
                toDelete.remove();
                $("#inbox_li").load(location.href + " #inbox_li");
                $("#sent_li").load(location.href + " #sent_li");
                $("#trash_li").load(location.href + " #trash_li");
        });
    };
}


function logout(){
    if (confirm('Are you sure you want to log out?')){
        jQuery.ajax({
            type:"POST",
            url:'/logout/'
        }).done(function(result){
            window.location.href = "/logout/";
            console.log("You logged out!");
        });
    }
}

function auto_refresh_tab() {
    setTimeout(function () {
      $.get('check', function(data){
        new_messages = JSON.parse(data.new_messages);

        if (data.new_messages_available) {
            for ( var i = 0 ; i < data.new_messages_count; i++ ){
                  $("#inbox_li").load(location.href + " #inbox_li");

                  var $new_message = $("<div>", {class: "message", id: "message" + new_messages[0][0]});
                  $("#chat").prepend($new_message);
                  console.log(location.href + "inbox/ #message" + new_messages[0][0]);
                  $new_message.load(location.href + "inbox/ #message" + new_messages[0][0], function() {
                        $(this).children(':first').unwrap();
                  }).fadeIn('slow');
            }
        }
      });
      auto_refresh_tab();
  }, 8000);
}
*/
