odoo.define('af_web_theme.FormView', function (require) {
"use strict";

var dom = require('web.dom');
var core = require('web.core');
var config = require("web.config");

var FormView = require('web.FormView');
var QuickCreateFormView = require('web.QuickCreateFormView');

var _t = core._t;
var QWeb = core.qweb;

FormView.include({
    init: function () {
        this._super.apply(this, arguments);
        if (config.device.isMobile) {
            this.controllerParams.disableAutofocus = true;
        }
    },
});

QuickCreateFormView.include({
    init: function () {
        this._super.apply(this, arguments);
        if (config.device.isMobile) {
            this.controllerParams.disableAutofocus = true;
        }
    },
});

});
