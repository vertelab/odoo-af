odoo.define('ipf.ais_a', function (require) {
    "use strict";
    
    var Activity = require('mail.Activity');
    var AttachmentBox = require('mail.AttachmentBox');
    var ChatterComposer = require('mail.composer.Chatter');
    var Dialog = require('web.Dialog');
    var Followers = require('mail.Followers');
    var ThreadField = require('mail.ThreadField');
    var mailUtils = require('mail.utils');
    
    var concurrency = require('web.concurrency');
    var config = require('web.config');
    var core = require('web.core');
    var Widget = require('web.Widget');
    
    var _t = core._t;
    var QWeb = core.qweb;
    
    // The purpose of this widget is to display the chatter area below the form view
    //
    // It instantiates the optional mail_thread, mail_activity and mail_followers widgets.
    // It Ensures that those widgets are appended at the right place, and allows them to communicate
    // with each other.
    // It synchronizes the rendering of those widgets (as they may be asynchronous), to mitigate
    // the flickering when switching between records
    var AisA = Widget.extend({
        template: 'ipf_ais_a.ais_a',
        /**
         * @override
         * @param {widget} parent
         * @param {Object} record
         * @param {Object} options
         * @param {string} [options.viewType=record.viewType] current viewType in
         *   which the chatter is instantiated
         */
        init: function (parent, record, options) {
            this._super.apply(this, arguments);
            console.log(this);
        },
        /**
         * @override
         */
        start: function () {
            var self = this;
            let tab = this.$el.closest('.tab-pane');
            console.log(tab);
            let tab_id = tab.attr('id');
            console.log(tab_id);
            let nav = $('a.nav-link[href="#' + tab_id + '"]');
            console.log(nav);
            nav.click(function() {self.render_ais_a()});
            return this._super.apply(this, arguments);
        },
        appendTo: function (target) {
            let tab = target.closest('.tab-pane');
            console.log('appendTo');
            console.log(tab);
            return this._super.apply(this, arguments);
        },
        render_ais_a: function () {
            console.log(this.getParent().state);
        }
    });
    
    return AisA;
    
    });
    