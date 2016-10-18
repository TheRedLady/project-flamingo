function PostViewModel() {
  var self = this;
  self.post = ko.observable();
  self.sharePost = sharePost;
  self.removePost = removePost;

  init();

  //-----------

  function init() {
    id = getId();
    $.getJSON("/api/posts/" + id + "/", function(data) {
      self.post(new Post(data));
    });
  }

  function sharePost(post) {
    $.ajax({
        url: "/api/posts/" + getId() + "/share/",
        type: "post"
    }).done(function() {alert("You shared this post");} );
  }

  function removePost(post) { 
    var conf = confirm("Are you sure you want to delete this post?");
    if(conf == true) {
      self.post();
      $.ajax({
        url: "/api/posts/" + getId(),
        type: "delete"
      }).done(function() {
        alert("You deleted this post");
        window.location.href = "/profile/"
        } );
    }
  }

}

ko.applyBindings(new PostViewModel());
