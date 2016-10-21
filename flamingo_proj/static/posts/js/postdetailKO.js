var id = getId();

console.log("here");
console.log(id);
$.getJSON("/api/posts/" + id, function(data) {
  console.log(data);
});
 
console.log(id);

ko.applyBindings(new Post(5));
