odoo.define('ipf.ais_a.form_renderer', function (require) {
    "use strict";
    
    var AisA = require('ipf.ais_a');
    var FormRenderer = require('web.FormRenderer');
    
    /**
     * Include the FormRenderer to instanciate the ais_a area.
     */
    FormRenderer.include({
        /**
         * @override
         */
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.ais_a = undefined;
            console.log('Formrenderer');
            console.log(this);
        },
    
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
    
        /**
         * Overrides the function that renders the nodes to return the ais_a's $el
         * for the 'af_ais_a' div node.
         *
         * @override
         * @private
         */
        _renderNode: function (node) {
            if (node.tag === 'div' && node.attrs.class === 'af-ais-a') {
                if (!this.ais_a) {
                    this.ais_a = new AisA(this, this.state, {
                        isEditable: this.activeActions.edit,
                        viewType: 'form',
                    });
                    this.ais_a.appendTo($('<div>'));
                    this._handleAttributes(this.ais_a.$el, node);
                } else {
                    this.ais_a.update(this.state);
                }
                return this.ais_a.$el;
            } else {
                return this._super.apply(this, arguments);
            }
        },
    });
    
    });
    