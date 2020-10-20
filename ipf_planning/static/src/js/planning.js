odoo.define('ipf.planning', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');
    var _t = core._t;

    
    // The purpose of this widget is to display Planning data from IPF.
    var Planning = Widget.extend({
        template: 'ipf_planning_tab',
        /**
         * @override
         * @param {widget} parent
         * @param {Object} record
         * @param {Object} options
         * @param {string} [options.viewType=record.viewType] current viewType in
         *   which the widget is instantiated
         */
        init: function (parent, record, options) {
            this._super.apply(this, arguments);
            this.record = record;
            this.data = null;
        },
        /**
         * @override
         */
        start: function () {
            var self = this;
            let tab = this.$el.closest('.tab-pane');
            let tab_id = tab.attr('id');
            let nav = $('a.nav-link[href="#' + tab_id + '"]');
            nav.click(function() {self.load_data()});
            return this._super.apply(this, arguments);
        },
        appendTo: function (target) {
            let tab = target.closest('.tab-pane');
            return this._super.apply(this, arguments);
        },
        renderElement: function () {
            var self = this;
            this._super.apply(this, arguments);
            this.$('button.ipf-planning-btn-load').click(function(){self.load_data()})
        },
        load_data: function () {
            var self = this;
            // Call backend and run ipf_load_planning on the active res.partner.
            return this._rpc({
                model: 'res.partner',
                method: 'ipf_load_planning',
                args: [this.record.res_id],
            }).then(function (result) {
                self.parse_data(result);
                self.renderElement()
            });
        },
        parse_data: function (data){
            this.data = data;
            this.columns = ['delmalsrubrik', 'vfTjanstKod', 'skapadDatum', 'sokandeaktiviteter', 'delmalsbeskrivning', 'autogenereradFor', 'id', 'skapadAv'];
            this.headers = {
                delmalsrubrik: _t('Delmålsrubrik'),
                vfTjanstKod: 'vfTjanstKod',
                skapadDatum: 'skapadDatum',
                sokandeaktiviteter: 'sokandeaktiviteter',
                delmalsbeskrivning: 'delmalsbeskrivning',
                autogenereradFor: 'autogenereradFor',
                id: 'id',
                skapadAv: 'skapadAv'
            };
        },
        get_rows: function () {
            let rows = [];
            _.each(this.data.delmalslista, function (row, pos, obj){
                rows.push({
                    delmalsrubrik: row.delmalsrubrik || '',
                    vfTjanstKod: row.vfTjanstKod || '',
                    skapadDatum: row.skapadDatum || '',
                    sokandeaktiviteter: row.sokandeaktiviteter || '',
                    delmalsbeskrivning: row.delmalsbeskrivning || '',
                    autogenereradFor: row.autogenereradFor || '',
                    id: row.id || '',
                    skapadAv: row.skapadAv || ''
                });
            });
            return rows;
        },
        get_source: function () {
            if (this.data.source === 'PLV') {
                return 'Planeringsverktyget';
            } else if (this.data.source === 'BAR') {
                return 'BÄR';
            } else {
                return 'Saknas';
            }
        }
    });
    
    return Planning;
    
    });
    