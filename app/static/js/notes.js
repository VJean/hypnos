$('#creation').on('shown.bs.modal', function () {
  $('#creationContent').focus()
})

$('#edition').on('shown.bs.modal', function () {
  $('#editionContent').focus()
})

function NotesViewModel(){
    var self = this;
    self.notesArray = ko.observableArray();
    
    $.getJSON('http://localhost:5000/api/notes', function(data){
        data['notes'].forEach(function(n,i,array) {
            self.notesArray.push({
                id: ko.observable(n.id),
                content: ko.observable(n.content),
                timestamp: ko.observable(n.timestamp),
                done: ko.observable(n.done)
            })
        })
    });

    self.update = function(note,newnote){
        var i = self.notesArray.indexOf(note)
        self.notesArray()[i].id(newnote.id)
        self.notesArray()[i].timestamp(newnote.timestamp)
        self.notesArray()[i].content(newnote.content)
        self.notesArray()[i].done(newnote.done)
    };

    self.beginAdd = function(){
        $("#creation").modal('show');
    }

    self.add = function(note){
        $.ajax({
            url: 'http://localhost:5000/api/notes',
            type:"POST",
            data: note,
            contentType:"application/json",
            dataType:"json",
            success: function(data){
                // unshift : add at beginning of list
                self.notesArray.unshift({
                    id: ko.observable(data.note.id),
                    content: ko.observable(data.note.content),
                    timestamp: ko.observable(data.note.timestamp),
                    done: ko.observable(data.note.done)
                })
            }
        })
    };

    self.edit = function(note) {
        editViewModel.setNote(note)
        $("#edition").modal('show');
    };

    self.markDone = function(note){
        $.ajax({
            url: 'http://localhost:5000/api/notes/'+note.id(),
            type:"PUT",
            data: JSON.stringify({'done': true}),
            contentType:"application/json",
            dataType:"json",
            success: function(data){
                self.update(note,data.note)
            }
        })
    };

    self.remove = function(note){
        $.ajax({
            url: 'http://localhost:5000/api/notes/'+note.id(),
            type:"DELETE",
            contentType:"application/json",
            dataType:"json",
            success: function(data){
                if (data.result){
                    self.notesArray.remove(note)
                }
            }
        })
    };
};

function AddViewModel(){
    var self = this;
    self.content = ko.observable();

    self.validAdd = function() {
        $("#creation").modal('hide')
        n = JSON.stringify({'content': self.content()});
        notesViewModel.add(n);
    };

};

function EditViewModel(){
    var self = this;
    self.content = ko.observable();

    self.setNote = function(note) {
        self.note = note;
        self.content(note.content());
    };

    self.validEdit = function() {
        $("#edition").modal('hide');

        $.ajax({
            url: 'http://localhost:5000/api/notes/'+self.note.id(),
            type:"PUT",
            data: JSON.stringify({'content': self.content()}),
            contentType:"application/json",
            dataType:"json",
            success: function(data){
                notesViewModel.update(self.note,data.note)
            }
        });
    };
};

var notesViewModel = new NotesViewModel();
var addViewModel = new AddViewModel();
var editViewModel = new EditViewModel();
ko.applyBindings(notesViewModel, $("#notesMain")[0]);
ko.applyBindings(addViewModel, $("#creation")[0]);
ko.applyBindings(editViewModel, $("#edition")[0]);