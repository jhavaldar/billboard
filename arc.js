var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

/*
 * value accessor - returns the value to encode for a given data object.
 * scale - maps value to a visual display encoding, such as a pixel position.
 * map function - maps from data value to display value
 * axis - sets up axis
 */


var bxValue = function(d) {return d.date;};
var bxScale = d3.time.scale().range([0,width]);
var bxMap = function(d) {return bxScale(bxValue(d));};
var bxAxis = d3.svg.axis().scale(bxScale).orient("bottom");

// setup y
var byValue = function(d) {return 100-d.chart;}; // data -> value
var byScale = d3.scale.linear().range([height,1]);
var byMap = function(d) { return byScale(byValue(d)); }; // data -> display
var byAxis = d3.svg.axis().scale(byScale).orient("left");

// setup fill color
var cValue = function(d) { return d.artist;},
    color = d3.scale.category20();

// add the graph canvas to the body of the webpage
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// add the tooltip area to the webpage
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

function parse_lengths(length) {
  var res = length.split(":");
  var mins = +res[0];
  var sec= +res[1];
  var ret = mins*60.0+sec;
  return ret;
}

function sortByDateAscending(a, b) {
    // Dates will be cast to numbers automagically:
    return a['date'] - b['date'];
}

d3.json("result_v3.json", function (data) {

  // Replace each date with a date object
  data.forEach(function(d) {
    var history = d['history'];
    // Parse the dates for every entry in the history object
    for(var i = 0; i < history.length; i++) {
      var splits = history[i]['date'].split("-");
      var month = splits[0];
      var day = splits[1];
      var year = splits[2];
      history[i]['date'] = new Date(year,month,day);
    }
    //Sort entries in the history object by date
    history = history.sort(sortByDateAscending);

    var minDate = d3.min(history, bxValue);
    var minChart = d3.min(history, byValue);
    var maxDate = d3.max(history, bxValue);
    var maxChart = d3.max(history, byValue);
    d.minDate = minDate;
    d.maxDate = maxDate;
    d.minChart = minChart;
    d.maxChart = maxChart;
    console.log(d.artist + "|" + d.minChart);
  });

  var day = 86400000;
  // Don't want dots overlapping the axis soooo
  bxScale.domain([d3.min(data, function(d) {return new Date(d.minDate)-day;}), d3.max(data, function(d) {return new Date(d.maxDate)})]);
  byScale.domain([d3.min(data, function(d) {return d.minChart;})-1, d3.max(data, function(d) {return d.maxChart;})+1]);

  // x-axis
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(bxAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("Date");

  // y-axis
  svg.append("g")
      .attr("class", "y axis")
      .call(byAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Chart");

  var lineFunction = d3.svg.line()
      .x(function(d) { return bxScale(d.date); })
      .y(function(d) { return byScale(d.chart); })
      .interpolate("monotone");

  svg.selectAll(".dot")
      .data(data)
    .enter().append("path")
      .attr("d", function(d) {console.log(d.history); return lineFunction(d.history); })
      .attr("stroke-width", 2)
      .attr("stroke", function(d) { return color(cValue(d));})
      .attr("fill", "none");

    /*

  svg.selectAll(".dot")
      .data(data)
    .enter().append("g")
      .style("fill", function(d) { return color(cValue(d));})
      .selectAll("circle")
        .data(function(d) {return d.history; })
      .enter().append("circle")
        .attr("class", "dot")
        .attr("r", 2.5)
        .attr("cx", bxMap)
        .attr("cy", byMap)
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", .9);
          tooltip.html(d.artist + "<br/> (" + bxValue(d)
          + ", " + byValue(d) + ")")
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
      });*/

  d3.select("body").selectAll("ul")
      .data(data)
    .enter().append("ul")
      .text(function(d) { return d.track; })
      .selectAll("li")
        .data(function(d) { return d.history; })
      .enter().append("li")
        .text(function(d) { return String(d.date) + ":" + d.chart })
        .style("background-color", function(d, i) { return i % 2 ? "#eee" : "#ddd"; });


});
