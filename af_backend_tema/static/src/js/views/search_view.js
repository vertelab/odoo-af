odoo.define('af_web_theme.SearchView', function (require) {
"use strict";

var core = require('web.core');
var config = require("web.config");

var SearchView = require('web.SearchView');

var _t = core._t;
var QWeb = core.qweb;

SearchView.include({
	start: function () {
		if (config.device.isMobile) {
			this.$('.o_enable_searchview').text(_t("Search"));
		}
		return this._super.apply(this, arguments);
    },
});

});