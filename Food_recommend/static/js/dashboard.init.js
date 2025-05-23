$(function () {
    $('[data-plugin="knob"]').knob()
});
var options = {
    chart: {height: 350, type: "area", toolbar: {show: !1}},
    colors: ["#3051d3", "#e4cc37"],
    dataLabels: {enabled: !1},
    series: [{name: "2018", data: [41, 47, 32, 75, 63, 35, 42, 20, 6, 15, 27, 39]}, {
        name: "2019",
        data: [35, 41, 62, 45, 14, 18, 29, 57, 28, 49, 35, 27]
    }],
    grid: {yaxis: {lines: {show: !1}}},
    stroke: {width: 3, curve: "stepline"},
    markers: {size: 0},
    xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        title: {text: "Month"}
    },
    fill: {type: "gradient", gradient: {shadeIntensity: 1, opacityFrom: .7, opacityTo: .9, stops: [0, 90, 100]}},
    legend: {position: "top", horizontalAlign: "right", floating: !0, offsetY: -25, offsetX: -5}
};
(chart = new ApexCharts(document.querySelector("#yearly-sale-chart"), options)).render();
options = {
    chart: {height: 350, type: "rangeBar", toolbar: {show: !1}},
    plotOptions: {bar: {horizontal: !0, barHeight: "12%"}},
    series: [{
        data: [{
            x: "Jack",
            y: [new Date("2020-01-02").getTime(), new Date("2020-01-04").getTime()],
            fillColor: "#3051d3"
        }, {
            x: "Thomas",
            y: [new Date("2020-01-04").getTime(), new Date("2020-01-08").getTime()],
            fillColor: "#e4cc37"
        }, {
            x: "David",
            y: [new Date("2020-01-08").getTime(), new Date("2020-01-12").getTime()],
            fillColor: "#F06543"
        }, {x: "James", y: [new Date("2020-01-12").getTime(), new Date("2020-01-18").getTime()], fillColor: "#4CB944"}]
    }],
    xaxis: {type: "datetime", axisBorder: {show: !1}}
};
(chart = new ApexCharts(document.querySelector("#activity-chart"), options)).render();
var chart;
options = {
    chart: {height: 270, type: "radialBar"},
    plotOptions: {
        radialBar: {
            hollow: {margin: 5, size: "38%"},
            track: {margin: 12},
            dataLabels: {
                name: {fontSize: "18px", offsetY: "-10"},
                value: {fontSize: "16px", offsetY: "5"},
                total: {
                    show: !0, label: "Total", formatter: function (e) {
                        return 166
                    }
                }
            }
        }
    },
    colors: ["#3051d3", "#e4cc37", "#f06543"],
    series: [44, 55, 67],
    labels: ["Facebook", "Twitter", "Instagram"]
};
(chart = new ApexCharts(document.querySelector("#radial-chart"), options)).render(), $("#usa-map").vectorMap({
    map: "usa_en",
    enableZoom: !0,
    showTooltip: !0,
    selectedColor: null,
    hoverColor: "#eaf0f1",
    backgroundColor: "transparent",
    color: "#f4f8f9",
    borderColor: "#7c8a96",
    colors: {ca: "#385ded", tx: "#385ded", mt: "#385ded", ny: "#385ded"},
    onRegionClick: function (e, t, a) {
        e.preventDefault()
    }
});