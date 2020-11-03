odoo.define('af_web_theme.Pager', function (require) {
"use strict";

var core = require('web.core');
var config = require("web.config");

var Pager = require('web.Pager');

var _t = core._t;
var QWeb = core.qweb;

Pager.include({
    _render: function () {
    	this._super.apply(this, arguments);
        if (this.state.size !== 0 && config.device.isMobile) {
            this.$value.html(Math.ceil(this.state.current_max / this.state.limit));
            this.$limit.html(Math.ceil(this.state.size / this.state.limit));
        }
    },
    _onEdit: function (event) {
        if (!config.device.isMobile) {
        	this._super.apply(this, arguments);
        }
        event.stopPropagation();
    },
});

});