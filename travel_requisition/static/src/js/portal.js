//odoo.define('stack_overflow.open_list_view', function (require) {
//
//    "use strict";
//    var pyUtils = require('web.py_utils');
//    var dialogs = require('web.view_dialogs');
//    var core = require('web.core');
//    var _t = core._t;
//    var fieldRegistry = require('web.field_registry');
//    var ListRenderer = require('web.ListRenderer');
//
//    var AddManyFieldOne2ManyRenderer = ListRenderer.extend({
//        /**
//         * It will returns the first visible widget that is editable
//         *
//         * @private
//         * @returns {Class} Widget returns first widget
//         */
//        _getFirstWidget: function () {
//            var record = this.state.data[this.currentRow];
//            var recordWidgets = this.allFieldWidgets[record.id];
//            var firstWidget = _.chain(recordWidgets).filter(function (widget) {
//                var isLast =
//                    widget.$el.is(':visible') &&
//                    (
//                        widget.$('input').length > 0 || widget.tagName === 'input' ||
//                        widget.$('textarea').length > 0 || widget.tagName === 'textarea'
//                    ) &&
//                    !widget.$el.hasClass('o_readonly_modifier');
//                return isLast;
//            }).first().value();
//            return firstWidget;
//        },
//
//        add_rows: function (lines, field_name) {
//            var self = this;
//            if (lines.length > 0) {
//                self.trigger_up('add_record', {
//                    context: [{ [field_name]: lines[0] }],
//                    forceEditable: "bottom",
//                    allowWarning: true,
//                    onSuccess: function () {
//                        self.unselectRow();
//                        lines.shift(); // Remove the first element after adding a line
//                        self.add_rows(lines, field_name);
//                    }
//                });
//
//            }
//        },
//        _onAddRecord: function (ev) {
//            // we don't want the browser to navigate to a the # url
//            ev.preventDefault();
//
//            // we don't want the click to cause other effects, such as unselecting
//            // the row that we are creating, because it counts as a click on a tr
//            ev.stopPropagation();
//
//
//            var self = this;
//            // but we do want to unselect current row
//            this.unselectRow().then(function () {
//                var context = ev.currentTarget.dataset.context;
//                if (context && pyUtils.py_eval(context).open_list_view) {
//                    // trigger add_record to get field name and model
//                    // you do not need to trigger add_record if you pass the field name and model in context
//                    self.trigger_up('add_record', {
//                        context: [{}],
//                        onSuccess: function () {
//                            var widget = self._getFirstWidget();
//                            var field_name = 'default_' + widget.name;
//                            var model = widget.field.relation;
//                            self.unselectRow();
//                            self._rpc({
//                                model: model,
//                                method: 'search',
//                                args: [[]],
//                            }).then(
//                                function (result) {
//                                    return new dialogs.SelectCreateDialog(self, _.extend({}, self.nodeOptions, {
//                                        res_model: model,
//                                        context: context,
//                                        title: _t("Search: add lines"),
//                                        initial_ids: result,
//                                        initial_view: 'search',
//                                        disable_multiple_selection: false,
//                                        no_create: !self.can_create,
//                                        on_selected: function (records) {
//                                            self.add_rows(records.map(product => product.id), field_name);
//                                        }
//                                    })).open();
//                                });
//                        }
//                    });
//                } else {
//                    self.trigger_up('add_record', { context: context && [context] });
//                }
//            });
//        },
//    });
//
//    var AddManyFieldOne2Many = fieldRegistry.map.section_and_note_one2many.extend({
//        /**
//         * We want to use our custom renderer for the list.
//         *
//         * @override
//         */
//        _getRenderer: function () {
//            if (this.view.arch.tag === 'tree') {
//                return AddManyFieldOne2ManyRenderer;
//            }
//            return this._super.apply(this, arguments);
//        },
//    });
//
//    fieldRegistry.add('add_many_one2many', AddManyFieldOne2Many);
//});

function addRow(){
alert('adding row')
}