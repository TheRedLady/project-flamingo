function MessagesViewModel() {
    var self = this;
    self.folders = ['Inbox', 'Sent', 'Trash'];
    self.chosenFolderId = ko.observable();
    self.chosenFolderData = ko.observable();
    self.chosenMailData = ko.observable();

    self.goToFolder = function(folder) {
        self.chosenFolderId(folder);
        self.chosenMailData(null);
        $.get('/api/messaging', { folder: folder }, self.chosenFolderData);
    }

    self.goToMail = function(mail) {
        self.chosenFolderData(null);
        $.get("/api/messaging/" + mail.id + "/", {}, self.chosenMailData);
    }

    self.moveToTrash = function(mail) {
        $.ajax({
            url: "/api/messaging/" + mail.id + "/",
            type: "delete"
        });
        self.goToFolder(self.chosenFolderId());
    }

    self.goToFolder('Inbox');
};

ko.applyBindings(new MessagesViewModel());