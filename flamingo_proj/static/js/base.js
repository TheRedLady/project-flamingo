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


getId = function () {
    var loc = String(window.location).split("/");
    var id = loc[loc.length - 2];
    return id;
}

function Post(data) {
    var self = this;
    self.id = data['id'];
    self.url = data['url'];
    self.posted_by = data['posted_by'];
    self.content = data['content'];
    self.created = data['created'];
    self.likes = ko.observable(data['like_count']);
    self.liked = ko.observable(data['liked']);

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

    var share = data['share'];
    if (share === null) {
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

