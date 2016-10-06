// Class to represent a row in the seat reservations grid
function Post(postedBy, content, created) {
    var self = this;
    self.posted_by = postedBy;
    self.content = content;
    self.created = created;
}

// This is a simple *viewmodel* - JavaScript that defines the data and behavior of your UI
function ProfileViewModel() {
    var self = this;
    self.firstName = ko.observable("Bert");
    self.lastName = ko.observable("Bertington");
    self.posts = ko.observableArray([]);
    self.nextPostContent = ko.observable();

    self.fullName = ko.computed(function() {
        return self.firstName() + " " + self.lastName();
    }, this);

    $.getJSON("/api/posts/", function(allData) {
        console.log(allData['results']);
        var mappedPosts = $.map(allData['results'], function(post) { return new Post(post['posted_by'], post['content'], post['created']) });
        console.log(mappedPosts);
        self.posts(mappedPosts);
    });

    self.addPost = function() {
        self.posts.unshift(new Post("CURRENT USER", self.nextPostContent()));
        self.nextPostContent("");
    };
    self.removePost = function(post) { self.posts.remove(post) };
}

// Activates knockout.js
ko.applyBindings(new ProfileViewModel());