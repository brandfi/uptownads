$(document).ready(function () {
    // Use the margin convention practice
    var div_width = document.querySelector("#div-clickads")
        .getBoundingClientRect().width;

    var margin = {
            top: 30,
            right: 20,
            bottom: 100,
            left: 40
        },
        width = div_width - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    var x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
    var y = d3.scaleLinear().rangeRound([height, 0]);

    var svg = d3.select("#adsclicks")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var url = "http://" + window.location.hostname + ':' + window.location.port + '/standashboard/total-clicks-api/';

    d3.json(url).then(function (data) {
        var jsonData = JSON.parse(data);
        jsonData.forEach(function (d) {
            d.title = d.title;
            d.count = +d.count;
        });

        // scale the range of the data
        x.domain(jsonData.map(function (d) {
            return d.title;
        }));

        y.domain([0, d3.max(jsonData, function (d) {
            return d.count;
        })]);

        // Call the x axis in a group tag
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".100em")
            .attr("transform", "rotate(90)")
            .attr("font", "sans-serif")
            .attr("font-size", "12px")
            .attr("font-weight", "bold")
            .style("text-anchor", "start");

        // text label for the x axis
        svg.append("text")
            .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.top + 30) + ")")
            .style("text-anchor", "middle")
            .attr("font", "sans-serif")
            .attr("font-size", "12px")
            .attr("font-weight", "bold")
            .text("Ad Title");

        // Call the y axis in a group tag
        svg.append("g")
            .call(d3.axisLeft(y));

        // text label for the y axis
        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left)
            .attr("x", 0 - (height / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .attr("font", "sans-serif")
            .attr("font-size", "12px")
            .attr("font-weight", "bold")
            .text("Total Count");

        svg.selectAll(".bar")
            .data(jsonData)
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("x", function (d) {
                return x(d.title);
            })
            .attr("y", function (d) {
                return y(d.count);
            })
            .attr("width", x.bandwidth())
            .attr("height", function (d) {
                return height - y(d.count);
            });


        // Add a title to the graph
        svg.append("text")
            .attr("x", (width / 2))
            .attr("y", 0 - (margin.top / 2))
            .attr("text-anchor", "middle")
            .style("font-size", "14px")
            .attr("font", "sans-serif")
            .attr("font-weight", "bold")
            .text("Clicks per Ad");

    });
});