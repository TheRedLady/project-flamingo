function ProfileViewModel() {
    var self = this;
    self.posts = ko.observableArray([]);
    self.nextPostContent = ko.observable("");
    self.current_profile = getId();
    self.following = ko.observable();
    self.showMessageBox = ko.observable(false);
    self.messageBoxContent = ko.observable();

   var posts_by_user = "/api/posts/?posted_by=" + self.current_profile;

    self.mapPosts = function(posts) {
      var mappedPosts = $.map(posts, function(post) { return new Post(post); })
      self.posts(mappedPosts)
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
        if (!self.nextPostContent()) {
            alert("Please add some content")
            return;
        }
        $.ajax("/api/posts/",
        {
            data: { posted_by: user_id, content: self.nextPostContent()},
            type: "post"
        }).done(function(post) {
            var new_post = new Post(post);
            self.posts.unshift(new_post);
            self.nextPostContent("");
        });
    };

    self.sharePost = function(post) {
      $.ajax({
        url: "/api/posts/" + post.id + "/share/",
        type: "post"
      }).done(function(post) {
        var new_post = new Post(post);
        if(self.current_profile == new_post.posted_by.id){
          self.posts.unshift(new_post);
        };
        alert("You shared this post");
      });
    };

    self.removePost = function(post) {
      var conf = confirm("Are you sure you want to delete this post?");
        if(conf == true) {
          self.posts.remove(post);
          post.removePost();
        }
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

    self.openMessageBox = function() {
        if (self.showMessageBox()) {
            self.showMessageBox(false);
        } else { self.showMessageBox(true); }
    }

    self.sendMessage = function() {

        console.log("Sending: " + self.messageBoxContent() +
                    " To: " + self.current_profile
        );

        if (!self.messageBoxContent()) {
          alert("Please add some content")
          return;
        }

        $.ajax("/api/messaging/", {
            data: ko.toJSON( {message_body: self.messageBoxContent() ,
                              recipient: self.current_profile}),
            type: "post",
            contentType: "application/json",
        }).done(function() {
              alert("Message Sent!");
              self.messageBoxContent('');
           });
    }
}


ko.applyBindings(new ProfileViewModel());
