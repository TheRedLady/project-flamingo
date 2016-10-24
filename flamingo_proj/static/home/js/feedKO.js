function Feed() {
    init();

    function init() {
      PostContainer.call(this, "/api/posts/feed", false);
    }
}

Feed.prototype = Object.create(PostContainer.prototype);

ko.applyBindings(new Feed());
