# Online Shop Gorgeous

## Table of Contents
- [Overview and goals](#overview-and-goals)
- [Design](#design)
- [Functionality](#functionality)
- [Validation and Testing](#validation-and-testing)
- [Deployment](#deployment)

## Overview and goals

This is Code Institute Stream Three Project as part of the Full Stack Development course. The project is focused on
both Front End and Back End Development skills. It is a brand new Django project composed of
multiple apps.

Gorgeous is a fictitious online clothing shop for women. All products are of high quality and newest fashion with
elegant and feminine style to them. The target audience is young and middle age women, who follow fashion, want to look
good and shop online.  

The goal was to create a website for existing and potential customers in order to sell products and manage shop online
and to promote the brand. The following requirements were set and met:
- the website is user and mobile friendly
- the website design helps to create a good brand image
- the homepage calls for action to make customers shop
- shop managers can manage products, stock and orders online
- customers can view and sort, filter products on the website, register, add products to the shopping bag, edit
shopping bag, buy products and view orders on their account, as also update their delivery address or other account
details and get customer support contact information.

The project was made keeping in mind possible future functionality updates.

## Design

The wireframes were created during the initial planning stage before starting the project development.

UX and UI design ideas were taken by looking at other online shop examples, like Shopify themes, ASOS, New Look,
Missguided, PrettyLittleThing, River Island, Forever 21 etc.

Shop logo was created using Adobe Illustrator.

The following colors used for the design - gold, black, white, grey. Gold color is used for logo, buttons and slider
arrows, grey color is used as a background color for footer and shopping bag, checkout containers, as also for borders.
Font is either in black or white, black color is used for copyright and promotion block background, as also for icons.

[Colour Contrast Check](http://leaverou.github.io/contrast-ratio/) was used to check color contrast and choose the
right color shades.

The website is made as responsive as possible using media queries and jQuery.

Bootstrap library was used for the website grid, as also for accordion, tabs and dropdown menu functionality.

The shop logo sits at the top middle of the page to make it stand out. On desktop site the size of the logo decreases
when you scroll down the page so the header does not take too much space.

As for the navigation the menu is just below the logo on the desktop site with links to the account dropdown menu and
shopping bag on the right side. And on the mobile site there is a burger icon on the left of the logo for the menu. On
click the menu slides in from the left and can be closed by sliding it left using a finger or by clicking on the burger
icon. It is achieved using [SlideOut.js library](https://slideout.js.org/).

The header with logo and the menu is fixed both on desktop and mobile site so it can be easily accessible at any time.

The homepage uses full screen slider at the top of the page as also a parallax image on the page with a call for action
to attract customers. All website pages are kept as clean as possible using white space to avoid distractions and
improve readability.

[Slick.js slider](http://kenwheeler.github.io/slick/) is used to create all sliders on the website as it is easily
customizable and works perfectly on all browsers.

On the products page the navigation for filtering products is displayed on the left as usually on shopping websites.
Customers can expand or close filters. On the mobile site there is a button at the top of the products list to open
filters in a pop up screen which overlays all the page (except header). It gives enough space for customers to view and
select filters. There is a button to either reset filters or to close them. Select menu is used to sort products, It is
positioned at the top right of the products list on desktop site and next to filters button on the mobile site.
[noUiSlider.js library](https://refreshless.com/nouislider/) is used to filter products by price.

On the individual product page the product image thumbnails are displayed on the left of the main product image so the
users do not have to scroll down to click on thumbnails. Users can click on thumbnails or on slider arrows to view
different product images. Users can also click on the main image to zoom it in. [jQuery Zoom library by Jack
Moore](http://www.jacklmoore.com/zoom/) is used for that purpose. Magnifying glass cursor is used on product image
hover. But for Internet Explorer the crosshair cursor is used instead as a fallback. On the mobile site the image
thumbnails are not displayed to save space but they are still displayed on tablet size screen.

## Functionality

