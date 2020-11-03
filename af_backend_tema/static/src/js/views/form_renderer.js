odoo.define('af_web_theme.FormRenderer', function (require) {
"use strict";

var dom = require('web.dom');
var core = require('web.core');
var config = require("web.config");

var FormRenderer = require('web.FormRenderer');

var _t = core._t;
var QWeb = core.qweb;

FormRenderer.include({
	_renderHeaderButtons: function () {
        var $buttons = this._super.apply(this, arguments);
        if (config.device.isMobile && this.state.model !== "res.config.settings") {
            var $dropdown = $(QWeb.render('af_web_theme.MenuStatusbarButtons'));
            $buttons.addClass("dropdown-menu").appendTo($dropdown);
            $buttons.children().addClass("dropdown-item");
            return $dropdown;
        }
        return $buttons;
    },
});

});