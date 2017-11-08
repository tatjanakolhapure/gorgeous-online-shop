/**
 * Created by Tatjana Kolhapure on 05/11/2017.
 */

;(function(jQuery){
	"use strict";
	function gorgeous()
	{
		var global = {
		    dropdownShop: jQuery(".dropdown--shop"),
            dropdownAccount: jQuery(".dropdown--account")
		};

	    var fn = {
			init: function() {
				jQuery(document).ready(function() {
				    // show navigation when document is ready to avoid blinking
				    jQuery("#navigation").show();
				    // load functions
				    fn.menuDropDown();
				    fn.slideOutMenu();
				    fn.changeLogoSize();
				    fn.scroll();
				    fn.homeBanner();
                    // change html for home banner arrows, remove "previous" and "next"
				    jQuery(".slick-arrow").text("");
                });

				jQuery(window).on("resize", function() {
				    fn.hideMenuDropDown();
                });
			},

            scroll: function() {
			    jQuery(window).scroll(function() {
				    fn.changeLogoSize();
                });
            },

            hideMenuDropDown: function() {
			    if (jQuery(window).width() > 768 ) {
			        if (global.dropdownShop.next().hasClass("move-down-shop")) {
                        global.dropdownShop.next().removeClass("move-down-shop");
                        global.dropdownShop.removeClass("show");

                    }
                    if (global.dropdownAccount.next().hasClass("move-down-account")) {
                        global.dropdownAccount.next().removeClass("move-down-account");
                        global.dropdownAccount.removeClass("show");
                    }
                }
            },

            menuDropDown: function() {
                // Solution for keeping drop-down menu open when clicking outside it
                // code by Mike Kane https://stackoverflow.com/questions/19740121/keep-bootstrap-dropdown-open-when-clicked-off
                global.dropdownShop.on({
                    "shown.bs.dropdown": function() {
                        if (jQuery(window).width() < 769 ) {
                            jQuery(this).attr('closable', false);
                        } else {
                            jQuery(this).attr('closable', true);
                        }
                    },
                    "hide.bs.dropdown": function() {
                        return jQuery(this).attr('closable') == 'true';
                    }
                });
                global.dropdownAccount.on({
                    "shown.bs.dropdown": function() {
                        if (jQuery(window).width() < 769 ) {
                            jQuery(this).attr('closable', false);
                        } else {
                            jQuery(this).attr('closable', true);
                        }
                    },
                    "hide.bs.dropdown": function () {
                        return jQuery(this).attr('closable') == 'true';
                    }
                });
                global.dropdownShop.children().first().on({
                    "click": function() {
                        jQuery(this).parent().attr('closable', true);
                        // End of solution by Mike Kane
                        if (jQuery(window).width() < 769 ) {
                            if (global.dropdownShop.next().hasClass("move-down-shop")) {
                                global.dropdownShop.next().removeClass("move-down-shop");
                            } else {
                                global.dropdownShop.next().addClass("move-down-shop");
                            }
                        }
                    }
                });
                global.dropdownAccount.children().first().on({
                    "click": function() {
                        jQuery(this).parent().attr('closable', true);
                        if (jQuery(window).width() < 769 ) {
                            if (global.dropdownAccount.next().hasClass("move-down-account")) {
                                global.dropdownAccount.next().removeClass("move-down-account");
                            } else {
                                global.dropdownAccount.next().addClass("move-down-account");
                            }
                        }
                    }
                });
            },

            // Code from SlideOut.js documentation
            slideOutMenu: function() {
                var slideout = new Slideout({
                    'panel': document.getElementById('main-content'),
                    'menu': document.getElementById('navigation'),
                    'padding': 256,
                    'tolerance': 70
                  });

                // Toggle button
                $('.btn-hamburger').on('click', function() {
                    slideout.toggle();
                });

                var fixed = document.querySelector('#mobile-header');

                slideout.on('translate', function(translated) {
                  fixed.style.transform = 'translateX(' + translated + 'px)';
                });

                slideout.on('beforeopen', function () {
                  fixed.style.transition = 'transform 300ms ease';
                  fixed.style.transform = 'translateX(256px)';
                });

                slideout.on('beforeclose', function () {
                  fixed.style.transition = 'transform 300ms ease';
                  fixed.style.transform = 'translateX(0px)';
                });

                slideout.on('open', function () {
                  fixed.style.transition = '';
                });

                slideout.on('close', function () {
                  fixed.style.transition = '';
                });
            },

            changeLogoSize: function() {
                if (jQuery(window).scrollTop() > 125) {
                    jQuery(".logo--main").addClass("logo--main-small");
                } else {
                    jQuery(".logo--main").removeClass("logo--main-small");
                }
            },

            homeBanner: function() {
			    var homeBanner = jQuery("#home-banner");
			    homeBanner.on('breakpoint', function(event, slick, currentSlide, nextSlide){
			        jQuery(".slick-arrow").text("");
			    });
                homeBanner.slick({
                    autoplay: true,
                    speed: 800,
                    responsive: [
                    {
                      breakpoint: 480,
                      settings: {
                        centerMode: true,
                        variableWidth: true,
                        arrows: false
                      }
                    }]
                });
            }
		};

		fn.init();
	}

	new gorgeous();
})(jQuery);
