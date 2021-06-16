odoo.define('af_web_gui.notifications', function (require) {
    "use strict";

    var Notification = require("web.Notification");
    Notification.include({
        _autoCloseDelay: 8000,
        init: function (parent, params) {
            this._super(parent, params);
            this.sticky = params.sticky ? params.sticky : true;
        },
    });
});
