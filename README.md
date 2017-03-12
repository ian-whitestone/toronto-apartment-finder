
# Toronto Apartment Finder
------------------------
<p align="center">
  <img src=images/robot.png alt="robot" style="width: 600px;" style="height: 200px;"/>
</p>

This repo contains the code for a bot that will scrape Craigslist & Kijiji for real-time listings matching specific criteria, then alert you in Slack. This will let you quickly see the best new listings, and contact the owners. You can adjust the settings to change your price range, what neighborhoods you want to look in, and what transit stations and other points of interest you'd like to be close to.

Inspired by the work of [Vik Paruchuri](https://github.com/VikParuchuri/apartment-finder). Please visit his repo for setup instructions and the original work.


## Overview


## Features





## TODO
------------------------

- [x] Craigslist Integration
- [x] Kijiji Integration
- [x] Enhanced Slack Posts
- [x] Work Commute time
- [] Scrape Viewit or other rental listing sites
- [] Build a recommender based on liked listings
- [] Refactoring
- [] Add docstrings

* Scrape other rental sites
* Scrape condos.ca and compare renting vs buying at the listings level
* Pull in listing description data and scan that as well

* Score each listing
* Add 1 line for each listing parameter (i.e. price, neighborhood), colour code by scale
* custom walkscore ratings  
* Add a like/dislike button, store results to create a ML pred'n tool.
