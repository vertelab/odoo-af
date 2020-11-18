odoo.define('contact.links.form_renderer', function (require) {
    "use strict";
    
    var ContactLinks = require('contact.links');
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
            this.contact_links = undefined;
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
            if (node.tag === 'div' && node.attrs.class === 'o-contact-links') {
                console.log(node);
                if (!this.contact_links) {
                    this.contact_links = new ContactLinks(this, this.state, {
                        isEditable: this.activeActions.edit,
                        viewType: 'form',
                    });
                    this.contact_links.appendTo($('<div>'));
                    this._handleAttributes(this.contact_links.$el, node);
                } else {
                    this.contact_links.update(this.state);
                }
                return this.contact_links.$el;
            } else {
                return this._super.apply(this, arguments);
            }
        },
    });
    
    });
    