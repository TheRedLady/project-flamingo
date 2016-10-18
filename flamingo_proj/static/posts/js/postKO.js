// Class to represent a row in the seat reservations grid
//
//


function PostViewModel() {
  var self = this;
//  self.post = "trynki";
  self.sharePost = sharePost;
  self.removePost = removePost;
  self.baba = "baba";

  init();

  //-----------

  function init() {
    var id = getId();
    $.getJSON("/api/posts/" + id + "/", function(data) {
      self.post = makePost(data);
    });
  }

  function sharePost(post) {
    $.ajax({
        url: "/api/posts/" + self.post['id'] + "/share/",
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

var model = new PostViewModel();
console.log(model);
ko.applyBindings(new PostViewModel());
