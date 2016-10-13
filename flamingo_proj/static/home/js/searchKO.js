function Post(data) {
    this.content = ko.observable(data.content);
    this.posted_by = ko.observable(data.posted_by);
    this.date = ko.observable(data.created);
}

function Profile(data) {
    this.fullName = data.user['first_name'] + " " + data.user['last_name'];
    this.profileUrl = ko.observable(data.url);
    this.email = ko.observable(data.user['email']);
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
            $.getJSON('/api/posts/search/' + self.searchText() + "/", {}, function(allData) {
            var mappedPosts= $.map(allData['results'], function(item) { return new Post(item) });
            self.postResults(mappedPosts);
            });
        } else {
            $.getJSON('/api/profiles/search/' + self.searchText() + "/", {}, function(allData) {
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
