$.getJSON('http://localhost:5000/api/nights', function(data){
    var nights = data['nights']
    nights.forEach(function(e,i,a){
        a[i].begin = moment(e.begin)
        a[i].to_rise = moment(e.to_rise)
        a[i].amount = moment.duration(e.amount)
    })
    createCharts(nights)
});

function createCharts(nights) {

    createWeeklyMean(nights)
    //createPlacesPie(nights)
}

function createWeeklyMean(nights) {
    var myLabels = []
    var myData = []

    // first night from the set might not be at the beginning of a week
    var fromIndex = nights.findIndex(function(element){return element.to_rise.weekday() == 0})
    // same for last night of the set
    var toIndex = nights.length - nights.slice().reverse().findIndex(function(element){return element.to_rise.weekday() == 6})

    var weeks = nights.slice(fromIndex,toIndex)

    for (var i = 0; i < weeks.length; i=i+7) {
        sum = 0
        for (var j = 0; j < 6; j++) {
            sum = sum + weeks[i+j].amount.asHours()
        }
        myData.push(sum / 7)
        myLabels.push(weeks[i].to_rise.week())
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

ko.bindingHandlers.dateTimePicker = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        //initialize datepicker with some optional options
        var options = allBindingsAccessor().dateTimePickerOptions || {};
        $(element).datetimepicker(options);
        //when a user changes the date, update the view model
        ko.utils.registerEventHandler(element, "dp.change", function (event) {
            var value = valueAccessor();
            if (ko.isObservable(value)) {
                if (event.date != null && !(event.date instanceof Date)) {
                    value(event.date.toDate());
                } else {
                    value(event.date);
                }
            }
        });
        ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
            var picker = $(element).data("DateTimePicker");
            if (picker) {
                picker.destroy();
            }
        });
    },
    update: function (element, valueAccessor, allBindings, viewModel, bindingContext) {
        var picker = $(element).data("DateTimePicker");
        //when the view model is updated, update the widget
        if (picker && ko.utils.unwrapObservable(valueAccessor())) {
            var koDate = ko.utils.unwrapObservable(valueAccessor());

            //in case return from server datetime i am get in this form for example /Date(93989393)/ then fomat this
            koDate = (typeof (koDate) !== 'object') ? new Date(parseFloat(koDate.replace(/[^0-9]/g, ''))) : koDate;

            picker.date(koDate);
        }
    }
};

// enlever le moment() du data-bind
// changer les valeurs des champs lorsqu'on affiche les dateTimePicker
// avec un bind sur le bouton 'show'

function NightsViewModel() {
    var self = this

    self.nights = ko.observableArray()
    $.getJSON('http://localhost:5000/api/nights?nlast=10', function(data){
        data['nights'].forEach(function(n,i,array){

            var rise = moment(n.to_rise)

            self.nights.push({
                id: n.id,
                alone: n.alone,
                place_id: n.place_id,
                begin: moment(n.begin),
                to_rise: rise,
                amount: moment.duration(n.amount),
                date: rise.startOf('day')
            })
        })
    })

    self.add = function(n) {
        var rise = moment(n.to_rise)

        self.nights.shift()

        self.nights.push({
            id: n.id,
            alone: n.alone,
            place_id: n.place_id,
            begin: moment(n.begin),
            to_rise: rise,
            amount: moment.duration(n.amount),
            date: rise.startOf('day')
        })
    }
}

function AddViewModel() {
    var self = this

    var now = moment()
    now.seconds(0).milliseconds(0)

    self.beginInput = ko.observable(now.toDate())
    self.endInput = ko.observable(now.add(1,'h').toDate())
    self.amount = ko.observable()
    self.wasAlone = ko.observable(false)
    self.selectedPlace = ko.observable()
    self.places = ko.observableArray()

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
            to_rise: moment(self.endInput()).format(),
            amount: self.amount(),
            alone: self.wasAlone(),
            place_id: self.selectedPlace().id()
        }
        $.ajax({
            url: 'http://localhost:5000/api/nights',
            type:"POST",
            data: JSON.stringify(night),
            contentType:"application/json",
            dataType:"json",
            success: function(data){
                nightsViewModel.add(data['night'])
            }
        })
    }

    self.updateAmount = function() {
        var newDuration = moment.duration(self.endInput() - self.beginInput())
        self.amount(newDuration.toJSON())
    }
}

var nightsViewModel = new NightsViewModel()
ko.applyBindings(nightsViewModel, $("#main")[0])

var addViewModel = new AddViewModel()
addViewModel.updateAmount()
ko.applyBindings(addViewModel, $("#creation")[0])

$("#beginInput").on("dp.change", function (e) {
    $('#endInput').data("DateTimePicker").minDate(e.date);
    addViewModel.updateAmount()
});
$("#endInput").on("dp.change", function (e) {
    $('#beginInput').data("DateTimePicker").maxDate(e.date);
    addViewModel.updateAmount()
});