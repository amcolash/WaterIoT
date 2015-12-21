$(document).ready(function() {
  var options = {
      chart: {
        renderTo: 'chart',
        type: 'spline',
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        series: {
          lineWidth: 4
        }
      },
      rangeSelector: {
        buttons: [{
        	type: 'week',
        	count: 1,
        	text: '1w'
        }, {
        	type: 'month',
        	count: 1,
        	text: '1m'
        }, {
        	type: 'month',
        	count: 3,
        	text: '3m'
        }, {
        	type: 'month',
        	count: 6,
        	text: '6m'
        }, {
        	type: 'year',
        	count: 1,
        	text: '1y'
        }, {
        	type: 'all',
        	text: 'All'
        }]
      },
      series: [{}],
      title: {
        text: 'Recent Water Hydration'
      },
      tooltip: {
        xDateFormat: '%A, %B %d, %I:%M%p'
      },
      xAxis: {
        dateTimeLabelFormats: {
        	millisecond: '%I:%M:%S.%L',
        	second: '%I:%M:%S',
        	minute: '%I:%M%p',
        	hour: '%I:%M%p',
        	day: '%e. %b',
        	week: '%e. %b',
        	month: '%b \'%y',
        	year: '%Y'
        },
        type: 'datetime',
        title: {
          text: 'Date'
        }
      },
      yAxis: {
        // labels: {
        //   formatter: function() {
        //     return this.value == 1 ? 'Wet' : 'Dry';
        //   }
        // },
        min: 0,
        max: 1,
        tickInterval: 0.2,
        title: {
          text: null
        }
      }
  };

  Highcharts.setOptions({
    global: {
      useUTC: false
    }
  });

  // Don't cache the json :)
  $.ajaxSetup({
    cache:false
  });

  $.getJSON('data.json', function(data) {
    var series = [];

    // Store some stats while parsing through
    var lastStatus;
    var lastWet;
    var lastDry;
    $.each(data, function(key, value) {
      series.push([Date.parse(key), value]);
      lastStatus = value;

      if (value == 1) {
        lastWet = key;
      }

      if (value == 0) {
        lastDry = key;
      }
    });

    $('#current').text(lastStatus ? 'Wet' : 'Dry');
    if (lastWet != null && lastWet != undefined) {
      $('#lastWet').text(new Date(lastWet).toLocaleString());
    } else {
      $('#lastWet').text('Not enough data');
    }

    if (lastDry != null && lastDry != undefined) {
      $('#lastDry').text(new Date(lastDry).toLocaleString());
    } else {
      $('#lastDry').text('Not enough data');
    }

    options.series[0].data = series;
    options.series[0].color = '#449944';
    options.series[0].name = 'Water Value';
    var chart = new Highcharts.StockChart(options);
  });

});
