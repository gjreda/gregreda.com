var path = "/data/movie-releases.tsv"

// dynamically generate chart width
var parentWidth = $(".article-content").innerWidth();

var margin = {top: 20, right: 50, bottom: 20, left: 50},
  width = parentWidth - margin.left - margin.right,
  height = (parentWidth/2.0) - margin.top - margin.bottom;

var monthNames = [ "Jan.", "Feb.", "Mar.", "Apr.", "May", "June",
  "July", "Aug.", "Sep.", "Oct.", "Nov.", "Dec." ];

var parseDate = d3.time.format("%Y-%m").parse,
  bisectDate = d3.bisector(function(d) { return d.release_date; }).left,
  formatPercent = function(d) { return (d * 100).toFixed(2) + "%"; },
  formatDate = function(d) { return monthNames[d.getMonth()] + " " + d.getFullYear(); };

var x = d3.time.scale().range([0, width]);
var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis().scale(x).orient("bottom");
var yAxis = d3.svg.axis().scale(y).orient("left");

var line = d3.svg.line()
  .x(function(d) { return x(d.release_date); })
  .y(function(d) { return y(d.cumulative); });

var svg = d3.select("#vis").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.tsv(path, function(error, data) {
data.forEach(function(d) {
  d.release_date = parseDate(d.release_date);
  d.percentage = +d.percentage;
  d.cumulative = +d.cumulative;
});

x.domain(d3.extent(data, function(d) { return d.release_date; }));
y.domain(d3.extent(data, function(d) { return d.cumulative; }));

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
  .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("% of total films");

svg.append("path")
    .datum(data)
    .attr("class", "line")
    .attr("d", line);

// draw bar chart
// svg.selectAll(".bar")
//     .data(data)
//   .enter().append("rect")
//     .attr("class", "bar")
//     .attr("x", function(d) { return x(d.release_date); })
//     .attr("width", "3px")
//     .attr("y", function(d) { return y(d.percentage); })
//     .attr("height", function(d){ return height - y(d.percentage); });

// mouseover labels
var focus = svg.append("g")
    .attr("class", "focus")
    .style("display", "none");

focus.append("circle")
    .attr("r", 4.5);

focus.append("text")
    .attr("x", 9)
    .attr("dy", ".35em");

svg.append("rect")
    .attr("class", "overlay")
    .attr("width", width)
    .attr("height", height)
    .on("mouseover", function() { focus.style("display", null); })
    .on("mouseout", function() { focus.style("display", "none"); })
    .on("mousemove", mousemove);

var textArea = svg.append("text")
    .attr("class", "mouseover-text")
    .attr("x", width - 125)
    .attr("y", height - 10)
    .on("mouseover", function() { focus.style("display", null); })
    .on("mouseout", function() { focus.style("display", "none"); })
    .on("mousemove", mousemove);

function mousemove() {
  var x0 = x.invert(d3.mouse(this)[0]),
      i = bisectDate(data, x0, 1),
      d0 = data[i - 1],
      d1 = data[i],
      d = x0 - d0.release_date > d1.release_date - x0 ? d1 : d0;
  focus.attr("transform", "translate(" + x(d.release_date) + "," + y(d.cumulative) + ")");
  // focus.select("text")
  //     .text(formatDate(d.release_date) + ": " + formatPercent(d.cumulative));
  textArea.text(formatDate(d.release_date) + ":  " + formatPercent(d.cumulative));
}
});