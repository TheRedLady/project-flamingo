// Class to represent a row in the seat reservations grid
//
//

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


// This is a simple *viewmodel* - JavaScript that defines the data and behavior of your UI
function ProfileViewModel() {
    var self = this;
    self.posts = ko.observableArray([]);
    self.nextPostContent = ko.observable("");
    self.current_profile = getId();
    self.following = ko.observable();
  
   var posts_by_user = "/api/posts/?posted_by=" + self.current_profile;

    self.mapPosts = function(posts) {
      var mappedPosts = $.map(posts, function(post) { return makePost(post); })
      for(let i = 0; i < mappedPosts.length; i++){
        self.posts.push(mappedPosts[i]);
      }
    }

    self.loopPages = function(url) {

      $.getJSON(url, function(data) {
        self.mapPosts(data['results']);
        if(data['previous'] == null) {
          var follow_url = "/api/profiles/" + self.current_profile + "/follow/";
          $.getJSON(follow_url, function(data) {
            self.following(data['following']);
          });
        }
        if(data['next'] != null){
          self.loopPages(data['next']);
        }
      });

    };

    self.loopPages(posts_by_user);

    self.addPost = function(user_id) {
        $.ajax("/api/posts/",
        {
          data: { posted_by: user_id, content: self.nextPostContent()},
          type: "post"
        }).done(function(post) {
          var new_post = makePost(post);
          self.posts.unshift(new_post);
        });
        self.nextPostContent("");
    };

    self.sharePost = function(post) {
      $.ajax({
        url: "/api/posts/" + post.id + "/share/",
        type: "post"
      }).done(function(post) {
        var new_post = makePost(post);
        if(self.current_profile == new_post.posted_by['id']){
          self.posts.unshift(new_post);
        }
      });
    };

    self.removePost = function(post) { 
      self.posts.remove(post);
      post.removePost();
    };

    self.follow = function() {
      var url = "/api/profiles/" + self.current_profile; 
      if(self.following()) {
        url += "/unfollow/";
      }
      else {
        url += "/follow/";
      }
      $.ajax({
        url: url,
        method: "POST",
      }).done(function (data) {
        self.following(data['following']);
      });
    };
}


function Feed(url) {
  var self = this;
  self.posts = ko.observableArray([]);
  self.nextPostContent = ko.observable("");

  self.loopPages = function(url) {
    $.getJSON(url, function(data) {
      var new_posts = $.map(data['results'], function(post) { return makePost(post); })
      for(let i = 0; i < new_posts.length; i++){
        self.posts.push(new_posts[i]);
      }
      if(data['next'] != null){
        self.loopPages(data['next']);
      }
    });
  };
  
  self.loopPages(url);

  self.addPost = function(user_id) {
    $.ajax("/api/posts/",
        {
          data: { posted_by: user_id, content: self.nextPostContent()},
          type: "post"
        });    
    self.nextPostContent("");
  };

  self.sharePost = function(post) {
      $.ajax({
        url: "/api/posts/" + post.id + "/share/",
        type: "post"
      });
  };

}
