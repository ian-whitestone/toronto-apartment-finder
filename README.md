# Toronto Apartment Finder
------------------------

This repo contains the code for a bot that will scrape Craigslist for real-time listings matching specific criteria, then alert you in Slack. This will let you quickly see the best new listings, and contact the owners. You can adjust the settings to change your price range, what neighborhoods you want to look in, and what transit stations and other points of interest you'd like to be close to.

This repo is largely based of the work of [Vik Paruchuri](https://github.com/VikParuchuri/apartment-finder). Please visit his repo for setup instructions and the original work.


## Modifications
------------------------

I have tweaked the settings so that the bot will scrape Toronto listings. A summary of other modifications is included below.


### Favourites Channel
In order to keep track of units that both my girlfriend & I like, I added functionality for the slack bot two check for any posts that have received 2 'thumbs-up'. All of these posts are moved to a #favourites channel.

### Keywords
Use regexes to determine if the unit is furnished or a studio.

### Other Minor Changes
* Only skip listings if they are missing *both* neighborhood & geotag information. The original repo dropped listings that were missing neighborhood information, which I felt was unnecessary due to the presence of the lat/lon coordinates in the geotag




## Future Work
------------------------
* Scrape other rental sites
* Scrape condos.ca and compare renting vs buying at the listings level
* Pull in listing description data and scan that as well
