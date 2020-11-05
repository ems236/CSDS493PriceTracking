10/23/2020 10PM first commit

How to load the extension:
Google Chrome extension-> Load unpacked -> select the extension folder

1) InjectedContentUI.html: the injected Html button on Amazon product page

  Note that the "Track item" button is a dummy right now which has no functionality

2) DashboardContent.html: the content page for the tracked product list.

  Take a random number and dynamically generate a random amount of pages based on that number.
  The first item tracked is set as the product page the user is browsing currently.
  
11/5/2020 10AM 2nd commit:

1) InjectedContentUI.html now sends an ajax call to the localhost server to register an item
2) DashboardContent.html: Only generates 3 cards to demonstrate a list 
                          shows up to 10 similar products (may have empty cards)
                          Mock data for history prices for graph and table
