import logging
import os
from pathlib import Path
from scraper import Scraper
from database import Database
from aldi import Aldi
from morrisons import Morrisons
from iceland import Iceland

# Define the path to the log file and ensures that it exists or creates it if it doesn't
logs_file = Path(Path().resolve(), "log.text")
logs_file.touch(exist_ok=True)

# Set up the logging configuration, specifying formats
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.environ.get("LOGLEVEL", "INFO"),
    handlers=[logging.FileHandler(logs_file), logging.StreamHandler()],
)


# Creating a logger object specific to this module
log = logging.getLogger(__name__)

# Creating the required instances
db = Database()
aldi, morrisons, iceland = Aldi(), Morrisons(), Iceland()
supermarkets = [aldi, morrisons, iceland]
scraper = Scraper(supermarkets=supermarkets, database=db)

# Scraping the necessary supermarket data
scraper.scrape()
