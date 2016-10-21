function ProfileViewModel() {
    var self = this;
    self.current_profile = getId();
    self.following = ko.observable();
    self.showMessageBox = ko.observable(false);
    self.messageBoxContent = ko.observable();

    self.follow = follow;


    init();


    //----
    

    function init() {
      $.ajax({
        url: "/api/profiles/" + self.current_profile + "/follow/",
        type: "get"
      }).done(function(data) {
        self.following(data['following']);
      });
      
    }

    function follow() {
      var url = "/api/profiles/" + self.current_profile; 
      if(self.following()) {
        url += "/unfollow/";
      }
      else {
        url += "/follow/";
      }
      $.ajax({
        url: url,
        method: "POST",
      }).done(function (data) {
        self.following(data['following']);
      });
    };

    self.openMessageBox = function() {
        if (self.showMessageBox()) {
            self.showMessageBox(false);
        } else { self.showMessageBox(true); }
    }

    self.sendMessage = function() {

        console.log("Sending: " + self.messageBoxContent() +
                    " To: " + self.current_profile
        );

        if (!self.messageBoxContent()) {
          alert("Please add some content")
          return;
        }

        $.ajax("/api/messaging/", {
            data: ko.toJSON( {message_body: self.messageBoxContent() ,
                              recipient: self.current_profile}),
            type: "post",
            contentType: "application/json",
        }).done(function() {
              alert("Message Sent!");
              self.messageBoxContent('');
           });
    }
}

var cont = new PostContainer("/api/posts/search/?posted_by=" + getId(), true);
ProfileViewModel.prototype = Object.create(cont);

ko.applyBindings(new ProfileViewModel());
