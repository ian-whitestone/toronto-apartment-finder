
## standard library imports
import time
import sys
import traceback
import logging as log
## third party library imports

## local library imports
from src.Scraper import do_scrape
from src.Favourites import post_favourites
import src.settings as settings

if __name__ == "__main__":
    # Configure top level logger
    if settings.TESTING:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logname = time.strftime("%Y_%m_%d-%H_%M_%S")
        log.basicConfig(
            format='%(asctime)s  - %(module)s - %(levelname)s - %(message)s',
            level=log.DEBUG, # Change debug level to choose how verbose you want logging to be
            filename=os.path.join(config.LOG_PATH,logname+".txt"))
        log.info("{}: Checking for favourites".format(time.ctime()))

    log.info('###############################################################')
    log.info('###############################################################')
    log.info('##################### CHECKING FOR FAVOURITES #################')
    log.info('###############################################################')
    log.info('###############################################################')
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
        log.exception("Error with the scraping:", sys.exc_info()[0])
        traceback.print_exc()


## TODO

# finish refactoring
# common function names formatting
# doc strings
# try excepts
