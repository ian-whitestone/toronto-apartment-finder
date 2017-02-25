from scraper import do_scrape
from scraper import post_favourites
import src.settings as settings
import time
import sys
import traceback

if __name__ == "__main__":
    # while True:
    print("{}: Checking for favourites".format(time.ctime()))
    try:
        post_favourites()
    except:
        print ('error checking favourites')
    print("{}: Starting scrape cycle".format(time.ctime()))
    try:
        do_scrape()
    except KeyboardInterrupt:
        print("Exiting....")
        sys.exit(1)
    except Exception as exc:
        print("Error with the scraping:", sys.exc_info()[0])
        traceback.print_exc()
    else:
        print("{}: Successfully finished scraping".format(time.ctime()))
    time.sleep(settings.SLEEP_INTERVAL)


## TO DO

#add logging
#remove furnished apartments
#remove studios


#put everything in SQL database for analytics down the road??
