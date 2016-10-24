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

    self.likeUnlike = likeUnlike;
//    self.removePost = removePost;

    init();

    //---------------

    function init() {
      var share = data['share'];
      if (share === null) {
        self.is_shared = false;
        self.share = null;
      }
      else {
        self.is_shared = true;
        self.share = share;
      }
    }

    function likeUnlike() {
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


//    function removePost() {
//      $.ajax({
//          url: "/api/posts/" + self.id,
//          type: "delete"
//      });
//    }
}


function PostContainer(url, append) {
  var self = this;
  self.posts = ko.observableArray([]);
  self.nextPostContent = ko.observable("");
  self.append = append;

  init();

  function init() {
    PostContainer.prototype.loopPages(self, url);
  }
}

PostContainer.prototype = {

  loopPages: function(obj, url) {
    $.getJSON(url, function(data) {
        var mappedPosts = $.map(data['results'], function(post) { return new Post(post); })
        for(let i = 0; i < mappedPosts.length; i++) {
          obj.posts.push(mappedPosts[i]);
        }

      if(data['next'] != null){
        PostContainer.prototype.loopPages(obj, data['next']);
      }
    });
  },

  addPost: function() {
      if (!self.nextPostContent()) {
        alert("Please add some content")
        return;
      }
      $.ajax("/api/posts/",
          {
              data: { content: self.nextPostContent()},
              type: "post"
          }).done(function(data) {
              self.nextPostContent("");
              if(self.append) {
                self.posts.unshift(new Post(data));
              }
              alert("Success. You can see your post in your profile.");
          });
  },

  sharePost: function(post) {

    $.ajax({
      url: "/api/posts/" + post.id + "/share/",
      type: "post"
    }).done(function(data) {
      if (self.append) {self.posts.unshift(new Post(data));}
      alert("You shared this post");
    });
  },

  removePost: function (post) {
      var conf = confirm("Are you sure you want to delete this post?");
      if(conf === true) {
          $.ajax({
          url: "/api/posts/" + post.id,
          type: "delete"
          }).done(function() {
            console.log(self.posts)
//            self.posts.remove(post)
          });
      }
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
