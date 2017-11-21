/**
 * Created by Tatjana Kolhapure on 05/11/2017.
 */

;(function(jQuery){
	"use strict";
	function Gorgeous()
	{
		var global = {
		    dropdownShop: jQuery(".dropdown--shop"),
            dropdownAccount: jQuery(".dropdown--account")
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
                });

				jQuery(window).on("resize", function() {
				    fn.hideMenuDropDown();
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
                            console.log(data);
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
                    console.log(data);
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
            }
		};

		fn.init();
	}

	new Gorgeous();
})(jQuery);
