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

    self.goToFolder('Inbox');
};

ko.applyBindings(new MessagesViewModel());