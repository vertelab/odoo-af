odoo.define('af_web_theme.Sidebar', function (require) {
"use strict";

var core = require('web.core');
var config = require("web.config");

var Sidebar = require('web.Sidebar');

var _t = core._t;
var QWeb = core.qweb;

Sidebar.include({
	init: function () {
		this._super.apply(this, arguments);
		if (config.device.isMobile) {
			_.each(this.sections, function(element) {
				if(element.name === 'print') {
					element.icon = 'fa fa-print';
				}
				if(element.name === 'other') {
					element.icon = 'fa fa-cogs';
				}
			});
		}
    },
});

});