odoo.define('ipf.planning.form_renderer', function (require) {
    "use strict";
    
    var Planning = require('ipf.planning');
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
            this.ipf_planning = undefined;
        },
    
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
    
        /**
         * Overrides the function that renders the nodes to return the planning $el
         * for the 'ipf-planning-tab' div node.
         *
         * @override
         * @private
         */
        _renderNode: function (node) {
            if (node.tag === 'div' && node.attrs.class === 'ipf-planning-tab') {
                if (!this.ipf_planning) {
                    this.ipf_planning = new Planning(this, this.state, {
                        isEditable: this.activeActions.edit,
                        viewType: 'form',
                    });
                    this.ipf_planning.appendTo($('<div>'));
                    this._handleAttributes(this.ipf_planning.$el, node);
                } else {
                    this.ipf_planning.update(this.state);
                }
                return this.ipf_planning.$el;
            } else {
                return this._super.apply(this, arguments);
            }
        },
    });
    
    });
    