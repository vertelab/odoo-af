odoo.define('af_gui_disabeling.user_menu', function (require) {
"use strict";

var core = require('web.core');
var UserMenu = require('web.UserMenu');
var session = require('web.session');

var _t = core._t;

UserMenu.include({
    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
             if (!session.debug){
                 $('li a[data-menu="settings"]').remove();
                 $('li a[data-menu="logout"]').remove();
            }
        });
    },
});
});
