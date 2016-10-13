function Message(data) {
    this.id = ko.observable(data.id);
    this.sender = ko.observable(data.sender);
    this.recipient = ko.observable(data.recipient);
    this.message_body = ko.observable(data.message_body);
    this.sent_at = ko.observable(data.sent_at);
}

function MessagesViewModel() {
    var self = this;
    self.folders = ['Inbox', 'Sent', 'Trash'];
    self.chosenFolderId = ko.observable();
    self.chosenFolderData = ko.observable();
    self.chosenMailData = ko.observable();
    self.messages = ko.observableArray([]);

    self.goToFolder = function(folder) {
        self.chosenFolderId(folder);
        self.chosenMailData(null);
//        $.get('/api/messaging', { folder: folder }, self.chosenFolderData);
        $.getJSON('/api/messaging', { folder: folder }, function(allData) {
        console.log(allData['results']);
        var mappedMails = $.map(allData['results'], function(item) { return new Message(item) });
        self.messages(mappedMails);
        });
    }

    self.goToMail = function(mail) {
        self.chosenFolderData(null);
        $.get("/api/messaging/" + mail.id() + "/", {}, self.chosenMailData);
    }

    self.moveToTrash = function(mail) {
        $.ajax({
            url: "/api/messaging/" + mail.id() + "/",
            type: "delete"
        }).done(function(result){
            console.log("result: " + result);
            self.messages.remove(mail);
        });
    }

    self.goToFolder('Inbox');
};

ko.applyBindings(new MessagesViewModel());