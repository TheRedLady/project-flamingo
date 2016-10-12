function Post(data) {
    this.content = ko.observable(data.content);
    this.posted_by = ko.observable(data.posted_by);
}

function Profile(data) {
    this.fullName = data.user['first_name'] + " " + data.user['last_name']
    this.profileUrl = ko.observable(data.url);
}

function SearchViewModel() {
    var self = this;
    self.folders = ['Tags', 'Profiles'];
    self.chosenFolderId = ko.observable();
    self.searchText = ko.observable();
    self.profileResults = ko.observableArray([]);
    self.tagResults = ko.observableArray([]);

    self.goToFolder(folder) {
        self.chosenFolderId(folder);
        if (folder === 'Tags') {
            $.getJSON('/api/posts/tag/' + self.searchText() + "/", {}, function(allData) {
            console.log(allData['results']);
            var mappedPosts= $.map(allData['results'], function(item) { return new Post(item) });
            self.tagResults(mappedPosts);
            });
        } else {
            $.getJSON('/api/profiles/search/' + self.searchText() + "/", {}, function(allData) {
            console.log(allData['results']);
            var mappedProfiles= $.map(allData['results'], function(item) { return new Profile(item) });
            self.profileResults(mappedProfiles);
            });
        }
    }
}