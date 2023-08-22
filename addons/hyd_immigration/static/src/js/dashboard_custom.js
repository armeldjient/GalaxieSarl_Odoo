odoo.define('hyd_immigration.Dashboard', function (require) {
    'use strict';

    var PjDashboard = require('pj_dashboard.Dashboard');
    var rpc = require('web.rpc');
    const { useListener } = require("@web/core/utils/hooks");
    var core = require('web.core');
    var _t = core._t;

    var flag = 0;
    var tot_so = []
    var tot_project = []
    var tot_task = []

    PjDashboard.include({
        events: Object.assign({}, PjDashboard.prototype.events, {
            'click .tot_tasks_end': 'tot_tasks_end_method',
            'click .tot_tasks_cancel': 'tot_tasks_cancel_method',
        }),

        /**
        for opening project task view
        */
        tot_tasks_end_method: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            if (flag == 0) {
                this.do_action({
                    name: _t("Procedures terminees"),
                    type: 'ir.actions.act_window',
                    res_model: 'project.task',
                    view_mode: 'tree,kanban,form',
                    domain: [['stage_id.is_closed', '=', true]],
                    views: [
                        [false, 'list'],
                        [false, 'form']
                    ],
                    target: 'current'
                }, options)
            } else {
                if (tot_task) {
                    this.do_action({
                        name: _t("Procedures terminees"),
                        type: 'ir.actions.act_window',
                        res_model: 'project.task',
                        domain: [["id", "in", tot_task], ['stage_id.is_closed', '=', true]],
                        view_mode: 'tree,kanban,form',
                        views: [
                            [false, 'list'],
                            [false, 'form']
                        ],
                        target: 'current'
                    }, options)
                }
            }
        },

        tot_tasks_cancel_method: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            if (flag == 0) {
                this.do_action({
                    name: _t("Procedures terminees"),
                    type: 'ir.actions.act_window',
                    res_model: 'project.task',
                    view_mode: 'tree,kanban,form',
                    domain: [['stage_id.is_cancel', '=', true]],
                    views: [
                        [false, 'list'],
                        [false, 'form']
                    ],
                    target: 'current'
                }, options)
            } else {
                if (tot_task) {
                    this.do_action({
                        name: _t("Procedures terminees"),
                        type: 'ir.actions.act_window',
                        res_model: 'project.task',
                        domain: [["id", "in", tot_task], ['stage_id.is_cancel', '=', true]],
                        view_mode: 'tree,kanban,form',
                        views: [
                            [false, 'list'],
                            [false, 'form']
                        ],
                        target: 'current'
                    }, options)
                }
            }
        },

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
                            label: "Montant",
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

        fetch_data: function() {
            var self = this;
            var def1 = this._rpc({
                model: 'project.project',
                method: 'get_tiles_data'
            }).then(function(result) {
                console.log(result)
                self.total_projects = result['total_projects'],
                    self.total_tasks = result['total_tasks'],
                    self.total_tasks_ended = result['total_tasks_ended'],
                    self.total_tasks_cancelled = result['total_tasks_cancelled'],
                    self.total_hours = result['total_hours'],
                    self.total_profitability = result['total_profitability'],
                    self.total_employees = result['total_employees'],
                    self.total_sale_orders = result['total_sale_orders'],
                    self.project_stage_list = result['project_stage_list']
                tot_so = result['sale_list']
            });
            var def2 = self._rpc({
                    model: "project.project",
                    method: "get_details",
                })
                .then(function(res) {
                    self.invoiced = res['invoiced'];
                    self.to_invoice = res['to_invoice'];
                    self.time_cost = res['time_cost'];
                    self.expen_cost = res['expen_cost'];
                    self.payment_details = res['payment_details'];
                });
            var def3 = self._rpc({
                    model: "project.project",
                    method: "get_hours_data",
                })
                .then(function(res) {
                    self.hour_recorded = res['hour_recorded'];
                    self.hour_recorde = res['hour_recorde'];
                    self.billable_fix = res['billable_fix'];
                    self.non_billable = res['non_billable'];
                    self.total_hr = res['total_hr'];
                });

            var def4 = self._rpc({
                    model: "project.project",
                    method: "get_task_data",
                })
                .then(function(res) {
                    self.task_data = res['project'];

                });

            return $.when(def1, def2, def3, def4);
        },

    });

    core.action_registry.add('project_dashboard', PjDashboard);
});
