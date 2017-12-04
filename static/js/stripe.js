/**
 * Created by Tatjana Kolhapure on 03/12/2017.
 */
;(function(){
	"use strict";

        jQuery(".payment-form").submit(function() {
            var form = this;
            var card = {
                number: jQuery("#id_card_number").val(),
                expMonth: jQuery("#id_expiry_month").val(),
                expYear: jQuery("#id_expiry_year").val(),
                cvc: jQuery("#id_cvv").val(),
                address_line1: jQuery("#id_address_line1").val(),
                address_line2: jQuery("#id_address_line2").val(),
                address_city: jQuery("#id_address_city").val(),
                address_zip: jQuery("#id_address_zip").val(),
                name: jQuery("#id_name").val()
            };

            var formButton = jQuery(".button--payment");
            formButton.attr("disabled", true);
            Stripe.createToken(card, function(status, response) {
                if (status === 200) {
                    console.log(status, response);
                    jQuery(".card-errors").hide();
                    jQuery("#id_stripe_id").val(response.id);
                    form.submit();

                } else {
                    jQuery(".stripe-error-message").text(response.error.message);
                    jQuery(".card-errors").show();
                    formButton.attr("disabled", false);
                }
            });
            return false;
        });

})(jQuery);