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
    self.profileResults = ko.observableArray([]);

    self.postTabSelected = ko.observable();
    self.profileTabSelected = ko.observable();


    self.goToFolder = function(folder) {
        self.chosenFolderId(folder);
        if (folder === 'Posts') {
//            PostContainer.call(this, "/api/posts/search/" + self.searchText(), false);
            self.loopPages("/api/posts/search/" + self.searchText());
            console.log(self.posts())
            self.postTabSelected(true);
            self.profileTabSelected(false);
        } else {
            self.postTabSelected(false);
            self.profileTabSelected(true);
            if (!self.searchText()) {self.posts(null); self.profileResults([]); return;}
            $.getJSON('/api/profiles/search/' + self.searchText(), {}, function(allData) {
            var mappedProfiles= $.map(allData['results'], function(item) { return new Profile(item) });
            self.profileResults(mappedProfiles);
            });
        }
    }

    self.findResults = function () {
        self.goToFolder('Posts');
        PostContainer.call(this, "/api/posts/search/" + self.searchText(), false);
    }
};

SearchViewModel.prototype = Object.create(PostContainer.prototype);

ko.applyBindings(new SearchViewModel());
