// Class to represent a row in the seat reservations grid
//
makePost = function(data) {
  return new Post(data['id'], data['url'], data['posted_by'], data['content'],
                  data['created'], data['shared']);
}

function Post(id, url, postedBy, content, created, shared) {
    var self = this;
    self.id = id;
    self.url = url;
    self.posted_by = postedBy;
    self.content = content;
    self.created = created;
    self.shared = shared;

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

    var loc = String(window.location).split("/");
    $.getJSON("/api/posts/?posted_by=" + loc[loc.length -2], function(allData) {
        var mappedPosts = $.map(allData['results'], function(post) { return makePost(post); });
        self.posts(mappedPosts);
    });

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
        new_post.shared = true;
        console.log(new_post);
        self.posts.unshift(new_post);
      });
    }

    self.removePost = function(post) { 
      self.posts.remove(post);
      post.removePost();
    };

    self.likePost = function(post) {
        $.ajax({
            url: "/api/posts/" + post.post_id + "/like/",
            method: "GET"
        }).done(function (results) {
            console.log(results);
            });
        };
}

// Activates knockout.js
ko.applyBindings(new ProfileViewModel());
