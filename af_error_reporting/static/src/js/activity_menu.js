odoo.define('af_error_reporting.ActivityMenu', function (require) {
"use strict";

var core = require('web.core');
var session = require('web.session');

var ActivityMenu = require('mail.systray.ActivityMenu');
var Dialog = require('web.Dialog');

var _t = core._t;
var QWeb = core.qweb;

ActivityMenu.include({
     events: {
        'click .o_mail_activity_action': '_onActivityActionClick',
        'click .o_mail_preview': '_onActivityFilterClick',
        'click .af_error_reporting': '_onafErrorreportingClick',
        'show.bs.dropdown': '_onActivityMenuShow',
    },
    _onafErrorreportingClick: function () {
        var action = {
            'type': 'ir.actions.act_url',
            'name': 'Error reporting',
            'target': 'new',
            'url': 'https://serviceportal.arbetsformedlingen.se/sp?id=sc_cat_item&amp;sys_id=733449fedb162300c66a547adc9619cf'
        };
        return this.do_action(action)
    },
});
});
