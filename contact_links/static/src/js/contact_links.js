odoo.define('contact.links', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');
    var _t = core._t;

    
    // The purpose of this widget is to display Contact Links to other systems.
    var ContactLinks = Widget.extend({
        template: 'ContactLinks',
        /**
         * @override
         * @param {widget} parent
         * @param {Object} record
         * @param {Object} options
         * @param {string} [options.viewType=record.viewType] current viewType in
         *   which the widget is instantiated
         */
        init: function (parent, record, options) {
            console.log(this);
            this._super.apply(this, arguments);
            this.record = record;
            this.data = null;
        },
        /**
         * @override
         */
        start: function () {
            this.load_data();
            return this._super.apply(this, arguments);
        },
        load_data: function () {
            var self = this;
            // Call backend and run ipf_load_planning on the active res.partner.
            return this._rpc({
                model: 'res.partner',
                method: 'get_contact_links',
                args: [this.record.res_id],
            }).then(function (result) {
                self.parse_data(result);
                self.renderElement()
            });
        },
        parse_data: function (data){
            this.data = data;
        },
        update: function(record){
            this.record = record;
            this.data = null;
            this.renderElement();
            this.load_data();
        }
    });
    
    return ContactLinks;
    
    });
    