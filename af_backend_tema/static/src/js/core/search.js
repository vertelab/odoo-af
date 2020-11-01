odoo.define('af_web_theme.MenuSearchMixin', function (require) {
"use strict";

var core = require('web.core');
var config = require("web.config");
var session = require("web.session");

var _t = core._t;
var QWeb = core.qweb;

var MenuSearchMixin = {
    _findNames: function (memo, menu) {
        if (menu.action) {
            var key = menu.parent_id ? menu.parent_id[1] + "/" : "";
            memo[key + menu.name] = menu;
        }
        if (menu.children.length) {
            _.reduce(menu.children, this._findNames.bind(this), memo);
        }
        return memo;
    },
    _menuInfo: function (key) {
        var original = this._searchableMenus[key];
        return _.extend({
            action_id: parseInt(original.action.split(',')[1], 10),
        }, original);
    },
    _searchFocus: function () {
        if (!config.device.isMobile) {
            this.$search_input.focus();
        } else {
        	this.$search_input.blur();
        }
    },
    _searchReset: function () {
        this.$search_container.removeClass("has-results");
        this.$search_results.empty();
        this.$search_input.val("");
    },
    _searchMenusSchedule: function () {
        this._search_def.reject();
        this._search_def = $.Deferred();
        setTimeout(this._search_def.resolve.bind(this._search_def), 50);
        this._search_def.done(this._searchMenus.bind(this));
    },
    _searchMenus: function () {
        var query = this.$search_input.val();
        if (query === "") {
            this.$search_container.removeClass("has-results");
            this.$search_results.empty();
            return;
        }
        var results = fuzzy.filter(query, _.keys(this._searchableMenus), {
            pre: "<b>",
            post: "</b>",
        });
        this.$search_container.toggleClass("has-results", Boolean(results.length));
        this.$search_results.html(QWeb.render("af_web_theme.MenuSearchResults", {
            results: results,
            widget: this,
        }));
    },
    _onSearchResultsNavigate: function (event) {
        if (this.$search_results.html().trim() === "") {
            this._searchMenusSchedule();
            return;
        }
        var all = this.$search_results.find(".af_menu_search_result");
        var key = event.key || String.fromCharCode(event.which);
        var pre_focused = all.filter(".active") || $(all[0]);
        var offset = all.index(pre_focused);
        if (key === "Tab") {
            event.preventDefault();
            key = event.shiftKey ? "ArrowUp" : "ArrowDown";
        }
        switch (key) {
	        case "Enter":
	            pre_focused.click();
	            break;
	        case "ArrowUp":
	            offset--;
	            break;
	        case "ArrowDown":
	            offset++;
	            break;
	        default:
	        	this._searchMenusSchedule();
            return;
        }
        if (offset < 0) {
            offset = all.length + offset;
        } else if (offset >= all.length) {
            offset -= all.length;
        }
        var new_focused = $(all[offset]);
        pre_focused.removeClass("active");
        new_focused.addClass("active");
        this.$search_results.scrollTo(new_focused, {
            offset: {
                top: this.$search_results.height() * -0.5,
            },
        });
    },
    _onMenuShown: function(event) {
    	this._searchFocus();
    },
    _onMenuHidden: function(event) {
    	this._searchReset();
    },
};

return MenuSearchMixin;

});