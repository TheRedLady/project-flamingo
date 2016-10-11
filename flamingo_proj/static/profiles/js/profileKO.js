// Class to represent a row in the seat reservations grid
//
makePost = function(data) {
  return new Post(data['id'], data['posted_by'], data['content'],
                  data['created'],data['posted_by_url'], data['posted_by_name'],
                  data['post_url']);
}

function Post(id, postedBy, content, created, posted_by_url, posted_by_name, post_url) {
    var self = this;
    self.post_id = id;
    self.post_url = post_url;
    self.posted_by = postedBy;
    self.posted_by_url = posted_by_url
    self.posted_by_name = posted_by_name
    self.content = content;
    self.created = created;

    self.removePost = function() {
      $.ajax({
          url: "/api/posts/" + self.post_id,
          type: "delete"
        });
    }
}

// This is a simple *viewmodel* - JavaScript that defines the data and behavior of your UI
function ProfileViewModel() {
    var self = this;
    self.firstName = ko.observable("Bert");
    self.lastName = ko.observable("Bertington");
    self.posts = ko.observableArray([]);
    self.nextPostContent = ko.observable("");

    self.fullName = ko.computed(function() {
        return self.firstName() + " " + self.lastName();
    }, this);
 
    var loc = String(window.location).split("/");
    $.getJSON("/api/posts/?posted_by=" + loc[loc.length -2], function(allData) {
        console.log(allData['results']);
        var mappedPosts = $.map(allData['results'], function(post) { return makePost(post); });
        console.log(mappedPosts);
        self.posts(mappedPosts);
    });

    self.addPost = function(user_id) {
      console.log(user_id);
        console.log(self.nextPostContent());
        $.ajax("/api/posts/",
        {
          data: { posted_by: user_id, content: self.nextPostContent()},
          type: "post"
        }).done(function(post) {
          var new_post = makePost(post);
          console.log(new_post);
        self.posts.unshift(new_post);
        });
        self.nextPostContent("");
    };
    self.removePost = function(post) { 
      self.posts.remove(post);
      post.removePost();
    };
}

// Activates knockout.js
ko.applyBindings(new ProfileViewModel());
