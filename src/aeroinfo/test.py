    """
    Test script for the aeroinfo package.
    This script is used to download and extract the FAA NASR data.

    Not sure what effect building the aeroinfo package has in terms of importing -- presumably only local imports work?

    """


import argparse
# import datetime
import logging
import os

# import aeroinfo
from aeroinfo.download_nasr import download_and_extract_nasr_zip

# Set up argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--edition", help="current or next", default="current")
parser.add_argument(
    "-l",
    "--log-level",
    help="how much logging do you want?",
    choices=["debug", "info", "warning", "error", "critical"],
    default="warning",
)
args = parser.parse_args()
log_level_map = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# Set up logging
logging.basicConfig(level=log_level_map[args.log_level])


# Blanket download and extraction of NASR data
# ***work on timing this operation
print(download_and_extract_nasr_zip(edition=args.edition, path=os.path.join("tmp","faa_nasr_data")))

# Query the database for 


