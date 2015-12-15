$(document).ready(function() {
  var options = {
      chart: {
        renderTo: 'chart',
        type: 'spline',
      },
      plotOptions: {
        line: {
          marker: {
            enabled: true
          }
        }
      },
      title: {
        text: 'Recent Water Values'
      },
      xAxis: {
        type: 'datetime',
        title: {
          text: 'Date'
        }
      },
      yAxis: {
        labels: {
          formatter: function() {
            return this.value == 1 ? 'Wet' : 'Dry';
          }
        },
        min: 0,
        max: 1,
        tickInterval: 1,
        title: {
          text: null
        }
      },
      legend: {
        enabled: false
      },
      series: [{}]
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
    $('#lastWet').text(lastWet);
    $('#lastDry').text(lastDry);

    options.series[0].data = series;
    options.series[0].color = '#449944';
    options.series[0].name = 'Water Value';
    var chart = new Highcharts.Chart(options);
  });

});
