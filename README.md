# TravelScrapers
This is a collection of scrapers that check for availability or monitor price changes.  Results are shown on screen or can be sent to an email address if automation is desired.

All tools have an sqlite database with example entries.  Please see appropriate section below for how to retrieve the relevent IDs.
In order to send emails, the SMTPInformation table must have 1 record with the appropriate information completed.  Check with your email provider or use your own SMTP server information.

## Hotel Availability Check
### IHG
type: ihg

To retrieve the hotel code for IHG hotels, do a search for the hotel.  Click on the hotel name.  In the URL bar, you'll see the hotel code before '/hoteldetail'.
### Hilton
type: hh

To retrieve the hotel code for Hilton hotels, do a search for the hotel.  Click on the hotel name.  In the URL bar, you'll see the hotel code in all caps.
## Cruise Price Check
To retrieve the CruiseID, find the cruise on CruiseFish.net.  Above the prices, there is a 'permalink' with the cruise ID at the end.
