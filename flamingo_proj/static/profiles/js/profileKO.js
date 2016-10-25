function ProfileViewModel() {
    self = this;
    self.current_profile = getId();
    self.following = ko.observable();
    self.showMessageBox = ko.observable(false);
    self.messageBoxContent = ko.observable();

    self.follow = follow;

    init();


    //---------

    function init() {
        PostContainer.call(self, "/api/posts/?posted_by=" + getId(), true);
        $.ajax({
            url: "/api/profiles/" + self.current_profile + "/follow/",
            type: "get"
        }).done(function(data) {
            self.following(data['following']);
        });

    }

    function follow() {
        var url = "/api/profiles/" + self.current_profile;
        if (self.following()) {
            url += "/unfollow/";
        } else {
            url += "/follow/";
        }
        $.ajax({
            url: url,
            method: "POST",
        }).done(function(data) {
            self.following(data['following']);
        });
    };

    self.openMessageBox = function() {
        if (self.showMessageBox()) {
            self.showMessageBox(false);
        } else {
            self.showMessageBox(true);
        }
    }

    self.sendMessage = function() {

        if (!self.messageBoxContent()) {
            alert("Please add some content")
            return;
        }

        $.ajax("/api/messaging/", {
            data: ko.toJSON({
                message_body: self.messageBoxContent(),
                recipient: self.current_profile
            }),
            type: "post",
            contentType: "application/json",
        }).done(function() {
            alert("Message Sent!");
            self.messageBoxContent('');
        });
    }
}

ProfileViewModel.prototype = Object.create(PostContainer.prototype);

ko.applyBindings(new ProfileViewModel());