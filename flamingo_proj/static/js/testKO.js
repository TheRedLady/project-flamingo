function AppViewModel() {
    this.knockoutTest = ko.observable("I am here");
}

// Activates knockout.js
ko.applyBindings(new AppViewModel());