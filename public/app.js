$(document).ready(function() {
  var options = {
      chart: {
        renderTo: 'chart',
        type: 'spline',
        height: 350
      },
      title: {
        text: 'Recent Watering'
      },
      xAxis: {
        type: 'datetime',
        title: {
          text: "Date"
        }
      },
      yAxis: {
        labels: {
          formatter: function() {
            return this.value == 1 ? "Wet" : "Dry";
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

  $.getJSON('data.json', function(data) {
    var series = [];

    // Store some stats while parsing through
    var lastStatus;
    var lastWet;
    var lastDry;
    $.each(data, function(key, value) {
      console.log(key + " : " + value);
      series.push([Date.parse(key), value]);
      lastStatus = value;

      if (value == 1) {
        lastWet = key;
      }

      if (value == 0) {
        lastDry = key;
      }
    });

    $('#current').text(lastStatus ? "Wet" : "Dry");
    $('#lastWet').text(lastWet);
    $('#lastDry').text(lastDry);

    options.series[0].data = series;
    var chart = new Highcharts.Chart(options);
  });

});
