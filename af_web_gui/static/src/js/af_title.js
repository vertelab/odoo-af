odoo.define('af_title', function (require) {
    "use strict";

    var AbstractWebClient = require("web.AbstractWebClient");

    AbstractWebClient.include({
        init: function (parent) {
            this._super(parent);
            this.set('title_part', {"zopenerp": "Kundrelationssystemet"});
        }
    });
});
