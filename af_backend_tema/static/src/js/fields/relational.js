odoo.define('af_web_theme.relational_fields', function (require) {
"use strict";

var core = require('web.core');
var config = require("web.config");
var fields = require('web.relational_fields');

var _t = core._t;
var QWeb = core.qweb;

fields.FieldStatus.include({
    _setState: function () {
        this._super.apply(this, arguments);
        if (config.device.isMobile) {
            _.map(this.status_information, function (value) {
                value.fold = true;
            });
        }
    },
});

fields.FieldOne2Many.include({
    _renderButtons: function () {
        var result = this._super.apply(this, arguments);
        if (config.device.isMobile && this.$buttons) {
        	var $buttons = this.$buttons.find('.btn-secondary');
        	$buttons.addClass('btn-primary af_mobile_add');
            $buttons.removeClass('btn-secondary');
        }
        return result;
    }
});

fields.FieldMany2Many.include({
    _renderButtons: function () {
        var result = this._super.apply(this, arguments);
        if (config.device.isMobile && this.$buttons) {
        	var $buttons = this.$buttons.find('.btn-secondary');
        	$buttons.addClass('btn-primary af_mobile_add');
            $buttons.removeClass('btn-secondary');
        }
        return result;
    }
});

});