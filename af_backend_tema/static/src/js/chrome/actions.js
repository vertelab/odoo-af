odoo.define('af_web_theme.ActionManager', function (require) {
"use strict";

var core = require('web.core');
var config = require("web.config");

var ActionManager = require('web.ActionManager');

var _t = core._t;
var QWeb = core.qweb;

ActionManager.include({
	_handleAction: function (action) {
        return this._super.apply(this, arguments).always($.proxy(this, '_hideMenusByAction', action));
    },
    _hideMenusByAction: function (action) {
        var unique_selection = '[data-action-id=' + action.id + ']';
        $(_.str.sprintf('.o_menu_apps .dropdown:has(.dropdown-menu.show:has(%s)) > a', unique_selection)).dropdown('toggle');
        $(_.str.sprintf('.o_menu_sections.show:has(%s)', unique_selection)).collapse('hide');
    },
});

});