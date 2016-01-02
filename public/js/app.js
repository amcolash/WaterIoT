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
        }],
        selected: 0 // choose 1 week previous
      },
      series: [{}],
      title: {
        text: 'Recent Water Hydration'
      },
      tooltip: {
        xDateFormat: '%A, %B %d, %l:%M%p'
        // formatter: function() {
        //   var date = new Date(this.x);
        //   return '<span>' + date + '</span>: ' + this.y + '%';
        // }
      },
      xAxis: {
        type: 'datetime',
        title: {
          text: 'Date'
        }
      },
      yAxis: {
        min: 0,
        max: 1,
        offset: 24,
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
      series.push([parseInt(key), value]);
      lastStatus = value;

      if (value > 0.8) {
        lastWet = key;
      }

      if (value < 0.2) {
        lastDry = key;
      }
    });

    $('#current').text((lastStatus * 100).toFixed(2) + '% (' + (lastStatus > 0.35 ? 'Wet' : 'Dry') + ')');
    if (lastWet != null && lastWet != undefined) {
      $('#lastWet').text(new Date(parseInt(lastWet)).toLocaleString());
    } else {
      $('#lastWet').text('Not enough data');
    }

    if (lastDry != null && lastDry != undefined) {
      $('#lastDry').text(new Date(parseInt(lastDry)).toLocaleString());
    } else {
      $('#lastDry').text('Not enough data');
    }

    // sort the dates because it doesn't seem like Python is doing it for us :/
    series.sort(function(a,b){
        if(a == b)
            return 0;
        if(a < b)
            return -1;
        if(a > b)
            return 1;
    });

    options.series[0].data = series;
    options.series[0].color = '#449944';
    options.series[0].name = 'Water Value';
    var chart = new Highcharts.StockChart(options);
  });

});
