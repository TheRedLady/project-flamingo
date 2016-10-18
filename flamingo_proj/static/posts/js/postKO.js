
function PostViewModel() {
  var self = this;
  self.post = ko.observable();
  self.sharePost = sharePost;
  self.removePost = removePost;

  init();

  //-----------

  function init() {
    var id = getId();
    $.getJSON("/api/posts/" + id + "/", function(data) {
      setPost(data);
    });
  }

  function setPost(data) {
    self.post(new Post(data));
  }

  function sharePost(post) {
    $.ajax({
        url: "/api/posts/" + self.post.id + "/share/",
        type: "post"
    });
  }

  function removePost(post) { 
    var conf = confirm("Are you sure you want to delete this post?");
    if(conf == true) {
      self.post.remove(post);
    }
  }

}

ko.applyBindings(new PostViewModel());
