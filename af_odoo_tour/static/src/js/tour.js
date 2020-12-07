odoo.define('af_odoo_tour.tour', function(require) {
"use strict";

var core = require('web.core');
var tour = require('web_tour.tour');

var _t = core._t;

tour.register('af_odoo_tour', {
    url: "/web",
}, [tour.STEPS.SHOW_APPS_MENU_ITEM, {
    trigger: '.o_app[data-menu-xmlid="af_odoo_tour.introduction_tour_wizard"]',
    content: _t('Search Partner'),
    position: 'right',
    edition: 'community',
},{
    trigger: '.o_app[data-menu-xmlid="af_odoo_tour.introduction_tour_wizard"]',
    content: _t('Search Partner'),
    position: 'bottom',
    edition: 'enterprise',
},{
    // The trigger will tell that you would like to input a value in the field 'Name'
    trigger: 'input[name="identification"]',
    extra_trigger: '.o_form_editable',
    // This is the 'hint' / tooltip that is shown to the enduser
    content: _t('Fill Identification of the contact.'),
    // When you run the test (from the developer tools) it will automatically fill in 'James Cook' automatically)
    run: 'id document',
},{
    // The trigger will tell that you would like to input a value in the field 'Name'
    trigger: 'input[name="social_sec_nr_search"]',
    extra_trigger: '.o_form_editable',
    // This is the 'hint' / tooltip that is shown to the enduser
    content: _t('Fill Social security number of the contact.'),
    // When you run the test (from the developer tools) it will automatically fill in 'James Cook' automatically)
    run: '19790101-1234',
},{
    trigger: '.search_partner',
    content: _t('Search Partner.'),
    position: 'bottom',
}]);
});