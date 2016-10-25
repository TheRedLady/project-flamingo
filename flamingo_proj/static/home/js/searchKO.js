function Profile(data) {
    this.fullName = data.user['first_name'] + " " + data.user['last_name'];
    this.profileUrl = ko.observable(data.url);
    this.email = ko.observable(data.user['email']);
    this.profileId = ko.observable(data.user['id']);

    this.goToProfile = function() {
        window.location.href = "/profile/" + this.profileId();
    }
}

function SearchViewModel() {
    self = this;
    self.folders = ['Posts', 'Profiles'];
    self.chosenFolderId = ko.observable();
    self.searchText = ko.observable();
    self.profileResults = ko.observableArray([]);

    self.postTabSelected = ko.observable();
    self.profileTabSelected = ko.observable();

    init();


    //------------

    function init() {
        PostContainer.call(self, "/api/posts/search/" + self.searchText(), true)
    }

    self.goToFolder = function(folder) {
        self.chosenFolderId(folder);
        if (folder === 'Posts') {
            self.posts([]);
            self.postTabSelected(true);
            self.profileTabSelected(false);
            if (self.searchText()) {
                self.loopPages("/api/posts/search/" + self.searchText());
            }
        } else {
            self.postTabSelected(false);
            self.profileTabSelected(true);
            if (!self.searchText()) {
                self.posts([]);
                self.profileResults([]);
                return;
            }
            $.getJSON('/api/profiles/search/' + self.searchText(), {}, function(allData) {
                var mappedProfiles = $.map(allData['results'], function(item) {
                    return new Profile(item)
                });
                self.profileResults(mappedProfiles);
            });
        }
    }

    self.findResults = function() {
        self.goToFolder('Posts');
    }

};

SearchViewModel.prototype = Object.create(PostContainer.prototype);

ko.applyBindings(new SearchViewModel());