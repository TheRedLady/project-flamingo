function Tag(data) {
    this.tag = ko.observable(data.tag_clean);
    this.occurrences_count = ko.observable(data.tag_occurrences_count);

    this.goToTag = function () {
        window.location.href = "/posts/tag/" + this.tag();
    }
}

function MessagesViewModel() {
    var self = this;
    self.tags = ko.observableArray([]);

    self.getTags = function() {
        $.getJSON('/api/posts/trending/', function(allData) {
        console.log(allData['results']);
        var mappedTags = $.map(allData['results'], function(item) { return new Tag(item) });
        self.tags(mappedTags);
        });
    }

    self.getTags();
};

ko.applyBindings(new MessagesViewModel());
