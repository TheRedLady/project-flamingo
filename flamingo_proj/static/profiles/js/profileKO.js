// Class to represent a row in the seat reservations grid
//
//

// This is a simple *viewmodel* - JavaScript that defines the data and behavior of your UI
function ProfileViewModel() {
    var self = this;
    self.posts = ko.observableArray([]);
    self.nextPostContent = ko.observable("");
    self.current_profile = getId();
    self.following = ko.observable();
  
   var posts_by_user = "/api/posts/?posted_by=" + self.current_profile;

    self.mapPosts = function(posts) {
      var mappedPosts = $.map(posts, function(post) { return new Post(post); })
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
          var new_post = new Post(post);
          self.posts.unshift(new_post);
        });
        self.nextPostContent("");
    };

    self.sharePost = function(post) {
      $.ajax({
        url: "/api/posts/" + post.id + "/share/",
        type: "post"
      }).done(function(post) {
        var new_post = Post(post);
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


ko.applyBindings(new ProfileViewModel());
