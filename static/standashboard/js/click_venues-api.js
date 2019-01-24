$(document).ready(function () {
    var title = $('#title').val();

    // Use the margin convention practice
    var div_width = document.querySelector("#div-venuedatetime")
        .getBoundingClientRect();

    var graph_width = div_width.right - div_width.left;
    var margin = {
            top: 30,
            right: 100,
            bottom: 50,
            left: 50
        },
        width = graph_width - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // Parse the dates which are in the format 2018-08-30
    var parseTime = d3.timeParse("%m/%d/%Y");

    // X scale using date 
    var x = d3.scaleTime().range([0, width]);

    // Y scale using close prices
    var y = d3.scaleLinear().rangeRound([height, 0]);

    // d3 line generator
    var line = d3.line()
        .x(function (d) {
            return x(d.impression_date);
        })
        .y(function (d) {
            return y(d.count);
        });

    // Add the SVG to the page and employ
    var svg = d3.select("#venue-datetime")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    var url = "http://" + window.location.hostname + ':' + window.location.port +
        '/standashboard/click-datetime/api/' + 'Kahawa' + '/';

    // Get the data for plotting
    d3.json(url).then(function (jsonData) {
        var data = JSON.parse(jsonData);
        data.forEach(function (d) {
            console.log(d.impression_date);
            // Converts the price_date string to a JavaScript Date Object
            d.impression_date = parseTime(d.impression_date);

            // Converts the closing_price from a string to a number.
            d.count = +d.count;
        });

        // set the domain of the x scale function
        x.domain(d3.extent(data, function (d) {
            return d.impression_date;
        }));

        y.domain([0, d3.max(data, function (d) {
            return d.count;
        })]);

        // Call the x axis in a group tag
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        // text label for the x axis
        svg.append("text")
            .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.top + 20) + ")")
            .style("text-anchor", "middle")
            .attr("font", "sans-serif")
            .attr("font-size", "12px")
            .attr("font-weight", "bold")
            .text("Date");

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
            .text("Daily Count");

        // Add a title to the graph
        svg.append("text")
            .attr("x", (width / 2))
            .attr("y", 0 - (margin.top / 2))
            .attr("text-anchor", "middle")
            .style("font-size", "14px")
            .attr("font", "sans-serif")
            .attr("font-weight", "bold")
            .text("Clicks per day");

        // Append the path, bind the data, and call the line generator
        svg.append("path")
            .datum(data) // Binds data to the line
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("shape-rendering", "crispEdges")
            .attr("class", "line")
            .attr("d", line); // Calls the line generator

        // Allow mouse over on the graph
        var focus = svg.append("g")
            .style("display", "none");

        // append the x line
        focus.append("line")
            .attr("class", "x")
            .style("stroke", "black")
            .style("stroke-dasharray", "3,3")
            .style("opacity", 1.5)
            .attr("y1", 0)
            .attr("y2", height);

        // append the y line
        focus.append("line")
            .attr("class", "y")
            .style("stroke", "black")
            .style("stroke-dasharray", "3,3")
            .style("opacity", 1.5)
            .attr("x1", width)
            .attr("x2", width);

        focus.append("circle")
            .attr("class", "y")
            .attr("r", 5.5)
            .attr("fill", "none")
            .attr("stroke", "black");

        // place the price at the intersection
        focus.append("text")
            .attr("class", "y1")
            .style("stroke", "white")
            .style("stroke-width", "3.5px")
            .style("opacity", 0.8)
            .attr("dx", 8)
            .attr("dy", "-.3em");

        focus.append("text")
            .attr("class", "y2")
            .attr("dx", 8)
            .attr("dy", "-.3em");

        // place the date at the intersection
        focus.append("text")
            .attr("class", "y3")
            .style("stroke", "white")
            .style("stroke-width", "3.5px")
            .style("opacity", 0.8)
            .attr("dx", 8)
            .attr("dy", "1em").attr("font", "sans-serif")
            .attr("font-size", "10px")
            .attr("font-weight", "bolder");

        focus.append("text")
            .attr("class", "y4")
            .attr("dx", 8)
            .attr("dy", "1em");

        svg.append("rect")
            .attr("fill", "none")
            .attr("pointer-events", "all")
            .attr("width", width)
            .attr("height", height)
            .on("mouseover", function () {
                focus.style("display", null);
            })
            .on("mouseout", function () {
                focus.style("display", "none");
            })
            .on("mousemove", mousemove);

        var bisectDate = d3.bisector(function (d) {
            return d.impression_date;
        }).left

        var formatDate = d3.timeFormat("%m/%d/%Y");

        var formatValue = d3.format(",.2f");
        var formatCurrency = function (d) {
            return "KES " + formatValue(d);
        };

        function mousemove() {
            var x0 = x.invert(d3.mouse(this)[0]),
                i = bisectDate(data, x0, 1),
                d0 = data[i - 1],
                d1 = data[i],
                d = x0 - d0.impression_date > d1.impression_date - x0 ? d1 : d0;

            focus.select("circle.y")
                .attr("transform", "translate(" + x(d.impression_date) + "," + y(d.count) + ")");

            focus.select("text.y1")
                .attr("transform", "translate(" + x(d.impression_date) + "," + y(d.count) + ")")
                .attr("font", "sans-serif")
                .attr("font-size", "10px")
                .attr("font-weight", "1000")
                .text(d.count);

            focus.select("text.y2")
                .attr("transform", "translate(" + x(d.impression_date) + "," + y(d.count) + ")")
                .attr("font", "sans-serif")
                .attr("font-size", "10px")
                .attr("font-weight", "1000")
                .text(d.count);

            focus.select("text.y3").attr("transform", "translate(" + x(d.impression_date) + "," + y(d.count) + ")")
                .attr("font", "sans-serif")
                .attr("font-size", "10px")
                .attr("font-weight", "1000")
                .text(formatDate(d.impression_date));

            focus.select("text.y4").attr("transform", "translate(" + x(d.impression_date) + "," + y(d.count) + ")")
                .attr("font", "sans-serif")
                .attr("font-size", "10px")
                .attr("font-weight", "1000")
                .text(formatDate(d.impression_date));

            focus.select(".x")
                .attr("transform", "translate(" + x(d.impression_date) + "," + y(d.count) + ")")
                .attr("y2", height - y(d.count));

            focus.select(".y")
                .attr("transform", "translate(" + width * -1 + "," + y(d.count) + ")")
                .attr("x2", width + width);
        }
    });

    function updateGraph(section) {
        var url = "http://" + window.location.hostname + ':' + window.location.port +
            '/standashboard/click-datetime/api/' + section + '/';
        d3.json(url).then(function (updatedJsonData) {
            var updatedData = JSON.parse(updatedJsonData);
            updatedData.forEach(function (d) {
                console.log(d.impression_date);
                // Converts the price_date string to a JavaScript Date Object
                d.impression_date = parseTime(d.impression_date);

                // Converts the closing_price from a string to a number.
                d.count = +d.count;
            });

            // set the domain of the x scale function
            x.domain(d3.extent(updatedData, function (d) {
                return d.impression_date;
            }));

            y.domain([0, d3.max(updatedData, function (d) {
                return d.count;
            })]);

            var svg = d3.select("#venue-datetime").transition();

            svg.select(".line")
                .duration(1000)
                .attr("d", line(updatedData)); // Calls the line generator

            // Call the x axis in a group tag
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            // Call the y axis in a group tag
            svg.append("g")
                .call(d3.axisLeft(y));
        });
    }

    d3.select('#inds')
        .on("change", function () {
            var sect = document.getElementById("inds");
            var section = sect.options[sect.selectedIndex].value;
            console.log(section);
            updateGraph(section);
        });
})