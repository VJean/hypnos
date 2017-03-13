$.getJSON('http://localhost:5000/api/nights', function(data){
    var nights = data['nights']
    nights.forEach(function(e,i,a){
        a[i].date = moment(e.date)
        a[i].amount = moment.duration(e.amount)
    })
    createCharts(nights)
});

function createCharts(nights) {

    createWeeklyMean(nights)
    createPlacesPie()
}

function createWeeklyMean(nights) {
    var myLabels = []
    var myData = []

    // first night from the set might not be at the beginning of a week
    var fromIndex = nights.findIndex(function(element){return element.date.weekday() == 0})
    // same for last night of the set
    var toIndex = nights.length - nights.slice().reverse().findIndex(function(element){return element.date.weekday() == 6})

    var weeks = nights.slice(fromIndex,toIndex)

    for (var i = 0; i < weeks.length; i=i+7) {
        sum = 0
        for (var j = 0; j < 6; j++) {
            sum = sum + weeks[i+j].amount.asHours()
        }
        myData.push(sum / 7)
        myLabels.push(weeks[i].date.week())
    }

    var ctx = $("#chartCanvas");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: myLabels,
            datasets: [{
                data: myData
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'category'
                }],
                yAxes: [{
                    ticks: {
                        suggestedMin: 3,
                        suggestedMax: 10,
                        stepSize: 1
                    }
                }]
            }
        }
    });
}

function createPlacesPie(){
    $.getJSON('http://localhost:5000/api/nights/stats?q=places_repartition', function(data){
        var labels = data['stats']['places_repartition']['labels']
        var data = data['stats']['places_repartition']['values']

        var ctx = $("#placesCanvas")
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data
                }]
            },
            options: {'legend':{'display':false}}
        })
    });
}

function NightsViewModel() {
    var self = this

    self.nights = ko.observableArray()
    $.getJSON('http://localhost:5000/api/nights?nlast=10', function(data){
        data['nights'].forEach(function(n,i,array){
            self.nights.push({
                id: n.id,
                alone: n.alone,
                place_id: n.place_id,
                begin: moment(n.begin),
                end: moment(n.end),
                amount: moment.duration(n.amount),
                date: moment(n.date)
            })
        })
    })

    self.add = function(n) {
        self.nights.shift()

        self.nights.push({
            id: n.id,
            alone: n.alone,
            place_id: n.place_id,
            begin: moment(n.begin),
            end: moment(n.end),
            amount: moment.duration(n.amount),
            date: moment(n.date)
        })
    }
}

function AddViewModel() {
    var self = this

    self.beginInput = ko.observable()
    self.endInput = ko.observable()
    self.amount = ko.observable()
    self.wasAlone = ko.observable(false)
    self.sleepless = ko.observable(false)
    self.selectedPlace = ko.observable()
    self.places = ko.observableArray()

    self.beginInput.subscribe(function (newValue) {
        if (moment(newValue).isValid()) {
            addViewModel.updateAmount();
        }
    });
    self.endInput.subscribe(function (newValue) {
        if (moment(newValue).isValid()) {
            addViewModel.updateAmount();
        }
    });

    $.getJSON('http://localhost:5000/api/places', function(data){
        data['places'].forEach(function(p,i,array){
            self.places.push({
                id: ko.observable(p.id),
                name: ko.observable(p.name)
            })
        })
    })

    self.validAdd = function() {
        $("#creation").modal('hide')
        var night = {
            begin: moment(self.beginInput()).format(),
            end: moment(self.endInput()).format(),
            date: moment(self.endInput()).startOf('day').format(),
            amount: self.amount(),
            sleepless: self.sleepless(),
            alone: self.wasAlone(),
            place_id: self.selectedPlace().id()
        }

        console.log(night);

        /*$.ajax({
            url: 'http://localhost:5000/api/nights',
            type:"POST",
            data: JSON.stringify(night),
            contentType:"application/json",
            dataType:"json",
            success: function(data){
                nightsViewModel.add(data['night'])
            }
        })*/
    }

    self.updateAmount = function() {
        var newDuration = moment.duration(moment(self.endInput()) - moment(self.beginInput()))
        console.log("new duration amount:",newDuration.toJSON());
        self.amount(newDuration.toJSON())
    }
}

var nightsViewModel = new NightsViewModel()
ko.applyBindings(nightsViewModel, $("#table")[0])

var addViewModel = new AddViewModel()
addViewModel.updateAmount()
ko.applyBindings(addViewModel, $("#creation")[0])
