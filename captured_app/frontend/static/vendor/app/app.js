var APP;

var chartConfig = [{
    data: {
      type: 'line'
    },
    conf: {
      axis: {
        
          x: {
            type: 'category',
            categories: [30, 200, 100, 400, 150, 250]
          }
        
      },
      tooltip: {
        // format: {
          // title: function(d) { return 'Point ' + d; },
        // },
        // contents: function(data, defaultTitleFormat, defaultValueFormat, color) {
          // console.log(data, defaultTitleFormat, defaultValueFormat, color);
          // return '<span class="badge badge-dark">!!!</span>';
        // }
      }
    }
  },
  {},
  {},
  {
    conf: {}
  },
  {},
  {
    data: {
      type: 'scatter'
    }
  }
];

$(function() {
  APP = (function() {
    var charts = [];
    var init = function() {
      $chartParents = $('.charts');
      $chartParents.addClass('loading');

      _.each($chartParents, function(value, key) {
        generateChartSection(key);
      })
    };

    var generateChartSection = function(i) {
      var chartElement = $chartParents.eq(i);
      var chartData = getChartData(i);
      // var chartData = getChartData(i).done(function(data) {
        chartElement.removeClass('loading');

        if (charts[i] === undefined) charts[i] = [];
        if (Array.isArray(chartData)) {
          _.each(chartData, function(value, key) {
            charts[i].push(makeChart(chartElement.find('.chart').eq(key)[0], value, chartConfig[i]));
          });
        } else charts[i].push(makeChart(chartElement.find('.chart')[0], chartData, chartConfig[i]));
      // })

    };

    var makeChart = function(chartElement, chartData, chartConfig) {
      return chart = bb.generate(_.extend(chartConfig.conf, {
        bindto: chartElement,
        data: _.extend(chartData, chartConfig.data)
      }));
    };

    var getChartData = function(i) {
      // return $.ajax({
      //   url: 'http://192.168.0.193/api/winners/' + i,
      //   // data: filters,
      //   // method: get,
      //   success: function (data) {
      //     $chartParents.eq(i).removeClass('loading');
      //     return data;
      //   }
      // });

      $chartParents.eq(i).removeClass('loading');

      switch (i) {
        case 1:
          return[{
            columns: [
              ['data1', 30, 200, 100, 400, 150, 250],
              ['data2', 50, 20, 10, 40, 15, 25]
            ]
          }, {
            columns: [
              ['data1', 30, 200, 100, 400, 150, 250],
              ['data2', 50, 20, 10, 40, 15, 25]
            ]
          }, {
            columns: [
              ['data1', 30, 200, 100, 400, 150, 250],
              ['data2', 50, 20, 10, 40, 15, 25]
            ]
          }, {
            columns: [
              ['data1', 30, 200, 100, 400, 150, 250],
              ['data2', 50, 20, 10, 40, 15, 25]
            ]
          }];
        break;

        case 3:
          return[{
            columns: [
              ['data1', 30, 200, 100, 400, 150, 250],
              ['data2', 50, 20, 10, 40, 15, 25]
            ]
          }, {
            columns: [
              ['data1', 30, 200, 100, 400, 150, 250],
              ['data2', 50, 20, 10, 40, 15, 25]
            ]
          }];
        break;

        default:
          return {
            columns: [
              ['data1', 30, 200, 100, 400, 150, 250],
              ['data2', 50, 20, 10, 40, 15, 25]
            ]
          };
        break;
      }
    };

    return {
      init: init,
      makeChart: makeChart
    }
  })();

  APP.init();
});