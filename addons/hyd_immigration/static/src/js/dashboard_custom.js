odoo.define('hyd_immigration.Dashboard', function (require) {
    'use strict';

    var PjDashboard = require('pj_dashboard.Dashboard');
    var rpc = require('web.rpc');
    const { useListener } = require("@web/core/utils/hooks");
    var core = require('web.core');

    PjDashboard.include({

        render_project_task: function() {
            var self = this
            rpc.query({
                model: "project.project",
                method: "get_project_task_count",
            }).then(function(data) {
                var ctx = self.$("#project_doughnut");
                new Chart(ctx, {
                    type: "doughnut",
                    data: {
                        labels: data.project,
                        datasets: [{
                            backgroundColor: data.color,
                            data: data.task
                        }]
                    },
                    options: {
                        legend: {
                            position: 'left'
                        },
                        title: {
                            display: true,
                            position: "top",
                            text: "Repartition des procedures",
                            fontSize: 20,
                            fontColor: "#111"
                        },
                        cutoutPercentage: 40,
                        responsive: true,
                    }
                });
            })
        },

        render_top_employees_graph: function() {
            var self = this

            var ctx = self.$(".top_selling_employees");

            rpc.query({
                model: "project.task",
                method: 'get_task_amount',
            }).then(function(arrays) {


                var data = {
                    labels: arrays[1],
                    datasets: [{
                            label: "Hours Spent",
                            data: arrays[0],
                            backgroundColor: [
                                "rgba(190, 27, 75,1)",
                                "rgba(31, 241, 91,1)",
                                "rgba(103, 23, 252,1)",
                                "rgba(158, 106, 198,1)",
                                "rgba(250, 217, 105,1)",
                                "rgba(255, 98, 31,1)",
                                "rgba(255, 31, 188,1)",
                                "rgba(75, 192, 192,1)",
                                "rgba(153, 102, 255,1)",
                                "rgba(10,20,30,1)"
                            ],
                            borderColor: [
                                "rgba(190, 27, 75, 0.2)",
                                "rgba(190, 223, 122, 0.2)",
                                "rgba(103, 23, 252, 0.2)",
                                "rgba(158, 106, 198, 0.2)",
                                "rgba(250, 217, 105, 0.2)",
                                "rgba(255, 98, 31, 0.2)",
                                "rgba(255, 31, 188, 0.2)",
                                "rgba(75, 192, 192, 0.2)",
                                "rgba(153, 102, 255, 0.2)",
                                "rgba(10,20,30,0.3)"
                            ],
                            borderWidth: 1
                        },

                    ]
                };

                //options
                var options = {
                    responsive: true,
                    title: {
                        display: true,
                        position: "top",
                        text: "Depenses par procedures",
                        fontSize: 18,
                        fontColor: "#111"
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0
                            }
                        }]
                    }
                };
                //create Chart class object
                var chart = new Chart(ctx, {
                    type: 'bar',
                    data: data,
                    options: options
                });

            });
        },

        income_this_year: function() {
            var selected = $('.btn.btn-tool.income');
            var data = $(selected[0]).data();
            var posted = false;

            rpc.query({
                    model: 'project.project',
                    method: 'get_expense_this_year',
                    args: [],

                })
                .then(function(result) {

                    var ctx = document.getElementById("canvas").getContext('2d');

                    // Define the data
                    var income = result.income; // Add data values to array
                    //                    var expense = result.expense;
                    var profit = result.profit;

                    var labels = result.month; // Add labels to array


                    if (window.myCharts != undefined)
                        window.myCharts.destroy();
                    window.myCharts = new Chart(ctx, {
                        //var myChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Depenses', // Name the series
                                data: profit, // Specify the data values array
                                backgroundColor: '#0bd465',
                                borderColor: '#0bd465',

                                borderWidth: 1, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            },{
                                label: 'Honoraires', // Name the series
                                data: income, // Specify the data values array
                                backgroundColor: '#abf465',
                                borderColor: '#ccd465',

                                borderWidth: 1, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }]
                        },
                        options: {
                            responsive: true, // Instruct chart js to respond nicely.
                            maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        }
                    });

                })
        },

    });

    core.action_registry.add('project_dashboard', PjDashboard);
});
