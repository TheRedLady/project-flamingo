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
    self.posts = ko.observableArray([]);
    self.profileResults = ko.observableArray([]);

    self.postTabSelected = ko.observable();
    self.profileTabSelected = ko.observable();

    self.goToFolder = function(folder) {
        self.chosenFolderId(folder);
        if (folder === 'Posts') {
          self.postTabSelected(true);
          self.profileTabSelected(false);

          self.loopPages = function(url) {
            if (!self.searchText()) {self.posts([]); self.profileResults([]); return;}
            $.getJSON(url, function(data) {
              var new_posts = $.map(data['results'], function(post) { return new Post(post); })
              self.posts(new_posts);
              if(data['next'] != null){
                self.loopPages(data['next']);
              }
            });
          };

          self.loopPages('/api/posts/search/' + self.searchText());
        } else {
            self.postTabSelected(false);
            self.profileTabSelected(true);
            if (!self.searchText()) {self.posts([]); self.profileResults([]); return;}
            $.getJSON('/api/profiles/search/' + self.searchText(), {}, function(allData) {
            var mappedProfiles= $.map(allData['results'], function(item) { return new Profile(item) });
            self.profileResults(mappedProfiles);
            });
        }
    }

    self.findResults = function () {
        self.goToFolder('Posts');
    }
};

ko.applyBindings(new SearchViewModel());
