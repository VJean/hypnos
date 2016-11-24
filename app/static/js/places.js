$('#creation').on('shown.bs.modal', function () {
  $('#creationContent').focus()
})

var mymap = L.map('map').setView([48.8624019,2.4022506], 13);

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>'})
 .addTo(mymap);

var markers = []

function PlacesViewModel(){
    var self = this;
    self.placesArray = ko.observableArray()

    $.getJSON('http://localhost:5000/api/places', function(data){
        data['places'].forEach(function(p,i,array) {
            self.placesArray.push({
                id: ko.observable(p.id),
                name: ko.observable(p.name),
                lon: ko.observable(p.lon),
                lat: ko.observable(p.lat)
            })

            
            var m = L.marker([p.lat, p.lon])
            m.addTo(mymap)
            markers.push(m)
        })

        var markersgroup = L.featureGroup(markers)
        mymap.fitBounds(markersgroup.getBounds().pad(0.3))

    });

    self.beginAdd = function(){
        $("#creation").modal('show');
    }

    self.add = function(place){
        $.ajax({
            url: 'http://localhost:5000/api/places',
            type:"POST",
            data: place,
            contentType:"application/json",
            dataType:"json",
            success: function(data){
                console.log(data)
                var newplace = data['place']
                self.placesArray.push({
                    id: ko.observable(newplace['id']),
                    name: ko.observable(newplace['name']),
                    lon: ko.observable(newplace['lon']),
                    lat: ko.observable(newplace['lat'])
                })
            }
        })
    };

    self.beginEdit = function(place){
        editViewModel.setPlace(place);
        $("#edition").modal('show');
    }

    self.update = function(old_p, new_p) {
        var i = self.placesArray.indexOf(old_p)
        self.placesArray()[i].id(new_p.id)
        self.placesArray()[i].name(new_p.name)
        self.placesArray()[i].lat(new_p.lat)
        self.placesArray()[i].lon(new_p.lon)
    }

    self.delete = function(place){
        $.ajax({
            url: 'http://localhost:5000/api/places' + '/' + place.id(),
            type:"DELETE",
            success: function(data){
                if (data['result']) {
                    self.placesArray.remove(place)
                }
            }
        })
    }
};

function AddViewModel(){
    var self = this;
    self.name = ko.observable();
    self.suggestedCoords = ko.observableArray();
    self.checkedCoords;

    self.validAdd = function() {
        $("#creation").modal('hide');
        p = JSON.stringify({'name': self.name(),'lat':self.checkedCoords.lat,'lon':self.checkedCoords.lon});
        placesViewModel.add(p);
    };

    self.searchCoordinates = function() {
        $.getJSON('http://nominatim.openstreetmap.org/search?format=json&limit=3&q=' + self.name(), function(data){
            // data : array of places returned by nominatim
            self.suggestedCoords(data);
        })
    };
};

function EditViewModel(){
    var self = this;
    self.name = ko.observable();
    self.lon = ko.observable();
    self.lat = ko.observable();
    self.suggestedCoords = ko.observableArray();

    self.setPlace = function(place) {
        self.place = place
        self.name(place.name())
        self.lon(place.lon())
        self.lat(place.lat())
    }

    self.validEdit = function() {
        $("#edition").modal('hide');

        $.ajax({
            url: 'http://localhost:5000/api/places/'+self.place.id(),
            type:"PUT",
            data: JSON.stringify({'name': self.name(), 'lon':self.lon(), 'lat':self.lat()}),
            contentType:"application/json",
            dataType:"json",
            success: function(data){
                placesViewModel.update(self.place,data.place);
            }
        });
    };

    self.searchCoordinates = function() {
        $.getJSON('http://nominatim.openstreetmap.org/search?format=json&limit=3&q=' + self.name(), function(data){
            // data : array of places returned by nominatim
            self.suggestedCoords(data);
        })
    };

    self.deletePlace = function(place) {
        
    }
};

var placesViewModel = new PlacesViewModel()
var addViewModel = new AddViewModel()
var editViewModel = new EditViewModel()
ko.applyBindings(placesViewModel, $("#main")[0])
ko.applyBindings(addViewModel, $("#creation")[0])
ko.applyBindings(editViewModel, $("#edition")[0])