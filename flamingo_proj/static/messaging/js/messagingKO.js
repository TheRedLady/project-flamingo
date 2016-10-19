function Message(data) {
    this.id = ko.observable(data.id);
    this.sender = ko.observable(data.sender_name);
    this.sender_id = ko.observable(data.sender);
    this.recipient = ko.observable(data.recipient_name);
    this.recipient_id = ko.observable(data.recipient);
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
        $.getJSON('/api/messaging', { folder: folder }, function(allData) {
        var mappedMails = $.map(allData['results'], function(item) { return new Message(item) });
        self.messages(mappedMails);
        });
    }

    self.goToMail = function(mail) {
        self.chosenFolderData(null);
        $.getJSON("/api/messaging/" + mail.id() + "/", {}, function(item) {
            self.chosenMailData(new Message(item));
        });
    }

    self.moveToTrash = function(mail) {
        var conf = confirm("Are you sure you want to delete this message?");
        if(conf == true) {
            $.ajax({
                url: "/api/messaging/" + mail.id() + "/",
                type: "delete"
            }).done(function(result){
                self.messages.remove(mail);
            });
        }
    }

    self.goToFolder('Inbox');
};

ko.applyBindings(new MessagesViewModel());