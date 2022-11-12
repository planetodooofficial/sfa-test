odoo.define('hr_payroll_extended.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var rpc = require('web.rpc');
var session = require('web.session');
var utils = require('web.utils');
//var web_client = require('web.web_client');
var _t = core._t;
var QWeb = core.qweb;

var AUTHORIZED_MESSAGES = [
    'report:do_action',
    ];

var AttendanceDashboard = AbstractAction.extend({
    template: 'AttendanceDashboard',
    events: {
        'keyup .searchInput': '_onKeypress',
        'change #report_type': 'onChangeReportType',
        'click  #pdf_button': 'download_pdf',
    },
    
    init: function(parent, options) {
        this._super(parent, options);
        this.attendance_id = options.context.attendance_id;
        this.employee_ids = [];
        this.header = [];
        if (!this.attendance_id)
        {
            this.attendance_id = parseInt(utils.get_cookie('id'));
        }
    },

    fetch_data: function () {
        var self = this;
        var def1 =  this._rpc({
            model: 'hr.attendance.muster.dashboard',
            method: 'get_employees_attendance_muster_data',
            args: [this.attendance_id],
        }).then(function(result) {
            self.employee_ids = result;
        });
        return $.when(def1);
    },
    willStart: function() {
        var self = this;
        return $.when(ajax.loadLibs(this), this._super()).then(function() {
            return self.fetch_data();
        });
    },
    start: function() {
        utils.set_cookie("id", this.attendance_id);
        var self = this;
        return this._super().then(function() {
            self.render_dashboards(self.employee_ids, self.employee_ids.employee_ids, self.employee_ids.header_list, self.employee_ids.header_date[0]);
        });
    },
    _onKeypress: function (ev) {
        var search_text = (this.$('.searchInput').val()).toLowerCase();
        var res = this.employee_ids;
        var header = this.employee_ids.header_list;
        var employee_ids = []
        _.each(res.employee_ids, function (emp) {
            if ((emp.employee_id.toLowerCase()).indexOf(search_text) != -1) {
                employee_ids.push(emp)
            }
        });
        this.render_dashboards(res, employee_ids, header, res.header_date[0], search_text);
    },

    download_pdf: function(event) {
        var self = this;
        var report_type = $('#report_type').val();
        return rpc.query({
            model: 'hr.attendance.muster.dashboard',
            method: 'get_employees_attendance_muster_data',
            args: [this.attendance_id],

        }).then(function(result) {
            var action = {
                'type': 'ir.actions.report',
                'report_type': 'xlsx',
                'report_name': 'pways_attendance_muster.attendance_muster_xls',
                'report_file': 'pways_attendance_muster.attendance_muster_xls',
                'data': result,
                'context': {
                    'active_model': 'hr.attendance.muster.dashboard',
                     'landscape': 1,
                    'data': result
                },
                'display_name': 'Attendance Muster Report',
            };
            return self.do_action(action);
        });
    },
    render_dashboards: function (res, employee_ids, header, header_date, search=null) {
        this.$('.o_employee_dashboard').html(QWeb.render('EmpAttendanceDashboard', 
            {
                widget: res, 
                'employee_ids': employee_ids,
                'header_list': header,
                'header_date': header_date,
                'search_text': search,
            }));
        var value = $("#o-export-search-filter").val();
        $("#o-export-search-filter").focus().val('').val(value);
    }
});

core.action_registry.add('attendance_dashboard', AttendanceDashboard);

return AttendanceDashboard;

});

