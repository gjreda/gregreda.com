/*
* Generating various types of distributions
* illustrating that not all averages are the same
* and that the distribution matters greatly
****************************************************/

// constants
var n = 10000;
var mean = 0.65;
var floor = 0;
var n_bins = 100;

// generate array of random values for distributions
var logNormalValues = d3.range(n).map(d3.random.logNormal(Math.log(mean), 0.5));
var normalValues = d3.range(n).map(d3.random.normal(d3.mean(logNormalValues), 1));

// formatting functions
var formatCount = d3.format(",.0f"),
    formatPercent = function(d) { return (d * 100).toFixed(2) + "%"; };

// dynamically generate chart width
var parentWidth = $(".article-content").innerWidth();
var margin = {top: 20, right: 50, bottom: 20, left: 50},
    width = parentWidth - margin.left - margin.right,
    height = (parentWidth/2.0) - margin.top - margin.bottom;


// function to draw histogram for a given array of values
var drawHistogram = function(elementId, values) {

  // setup axes scales
  var x = d3.scale.linear().domain([0, 100]).range([0, width]);

  // generate histogram with uniformly spaced bins
  var data = d3.layout.histogram().bins(x.ticks(n_bins))(values);

  // add 500 to leave some spacing for "Mean" label at top left of chart
  var y = d3.scale.linear()
      .domain([0, d3.max(data, function(d) { return d.y })])
      .range([height, 0]);

  var xAxis = d3.svg.axis().scale(x).orient("bottom");
  var yAxis = d3.svg.axis().scale(y).orient("left");

  var svg = d3.select(elementId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr('transform', "translate(" + margin.left + "," + margin.top +")");

  var bar = svg.selectAll(".bar")
        .data(data)
      .enter().append("g")
        .attr("class", "bar")
        .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

  bar.append("rect")
      .attr("x", 1)
      .attr("width", x(data[0].dx) - 1)
      .attr("height", function(d) { return height - y(d.y); });

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  // summary statistics for distribution (top right corner)
  var summaryTextArea = svg.append("text")
      // .attr("class", "mouseover-text")
      .attr("x", 0)
      .attr("y", 0)
      .text("Mean: " + formatCount(d3.mean(values)));

  // mouseover text (top left corner)
  // var mouseoverTextArea = svg.append("text")
  //     .attr("class", "mouseover-text")
  //     .attr("x", width - 125)
  //     .attr("y", height - 10)
  //     .on("mouseover", function() { focus.style("display", null); })
  //     .on("mouseout", function() { focus.style("display", "none"); })
  //     .on("mousemove", mousemove);

};

drawHistogram("#normalDistribution", normalValues);
drawHistogram("#logNormalDistribution", logNormalValues);
