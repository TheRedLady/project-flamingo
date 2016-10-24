function PostsByTag() {
    init();

    function init() {
      PostContainer.call(this, "/api/posts/search/" + getId(), true);
    }
}

PostsByTag.prototype = Object.create(PostContainer.prototype);

ko.applyBindings(new PostsByTag());

//ko.applyBindings(new PostContainer("/api/posts/search/" + getId(), false));
