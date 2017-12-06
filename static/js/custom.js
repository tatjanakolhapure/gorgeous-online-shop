/**
 * Created by Tatjana Kolhapure on 05/11/2017.
 */

;(function(jQuery){
	"use strict";
	function Gorgeous()
	{
		var global = {
		    dropdownShop: jQuery(".dropdown--shop"),
            dropdownAccount: jQuery(".dropdown--account"),
            priceRangeSlider: document.getElementById('price-range'),
            mobileHeader: jQuery('#mobile-header')
		};

	    var fn = {
			init: function() {

                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                var csrftoken = getCookie('csrftoken');

                function csrfSafeMethod(method) {
                    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                }
                // pass csrftoken in header for each ajax call
                jQuery.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });

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
				    fn.parallaxImg();
				    fn.homePopular();
				    fn.submitRegisterForm();
				    fn.submitLoginForm();
				    fn.loginRegisterTabs();
				    fn.filterProducts();
				    fn.sortProducts();
				    if (global.priceRangeSlider != null) {
				        fn.priceRangeSlider();
                    }
                    fn.mobileFilters();
                    fn.productSlider();
                    if (jQuery('.product-images').length > 0) {
                        fn.zoomProductImage();
                    }
                    fn.addToCart();
                    fn.updateCart();
                    fn.shoppingBagQuantity();
                    fn.shoppingBagButtons();
                    fn.checkoutAccordion();
                    fn.orderButtonText();
                });

				jQuery(window).on("resize", function() {
				    fn.hideMenuDropDown();
				    fn.mobileFiltersResize();
				    fn.shoppingBagQuantity();
				    fn.orderButtonText();
                });
			},

            scroll: function() {
			    jQuery(window).scroll(function() {
				    fn.changeLogoSize();
				    fn.parallaxImg();
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
                            if (jQuery('.login-mobile').length > 0) {
                                if (global.dropdownAccount.next().hasClass("move-down-account-logged-out")) {
                                    global.dropdownAccount.next().removeClass("move-down-account-logged-out");
                                } else {
                                    global.dropdownAccount.next().addClass("move-down-account-logged-out");
                                }
                            } else {
                                if (global.dropdownAccount.next().hasClass("move-down-account")) {
                                    global.dropdownAccount.next().removeClass("move-down-account");
                                } else {
                                    global.dropdownAccount.next().addClass("move-down-account");
                                }
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
            },
            // code by Renan Breno https://codepen.io/RenanB/pen/GZeBNg
            parallaxImg: function() {
			    var img = jQuery('.parallax-img');
			    // check if element is in DOM
			    if (img.length > 0) {
                    var imgParent = img.parent();
                    var speed = img.data('speed');
                    var imgY = imgParent.offset().top;
                    var winY = jQuery(window).scrollTop();
                    var winH = jQuery(window).height();
                    var parentH = imgParent.innerHeight();
                    // The next pixel to show on screen
                    var winBottom = winY + winH;
                    //If block is shown on screen
                    if (winBottom > imgY && winY < imgY + parentH) {
                        // Number of pixels shown after block appear
                        var imgBottom = ((winBottom - imgY) * speed);
                        // Max number of pixels until block disappear
                        var imgTop = winH + parentH;
                        // Porcentage between start showing until disappearing
                        var imgPercent = ((imgBottom / imgTop) * 100) + (50 - (speed * 50));
                    }
                    img.css({
                        top: imgPercent + '%',
                        transform: 'translate(-50%, -' + imgPercent + '%)'
                    });
                }
			},
			// End of code by Renan Breno

            homePopular: function() {
			    var homePopular = jQuery("#home-popular");
                homePopular.slick({
                    autoplay: true,
                    arrows: true,
                    slidesToShow: 4,
                    slidesToScroll: 1,
                    responsive: [
                    {
                      breakpoint: 1020,
                      settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1
                      }
                    },
                    {
                      breakpoint: 768,
                      settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1
                      }
                    },
                    {
                      breakpoint: 425,
                      settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                      }
                    }
                    ]
                });
            },

            submitRegisterForm: function() {
                var register_frm = jQuery('#register').find('form'),
                    reg_submit_btn = register_frm.find('button');

                register_frm.on("submit", function () {
                    var formData = jQuery(this).serializeArray();
                    formData.push({ name: reg_submit_btn.attr('name'), value: reg_submit_btn.attr('value') });
                    jQuery.ajax({
                        type: register_frm.attr('method'),
                        url: register_frm.attr('action'),
                        data: formData,
                        dataType: 'json',
                        success: function(data) {
                            window.location.href = '/account/details/';
                        },
                        error: function(data, error) {
                            console.log(error);
                            jQuery("#register-errors").text(data.responseJSON.message).show();
                        }
                    });
                    return false;
                });
            },

            submitLoginForm: function() {
                var login_frm = jQuery('#login').find('form'),
                    login_submit_btn = login_frm.find('button');

                login_frm.on("submit", function () {
                    var formData = jQuery(this).serializeArray();
                    formData.push({ name: login_submit_btn.attr('name'), value: login_submit_btn.attr('value') });
                    jQuery.ajax({
                        type: login_frm.attr('method'),
                        url: login_frm.attr('action'),
                        data: formData,
                        dataType: 'json',
                        success: function(data) {
                            window.location.href = '/account/details/';
                        },
                        error: function(data, error) {
                            console.log(error);
                            jQuery("#login-errors").text(data.responseJSON.message).show();
                        }
                    });
                    return false;
                });
            },

            loginRegisterTabs: function() {
			    var formsContainer = jQuery('#forms-container');
			    formsContainer.find('.nav-tabs a').click(function(e) {
			        e.preventDefault();
			        jQuery(this).tab('show');
                });

                // store the currently selected tab in the hash value
                jQuery("ul.nav-tabs > li > a").on("shown.bs.tab", function(e) {
                    var id = jQuery(e.target).attr("href").substr(1);
                    window.location.hash = id;
                    jQuery(document).scrollTop(0);
                });
                // on load of the page: switch to the currently selected tab
                var hash = window.location.hash;
                formsContainer.find('.nav-tabs').find('a[href="' + hash + '"]').tab('show');
            },

            filterProducts: function() {
			    var checkbox = jQuery('.collapse').find('input');
                checkbox.on("change", function () {
                    var data = jQuery('.collapse').find('input:checked').serializeArray();
                    jQuery.ajax({
                        url: "/products/",
                        type: 'GET',
                        data: data,
                        success: function(data) {
                            jQuery('#products-list').html(data);
                        },
                        error: function(data, error) {
                            console.log(error);
                        }
                    });
                    return false;
                });
            },

            sortProducts: function() {
			    var sortSelect = jQuery('#sort');
                sortSelect.on("change", function () {
                    var data = sortSelect.serializeArray();
                    jQuery.ajax({
                        url: "/products/",
                        type: 'GET',
                        data: data,
                        success: function(data) {
                            jQuery('#products-list').html(data);
                        },
                        error: function(data, error) {
                            console.log(error);
                        }
                    });
                    return false;
                });
            },

            priceRangeSlider: function() {
                // create price range slider
                noUiSlider.create(global.priceRangeSlider, {
                    start: [ 0, 100 ],
                    snap: true,
                    connect: true,
                    range: {
                        'min': 0,
                        '10%': 10,
                        '20%': 20,
                        '30%': 30,
                        '40%': 40,
                        '50%': 50,
                        '60%': 60,
                        '70%': 70,
                        '80%': 80,
                        '90%': 90,
                        'max': 100
                    },
                    // add £ to price values to display in the front end
                    format: wNumb({
                        prefix: '£ '
                    })
                });

                global.priceRangeSlider.noUiSlider.on('change', function() {
                    // get values of start and end price
                    var values = global.priceRangeSlider.noUiSlider.get();
                    // get values of selected checkboxes
                    var data = jQuery('.collapse').find('input:checked').serializeArray();
                    // push values of start and end price to checkboxes values
                    data.push({'name':'start_price','value': values[0].replace('£','')});
                    data.push({'name':'end_price','value': values[1].replace('£','')});
                    jQuery.ajax({
                        url: "/products/",
                        type: 'GET',
                        data: data,
                        success: function(data) {
                            jQuery('#products-list').html(data);
                        },
                        error: function(data, error) {
                            console.log(error);
                        }
                    });
                    return false;
                });

                // get price range values
                var snapValues = [
                    document.getElementById('slider-snap-value-lower'),
	                document.getElementById('slider-snap-value-upper')
                ];
                // show price range values in the front end
                global.priceRangeSlider.noUiSlider.on('update', function( values, handle ) {
                    snapValues[handle].innerHTML = values[handle];
                });
            },

            mobileFilters: function() {
			    // open filters and hide necessary elements when clicking on filter
                jQuery('#filter-products').on('click', function(){
                    jQuery('#filters-container').show();
                    jQuery('#promotion').hide();
                    jQuery('.heading--top').hide();
                    jQuery('#products-nav').hide();
                });
                // toggle plus and minus icons when clicking on accordion heading
                // on mobile only
                jQuery('.filter-header').find('a').on('click', function() {
                    if (jQuery(window).width() < 768 ) {
                        jQuery(this).find('.fa.fa-plus').toggle();
                        jQuery(this).find('.fa.fa-minus').toggle();
                    }
                });
                // hide filters and show necessary elements when clicking on done
                jQuery('#close-filters').on('click', function(){
                    jQuery('#filters-container').hide();
                    jQuery('#promotion').show();
                    jQuery('.heading--top').show();
                    jQuery('#products-nav').show();
                });
                // reset inputs and price range slider when clicking reset
                jQuery('#reset-filters').on('click', function(){
                    jQuery('.filter-block').find('input:checked').prop('checked', false);
                    global.priceRangeSlider.noUiSlider.reset();
                    // get values of start and end price
                    var values = global.priceRangeSlider.noUiSlider.get();
                    // get values of selected checkboxes
                    var data = jQuery('.collapse').find('input:checked').serializeArray();
                    // push values of start and end price to checkboxes values
                    data.push({'name':'start_price','value': values[0].replace('£','')});
                    data.push({'name':'end_price','value': values[1].replace('£','')});
                    jQuery.ajax({
                        url: "/products/",
                        type: 'GET',
                        data: data,
                        success: function(data) {
                            jQuery('#products-list').html(data);
                        },
                        error: function(data, error) {
                            console.log(error);
                        }
                    });
                    return false;
                });
            },

            mobileFiltersResize: function() {
			    var openFilter = jQuery('.filter-header').find('a[aria-expanded="true"]');
			    // check is mobile header is visible to match CSS media queries
			    if (global.mobileHeader.is(':visible') == false) {
			        // if mobile header is not visible
			        // show necessary elements on desktop on resize
                    jQuery('#promotion').show();
                    jQuery('.heading--top').show();
                    jQuery('#products-nav').show();
                    // if filter is open hide minus icon
                    if (openFilter) {
                        openFilter.find('.fa.fa-minus').hide();
                    }
                }
			    // check is mobile header is visible to match CSS media queries
                if (global.mobileHeader.is(':visible')) {
			        // check if filters are open
                    if (jQuery('#reset-filters').is(':visible')) {
                        // hide necessary elements if filters are open
                        jQuery(jQuery('.heading--top')).hide();
                        jQuery('#promotion').hide();
                        jQuery('#products-nav').hide();
                    }
			        // if filter is expanded hide plus and show minus icon on mobile
                    if (openFilter) {
                        openFilter.find('.fa.fa-plus').hide();
                        openFilter.find('.fa.fa-minus').show();
                    }
                }
            },

            productSlider: function() {
			    jQuery('.product-images').slick({
			        slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: true,
                    fade: true
                });
                jQuery('.product-thumbnails').slick({
                    slidesToShow: 5,
                    asNavFor: '.product-images',
                    focusOnSelect: true,
                    vertical: true,
                    arrows: false
                });
            },

            zoomProductImage: function() {
			     // check if mobile header is visible to match CSS media queries
                var imgUrl;
                jQuery('.product-images').on('afterChange', function (slick) {
                    // get img url from the current slide after each slide change
                    imgUrl = jQuery('.product-image.slick-current').find('img').attr('src');
                });
                // settings for image zoom
                jQuery('.product-image').zoom({
                    on: 'click',
                    url: imgUrl,
                    magnify: 1.1,
                    touch: false
                });
            },

            addToCart: function() {
			    var cart_frm = jQuery('.product-description').find('.cart-form');
                cart_frm.on("submit", function () {
                    var formData = jQuery(this).serializeArray(),
                        selectedSize = formData[0].value,
                        errorMessage = jQuery('.error-message'),
                        successMessage = jQuery('.success-message');
                    jQuery.ajax({
                        type: cart_frm.attr('method'),
                        url: cart_frm.attr('action'),
                        data: formData,
                        success: function(data) {
                            // insert selected size into success message html
                            jQuery('.selected-size').text(selectedSize);
                            // hide error message and show success message
                            if(errorMessage.is(":visible")){
                                errorMessage.hide();
                            }
                            successMessage.show();
                            // update price in shopping bag
                            jQuery('.price--total').text('£'+data.total_price);
                        },
                        error: function(data, error) {
                            console.log(error);
                            // add error message to html
                            errorMessage.find('span').html(selectedSize + " size is no more available");
                            // hide success message and show error message
                            if(successMessage.is(":visible")){
                                successMessage.hide();
                            }
                            errorMessage.show();
                        }
                    });
                    return false;
                });
            },

            updateCart: function() {
			    var cart_frm = jQuery('.product-item__form');
                cart_frm.on("submit", function () {
                    var formErrorMsg = jQuery(this).find('.cart-error-message'),
                        formButtons = jQuery(this).find('.product-item__buttons'),
                        formData = jQuery(this).serializeArray();
                    jQuery.ajax({
                        type: jQuery(this).attr('method'),
                        url: jQuery(this).attr('action'),
                        data: formData,
                        success: function(data) {
                            // hide error message if visible
                            if(formErrorMsg.is(':visible')) {
                                formErrorMsg.fadeOut(200);
                            }
                            // hide buttons
                            formButtons.fadeOut(200);
                            // update prices
                            jQuery('.price--subtotal').text('£'+data.subtotal_price);
                            jQuery('.price--delivery').text('£'+data.delivery_price);
                            jQuery('.price--total').text('£'+data.total_price);
                        },
                        error: function(error) {
                            console.log(error);
                            // show error message
                            formErrorMsg.show();
                        }
                    });
                    return false;
                });
            },

            shoppingBagQuantity: function() {
			    // change text for quantity label depending on screen size
                // check if mobile header is visible to match CSS media queries
			    if (global.mobileHeader.is(':visible') == true) {
                    jQuery('label[for=id_quantity]').text('Qty:');
                }
                else {
                    jQuery('label[for=id_quantity]').text('Quantity:');
                }
            },

            shoppingBagButtons: function() {
			    var previousValue,
                    newValue;
			    // on focus get previous select value
                // on change get new select value and show buttons
			    jQuery('.product-item__form-select').find('select').on('focus', function (){
			        previousValue = this.value;
                }).on('change', function(){
			        newValue = this.value;
                    jQuery(this).parent().next().fadeIn(200);
                });
			    // when clicking cancel change the relevant select value to previous one
                // hide buttons and hide error message (if visible)
			    jQuery('.product-item__button--cancel').on('click', function(){
			        jQuery(this).parent().fadeOut(200);
			        var formErrorMsg = jQuery(this).parent().next();
			        if(formErrorMsg.is(':visible')){
			            formErrorMsg.fadeOut(200);
                    }
			        if(previousValue.startsWith('UK')){
			            jQuery('#size-update').val(previousValue);
                    }
                    else {
			            jQuery('#id_quantity').val(previousValue);
                    }
                });
            },

            checkoutAccordion: function(){
			    // check if mobile header is visible to match CSS media queries
			    if (global.mobileHeader.is(':visible') == true) {
                    jQuery('#summary-products').removeClass('show');
                }
            },

            orderButtonText: function(){
                // check if mobile header is visible to match CSS media queries
			    if (global.mobileHeader.is(':visible') == true) {
                    jQuery('.button--order').text('View');
			    }
			    else {
                    jQuery('.button--order').text('View order');
                }
            }
		};

		fn.init();
	}

	new Gorgeous();
})(jQuery);
