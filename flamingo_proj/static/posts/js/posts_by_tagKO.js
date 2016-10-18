function PostsByTag() {
  var self = this;
  self.posts = ko.observableArray([]);
  self.nextPostContent = ko.observable("");

  self.tag = function () {
    var loc = String(window.location).split("/");
    var id = loc[loc.length - 2];
    return id;
    }

  self.loopPages = function(url) {
    $.getJSON(url, function(data) {
      var new_posts = $.map(data['results'], function(post) { return new Post(post); })
      self.posts(new_posts);
      if(data['next'] != null){
        self.loopPages(data['next']);
      }
    });
  };

  self.loopPages("/api/posts/search/" + self.tag());

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


ko.applyBindings(new PostsByTag());
