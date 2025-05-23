if ($("#overlapping-bars").length) {
    var data = {
        labels: ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        series: [[8, 6, 9, 6, 8, 6, 3, 6, 7, 10, 9, 7], [7, 5, 4, 5, 7, 3, 4, 5, 4, 6, 8, 5]]
    }, options = {seriesBarDistance: 10}, responsiveOptions = [["screen and (max-width: 640px)", {
        seriesBarDistance: 5,
        axisX: {
            labelInterpolationFnc: function (e) {
                return e[0]
            }
        }
    }]];
    new Chartist.Bar("#overlapping-bars", data, options, responsiveOptions)
}
$("#stacked-bar-chart").length && new Chartist.Bar("#stacked-bar-chart", {
    labels: ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"],
    series: [[8e5, 12e5, 14e5, 13e5, 152e4, 14e5], [2e5, 4e5, 5e5, 3e5, 452e3, 5e5], [16e4, 29e4, 41e4, 6e5, 588e3, 41e4]]
}, {
    stackBars: !0, axisY: {
        labelInterpolationFnc: function (e) {
            return e / 1e3 + "k"
        }
    }, plugins: [Chartist.plugins.tooltip()]
}).on("draw", function (e) {
    "bar" === e.type && e.element.attr({style: "stroke-width: 30px"})
}), $("#animating-donut").length && ((chart = new Chartist.Pie("#animating-donut", {
    series: [70, 30, 40, 40, 20, 30, 10],
    labels: [1, 2, 3, 4, 5, 6, 7]
}, {donut: !0, showLabel: !1, plugins: [Chartist.plugins.tooltip()]})).on("draw", function (e) {
    if ("slice" === e.type) {
        var t = e.element._node.getTotalLength();
        e.element.attr({"stroke-dasharray": t + "px " + t + "px"});
        var a = {
            "stroke-dashoffset": {
                id: "anim" + e.index,
                dur: 1e3,
                from: -t + "px",
                to: "0px",
                easing: Chartist.Svg.Easing.easeOutQuint,
                fill: "freeze"
            }
        };
        0 !== e.index && (a["stroke-dashoffset"].begin = "anim" + (e.index - 1) + ".end"), e.element.attr({"stroke-dashoffset": -t + "px"}), e.element.animate(a, !1)
    }
}), chart.on("created", function () {
    window.__anim21278907124 && (clearTimeout(window.__anim21278907124), window.__anim21278907124 = null), window.__anim21278907124 = setTimeout(chart.update.bind(chart), 1e4)
}));
if ($("#smil-animations").length) {
    var chart = new Chartist.Line("#smil-animations", {
        labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        series: [[12, 9, 7, 8, 5, 4, 6, 2, 3, 3, 4, 6], [4, 5, 3, 7, 3, 5, 5, 3, 4, 4, 5, 5], [5, 3, 4, 5, 6, 3, 3, 4, 5, 6, 3, 4], [3, 4, 5, 6, 7, 6, 4, 5, 6, 7, 6, 3]]
    }, {low: 0, plugins: [Chartist.plugins.tooltip()]}), seq = 0, delays = 80, durations = 500;
    chart.on("created", function () {
        seq = 0
    }), chart.on("draw", function (e) {
        if (seq++, "line" === e.type) e.element.animate({
            opacity: {
                begin: seq * delays + 1e3,
                dur: durations,
                from: 0,
                to: 1
            }
        }); else if ("label" === e.type && "x" === e.axis) e.element.animate({
            y: {
                begin: seq * delays,
                dur: durations,
                from: e.y + 100,
                to: e.y,
                easing: "easeOutQuart"
            }
        }); else if ("label" === e.type && "y" === e.axis) e.element.animate({
            x: {
                begin: seq * delays,
                dur: durations,
                from: e.x - 100,
                to: e.x,
                easing: "easeOutQuart"
            }
        }); else if ("point" === e.type) e.element.animate({
            x1: {
                begin: seq * delays,
                dur: durations,
                from: e.x - 10,
                to: e.x,
                easing: "easeOutQuart"
            },
            x2: {begin: seq * delays, dur: durations, from: e.x - 10, to: e.x, easing: "easeOutQuart"},
            opacity: {begin: seq * delays, dur: durations, from: 0, to: 1, easing: "easeOutQuart"}
        }); else if ("grid" === e.type) {
            var t = {
                begin: seq * delays,
                dur: durations,
                from: e[e.axis.units.pos + "1"] - 30,
                to: e[e.axis.units.pos + "1"],
                easing: "easeOutQuart"
            }, a = {
                begin: seq * delays,
                dur: durations,
                from: e[e.axis.units.pos + "2"] - 100,
                to: e[e.axis.units.pos + "2"],
                easing: "easeOutQuart"
            }, i = {};
            i[e.axis.units.pos + "1"] = t, i[e.axis.units.pos + "2"] = a, i.opacity = {
                begin: seq * delays,
                dur: durations,
                from: 0,
                to: 1,
                easing: "easeOutQuart"
            }, e.element.animate(i)
        }
    }), chart.on("created", function () {
        window.__exampleAnimateTimeout && (clearTimeout(window.__exampleAnimateTimeout), window.__exampleAnimateTimeout = null), window.__exampleAnimateTimeout = setTimeout(chart.update.bind(chart), 12e3)
    })
}
if ($("#simple-line-chart").length && new Chartist.Line("#simple-line-chart", {
    labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    series: [[12, 9, 7, 8, 5], [2, 1, 3.5, 6.5, 3], [1, 4, 1, 5, 7]]
}, {fullWidth: !0, chartPadding: {right: 40}, plugins: [Chartist.plugins.tooltip()]}), $("#scatter-diagram").length) {
    var times = function (e) {
        return Array.apply(null, new Array(e))
    };
    data = times(52).map(Math.random).reduce(function (e, t, a) {
        return e.labels.push(a + 1), e.series.forEach(function (e) {
            e.push(100 * Math.random())
        }), e
    }, {
        labels: [], series: times(4).map(function () {
            return new Array
        })
    }), options = {
        showLine: !1, axisX: {
            labelInterpolationFnc: function (e, t) {
                return t % 13 == 0 ? "W" + e : null
            }
        }
    }, responsiveOptions = [["screen and (min-width: 640px)", {
        axisX: {
            labelInterpolationFnc: function (e, t) {
                return t % 4 == 0 ? "W" + e : null
            }
        }
    }]];
    new Chartist.Line("#scatter-diagram", data, options, responsiveOptions)
}
if ($("#chart-with-area").length && new Chartist.Line("#chart-with-area", {
    labels: [1, 2, 3, 4, 5, 6, 7, 8],
    series: [[5, 9, 7, 8, 5, 3, 5, 4]]
}, {low: 0, showArea: !0, plugins: [Chartist.plugins.tooltip()]}), $("#simple-pie").length) {
    data = {series: [7, 5, 4]};
    var sum = function (e, t) {
        return e + t
    };
    new Chartist.Pie("#simple-pie", data, {
        labelInterpolationFnc: function (e) {
            return Math.round(e / data.series.reduce(sum) * 100) + "%"
        }
    })
}