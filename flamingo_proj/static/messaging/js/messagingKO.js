function Message(data) {
    this.id = ko.observable(data.id);
    this.sender = ko.observable(data.sender_name);
    this.sender_id = ko.observable(data.sender);
    this.recipient = ko.observable(data.recipient_name);
    this.recipient_id = ko.observable(data.recipient);
    this.message_body = ko.observable(data.message_body);
    this.sent_at = ko.observable(data.sent_at);
    this.sender_is_self = ko.observable(data.sender_is_self);
}

function MessagesViewModel() {
    var self = this;
    self.folders = ['Inbox', 'Sent', 'Trash'];
    self.chosenFolderId = ko.observable();
    self.chosenFolderData = ko.observable();
    self.chosenMailData = ko.observable();
    self.messages = ko.observableArray([]);
    self.showMessageBox = ko.observable(false);
    self.messageBoxContent = ko.observable();

    self.goToFolder = function(folder) {
        self.chosenFolderId(folder);
        self.chosenMailData(null);
        $.getJSON('/api/messaging', { folder: folder }, function(allData) {
        var mappedMails = $.map(allData['results'], function(item) { return new Message(item) });
        self.messages(mappedMails);
        self.showMessageBox(false);
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
            self.chosenMailData(null);
            $.ajax({
                url: "/api/messaging/" + mail.id() + "/",
                type: "delete"
            }).done(function(result){
                self.messages.remove(mail);
            });
        }
    }

    self.openMessageBox = function() {
        if (self.showMessageBox()) {
            self.showMessageBox(false);
        } else { self.showMessageBox(true); }
    }

    self.sendTo = function () {
        if (self.chosenFolderId() === "Inbox") {
            return self.chosenMailData().sender_id()
        } else if (self.chosenFolderId() === "Sent") {
            return self.chosenMailData().recipient_id()
        } else {
            if (self.chosenMailData().sender_is_self()) {
                return self.chosenMailData().recipient_id()
            } else {
                return self.chosenMailData().sender_id()
            }
        }
    }

    self.sendMessage = function() {
        console.log("Sending: " + self.messageBoxContent() +
                    " To: " + self.sendTo()
        );

        $.ajax("/api/messaging/", {
            data: {message_body: self.messageBoxContent() ,
                   recipient: send_to},
            type: "post",
        }).done(function() {
              alert("Message Sent!");
              self.messageBoxContent('');
              self.showMessageBox(false);
           });
    }

    self.goToFolder('Inbox');
};

ko.applyBindings(new MessagesViewModel());