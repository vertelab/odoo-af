odoo.define("crash_manager", function(require) {
    "use strict";

    var core = require("web.core");
    var _t = core._t;
    var CrashManager = require("web.CrashManager");
    var Dialog = require('web.Dialog');
    var QWeb = core.qweb;

    CrashManager.include({
        show_warning: function(error) {
            if (!this.active) {
                return;
            }
            return new Dialog(this, {
                size: 'medium',
                title: "Felmeddelande",
                $content: $(QWeb.render('CrashManager.warning', {error: error}))
            }).open({shouldFocusButtons:true});
        },
        show_error: function(error) {
            if (!this.active) {
                return;
            }
            var dialog = new Dialog(this, {
                title: "Felmeddelande",
                $content: $(QWeb.render('CrashManager.error', {error: error}))
            });

            // When the dialog opens, initialize the copy feature and destroy it when the dialog is closed
            var $clipboardBtn;
            var clipboard;
            dialog.opened(function () {
                // When the full traceback is shown, scroll it to the end (useful for better python error reporting)
                dialog.$(".o_error_detail").on("shown.bs.collapse", function (e) {
                    e.target.scrollTop = e.target.scrollHeight;
                });

                $clipboardBtn = dialog.$(".o_clipboard_button");
                $clipboardBtn.tooltip({title: _t("Copied !"), trigger: "manual", placement: "left"});
                clipboard = new window.ClipboardJS($clipboardBtn[0], {
                    text: function () {
                        return (_t("Error") + ":\n" + error.message + "\n\n" + error.data.debug).trim();
                    },
                    // Container added because of Bootstrap modal that give the focus to another element.
                    // We need to give to correct focus to ClipboardJS (see in ClipboardJS doc)
                    // https://github.com/zenorocha/clipboard.js/issues/155
                    container: dialog.el,
                });
                clipboard.on("success", function (e) {
                    _.defer(function () {
                        $clipboardBtn.tooltip("show");
                        _.delay(function () {
                            $clipboardBtn.tooltip("hide");
                        }, 800);
                    });
                });
            });
            dialog.on("closed", this, function () {
                $clipboardBtn.tooltip('dispose');
                clipboard.destroy();
            });

            return dialog.open();
        },
    });
});
