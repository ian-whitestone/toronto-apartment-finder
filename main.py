## standard library imports
import time
import sys
import traceback
import logging as log
import os

## third party library imports

## local library imports
from src.Scraper import do_scrape
from src.Favourites import post_favourites
import src.settings as settings

# set log levels for requests/selenium libraries
log.getLogger("requests").setLevel(log.WARNING)
log.getLogger("selenium").setLevel(log.WARNING)

if __name__ == "__main__":
    # Configure top level logger
    if settings.TESTING:
        log.basicConfig(stream=sys.stdout, level=log.DEBUG)
    else:
        logname = time.strftime("%Y_%m_%d-%H_%M_%S")
        log.basicConfig(
            format='%(asctime)s  - %(module)s - %(levelname)s - %(message)s',
            level=log.INFO, # Change debug level to choose how verbose you want logging to be
            filename=os.path.join(settings.LOG_PATH, logname+".txt"))

    log.info("{}: Checking for favourites".format(time.ctime()))

    log.info('###############################################################')
    log.info('###############################################################')
    log.info('##################### CHECKING FOR FAVOURITES #################')
    log.info('###############################################################')
    log.info('###############################################################')

    if settings.TESTING == False:
        post_favourites()


    log.info('###############################################################')
    log.info('###############################################################')
    log.info('##################### STARTING SCRAPING #######################')
    log.info('###############################################################')
    log.info('###############################################################')

    try:
        do_scrape()
        log.info("{}: Successfully finished scraping".format(time.ctime()))
    except KeyboardInterrupt:
        log.info("Exiting....")
        sys.exit(1)
    except Exception as exc:
        log.exception("Error with the scraping: %s" % str(exc))


## TODO

# finish refactoring
# --> split up GeneralUtils (create a separate Slack posting class?, geo filtering class/module?)
# common function names formatting
# doc strings
# try excepts for all functions
