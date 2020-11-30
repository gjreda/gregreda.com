Title: Finding the midpoint of film releases
Date: 2014-01-23
Slug: film-releases-midpoint
Tags: data science, movies, d3js, visualization
Description: Looking film release dates throughout history to determine the date that has an equal number of films made before and after it.

<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
<script src="http://d3js.org/d3.v3.min.js"></script>

<style>
.chart {
  font: 12px sans-serif;
}
.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}
.x.axis path {
  /*display: none;*/
}
.line {
  fill: none;
  stroke: steelblue;
  stroke-width: 1.5px;
}
.bar {
  fill: steelblue;
}
.overlay {
  fill: none;
  pointer-events: all;
}
.focus circle {
  fill: none;
  stroke: steelblue;
}
.mouseover-text {
  color: black;
  /*font-weight: bold;*/
  font-size: 14px;
}
</style>

> "We're talking about Thunderdome. It's from before you were born."

> "Most movies are from before I was born."

That statement spurred a pretty interesting question: *what's the date where that statement is no longer true?* Put another way, *what date in history has an equal number of films made before and after it?*

My birthday, November 4, 1985, *felt* like a relatively safe date, but really, no one had a clue if what I said was true, including me. Guesses by about a dozen coworkers included dates from September 1963 all the way to September 2001.

Knowing that [IMDB](http://imdb.com) makes their [data publicly available](http://www.imdb.com/interfaces), I decided to find the actual date. Using the most current [releases.list file](ftp://ftp.fu-berlin.de/pub/misc/movies/database/release-dates.list.gz) (1/17/14 at the time of writing), I held the following assumptions:

1. Only films. The release-dates.list also includes TV shows and video games. It also includes movies that went straight to video - those count.

2. Films with a release date in the future do not count.

3. If the film was released multiple times (different release dates for different countries), use the earliest release date.

4. If only a release month and year were provided, assume the 15th of that month.

5. If only a release year was provided, assume [July 2nd](http://en.wikipedia.org/wiki/July_2) of that year.

The result?

<div id="vis" class="chart"></div>

May 15, 2002.

Of course, given the current rate at which films are being made, this analysis is already out of date.

For those interested, you can find the code [here](https://github.com/gjreda/movie-release-timeline).

<script>
var path = "/data/movie-releases.tsv"

// dynamically generate chart width
var parentWidth = $("#content").innerWidth();

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
  textArea.text(formatDate(d.release_date) + ":  " + formatPercent(d.cumulative));
}
});
</script>