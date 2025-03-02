odoo.define('pos_add_button.ProductTestButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const {_t} = require('web.core');

    class ProductTestButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);     //Event on click
        }

      async onClick() {
        //Error Popup
//        this.showPopup('ErrorPopup', {
//            title: this.env._t('Popup to Call So Button'),
//            body: this.env.pos.get_cashier().name,
//        });

        //Confirmation Popup
        //calling odoo orm function using rpc
//        let result = await this.rpc({
//            model: 'product.product',
//            method: 'search',
//            args: [[['available_in_pos', '=', true]]],
////            args: [['&',['available_in_pos', '=', true], '|','|',
////             ['name', 'ilike', this.state.searchWord],
////             ['default_code', 'ilike', this.state.searchWord],
////             ['barcode', 'ilike', this.state.searchWord]]],
//            context: this.env.session.user_context,
//            kwargs: {
//                offset: 2,
//                limit: 5,
//            }
//        });
        //Calling local rpc
//        let result=await this.rpc({
//                route: '/owl/rpc/example',
//                params: { },
//            }, { shadow: true });
//        console.log(result)

//        const { confirmed } = await this.showPopup('ConfirmPopup', {
//            title: _t('Confirmation Popup'),
//            body: result,
//            confirmText: this.env._t('Yes'),
//            cancelText: this.env._t('No'),
//        });
//        if (confirmed) {
//            console.log("Confirmation Done")
//        }else{
//            console.log("Confirmation Cancelled")
//        }
        //Offline Popup
//        this.showPopup('OfflineErrorPopup', {
//            title: this.env._t('Connection is lost'),
//            body: this.env._t('Check the internet connection then try again.'),
//        });

            let multi_lang = await this.rpc({
        route: '/owl/rpc/example', // Replace with the correct route to fetch languages
        params: {},
    });

    console.log(multi_lang);

    // Transform language data into a format suitable for the selection popup
    let multi_lang_list = [];
    multi_lang.forEach(function(lang) {
        multi_lang_list.push({ id: lang.id, label: lang.name, item: lang });
    });
    console.log(multi_lang_list);

    // Display the selection popup to the user
    const { confirmed, payload: selectedLang } = await this.showPopup(
        'SelectionPopup',
        {
            title: this.env._t('Select a Language'),
            list: multi_lang_list,
        }
    );

    console.log(confirmed); // True if a choice was made, else false
    console.log(selectedLang); // Selected language object, or null if canceled
    console.log(selectedLang.code); // Selected language object, or null if canceled

    if (confirmed && selectedLang) {
        // Update the user's language setting via RPC
        await this.rpc({
                model: 'res.users',
                method: 'write',
                args: [
                    [this.env.session.uid], // Current user ID
                    { lang: selectedLang.code }, // Update the language
                ],
        });

        // Refresh the page to apply the new language
        location.reload();
    }

               //Close Popup
//            const info = await this.env.pos.getClosePosInfo();
//            this.showPopup('ClosePosPopup', { info: info, keepBehind: true });
      }

    }


    ProductTestButton.template = 'ProductTestButton';

    ProductScreen.addControlButton({
        component: ProductTestButton,
        position: ['before', 'OrderlineCustomerNoteButton'],
    });


    Registries.Component.add(ProductTestButton);

    return ProductTestButton;
});
