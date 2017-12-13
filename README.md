# Online Shop Gorgeous

## Table of Contents
- [Overview and goals](#overview-and-goals)
- [Pages](#pages)
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

## Pages

The website has the following pages:
- Homepage
- Products page with all products
- Products page for each category (dresses, tops, trousers, coats, shoes)
- Individual product page
- Shopping bag page
- Checkout page
- Login/ Register page
- Account page
- Account delivery address edit page
- Account details edit page
- Account password change page
- Account password change complete page
- Orders page
- Individual order page
- Contact page

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

[Font Awesome Icons](http://fontawesome.io/icons/) were used for different icons on the website (account, shopping bag,
 burger menu, social media, arrow icons etc.).

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

One page (Login/register page) is used as for both logging in and for registration. The page has two tabs. One tab with
login form and one tab with registration form. So users can switch to the tab they need.

All accounts pages have the same layout with account navigation on the left which has two sections: My details and
My orders. The page the customer is on is underlined (either My details or My orders link). 

On the products page the navigation for filtering products is displayed on the left as usually on shopping websites.
Customers can expand or close filters. On the mobile site there is a button at the top of the products list to open
filters in a pop up screen which overlays all the page (except header). It gives enough space for customers to view and
select filters. There is a button to either reset filters or to close them. Select menu is used to sort products, It is
positioned at the top right of the products list on desktop site and next to filters button on the mobile site.
[noUiSlider.js library](https://refreshless.com/nouislider/) is used to filter products by price. And
[wNumb.js](https://refreshless.com/wnumb/) library is used to format numbers for noUiSlider.

On the individual product page the product image thumbnails are displayed on the left of the main product image so the
users do not have to scroll down to click on thumbnails. Users can click on thumbnails or on slider arrows to view
different product images. Users can also click on the main image to zoom it in. [jQuery Zoom library by Jack
Moore](http://www.jacklmoore.com/zoom/) is used for that purpose. Magnifying glass cursor is used on product image
hover. But for Internet Explorer the crosshair cursor is used instead as a fallback. On the mobile site the image
thumbnails are not displayed to save space but they are still displayed on tablet size screen.

On the Shopping bag and Checkout page there are different sections with grey background to separate content for
readability. On the Checkout page, for example, order form is on the left and product list is on the right. Product list
 can be closed or expanded (it is closed on mobile by default to save space). Each product also has a borderline to
 separate it from other products.

## Functionality

Django project has the following apps:
- gorgeous
- home
- accounts
- products
- cart
- orders

In the templates folder there is a folder for each app templates.

### Gorgeous app
The main app gorgeous has urls file where urls from all other apps are imported, as also admin.site, tinymce and
django.contrib.auth urls (for updating password). Gorgeous app has one view to render
contact page.

### Home app
Home app has one view to render homepage. Popular products data is passed to the template to display bestsellers in the
"Popular this week" slider. At the moment bestsellers are filtered from all products sold (as there won't be orders made every week).
But the logic for filtering the most sold products this week is in place and commented out in the view.

### Accounts app
Accounts app has customized user model. It accepts email as a username and has fields first_name and last_name.
Superuser must be created in the back-end using "python manage.py createsuperuser" command. And first_name and last_name
fields are also required when creating a superuser. Superusers can be shop managers. However they are not supposed to
shop on the website. It can be changed in the future though if necessary. Accounts app also has customized authenticate
and get_user function for user.

Address model is used to save customer's delivery address.

Accounts app has UserRegistrationForm, UserLoginForm, UserDetailsForm and AddressForm. UserRegistrationForm and
AddressForm is used for registration. AddressForm is also used to edit customer's address. UserLoginForm is used for
logging in to the account. UserDetailsForm is used to edit user's details. 

Login and registration form data is submitted using ajax to avoid page refresh. On success the user is redirected to their
account page and if form validation failed the error message is displayed for the user.

In order to check which form has been submitted (as they are on the same page) submit button value is used.

Account page displays user details and their address. There is a link to edit user details, user password or to edit
user address. When user clicks on any of the links they are redirected to another page for editing the necessary
details. They can click cancel to return to account page and if the click save, form validation will take place. In
case of success they will be redirected to account page. UserDetailsForm data is submitted using ajax in order to
display a message to the user if an email address has been taken already.

When user clicks on logout they are redirected to homepage.

### Products app

Products app has several models. 
