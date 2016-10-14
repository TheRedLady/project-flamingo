function Post(data) {
    this.content = ko.observable(data.content);
    this.posted_by_name = ko.observable(data.posted_by_name);
    this.date = ko.observable(data.created);
    this.postId = ko.observable(data.id);

    this.goToPost = function () {
        console.log(data)
        window.location.href = "/posts/" + this.postId();
    }
}

function Profile(data) {
    this.fullName = data.user['first_name'] + " " + data.user['last_name'];
    this.profileUrl = ko.observable(data.url);
    this.email = ko.observable(data.user['email']);
    this.profileId = ko.observable(data.user['id']);

    this.goToProfile = function () {
        console.log(data)
        window.location.href = "/profile/" + this.profileId();
    }
}

function SearchViewModel() {
    var self = this;
    self.folders = ['Posts', 'Profiles'];
    self.chosenFolderId = ko.observable();
    self.searchText = ko.observable();
    self.results = ko.observableArray([]);
    self.postResults = ko.observableArray([]);
    self.profileResults = ko.observableArray([]);

    self.postTabSelected = ko.observable();
    self.profileTabSelected = ko.observable();

    self.goToFolder = function(folder) {
        self.chosenFolderId(folder);
        if (folder === 'Posts') {
            self.postTabSelected(true);
            self.profileTabSelected(false);
            $.getJSON('/api/posts/search/' + self.searchText(), {}, function(allData) {
            var mappedPosts= $.map(allData['results'], function(item) { return new Post(item) });
            self.postResults(mappedPosts);
            });
        } else {
            $.getJSON('/api/profiles/search/' + self.searchText(), {}, function(allData) {
            var mappedProfiles= $.map(allData['results'], function(item) { return new Profile(item) });
            self.profileResults(mappedProfiles);
            self.postTabSelected(false);
            self.profileTabSelected(true);
            });
        }
    }

    self.findResults = function () {
        self.goToFolder('Posts');
    }
};

ko.applyBindings(new SearchViewModel());
