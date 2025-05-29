#!/usr/bin/env python3

import pprint
import logging

# Set up logging
log_level = "warning"  # Default log level
log_level_map = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# logging.basicConfig(level=log_level_map[log_level])
logging.basicConfig(
    level=log_level_map[log_level],
    filename="app.log",  # Specify the log file name
    filemode="a",        # Append to the file (use "w" to overwrite)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from database import find_airport, find_navaid, find_runway, find_runway_end
# from sqlalchemy import create_engine # ***this is not used here, and is now imported in the database module

pp = pprint.PrettyPrinter()


# include = ["demographic"]
# include = None # Same as "demographic"?
include = ["all"]

print("#  NMM ###############################")
airport = find_airport("NMM", include=include)
pp.pprint(airport.to_dict(include=include))

print("# NMM runway 19L/01R ##################")
runway = find_runway("19L", airport, include=include)
pp.pprint(runway.to_dict(include=include))

print("# NMM runway end 19L #####################")
rwend = find_runway_end("19L", runway, include=include)
pp.pprint(rwend.to_dict(include=include))

# print("#  DPA ###############################")
# airport = find_airport("DPA", include=include)
# pp.pprint(airport.to_dict(include=include))

# print("#  dpa ###############################")
# airport = find_airport("dpa", include=include)
# pp.pprint(airport.to_dict(include=include))

# print("# KDPA ###############################")
# airport = find_airport("KDPA", include=include)
# pp.pprint(airport.to_dict(include=include))

# print("#  3CK ###############################")
# airport = find_airport("3CK", include=include)
# pp.pprint(airport.to_dict(include=include))

# print("#  SSI ###############################")
# airport = find_airport("SSI")
# pp.pprint(airport.to_dict())

# include = ["demographic", "runways"]
# print("# LL10 ###############################")
# airport = find_airport("LL10", include=include)
# pp.pprint(airport.to_dict(include=include))

# include = ["additional", "runway_ends"]
# print("# LL10 runway 18/36 ##################")
# runway = find_runway("18", airport, include=include)
# pp.pprint(runway.to_dict(include=include))

# include = ["geographic", "lighting"]
# print("# LL10 runway 36 #####################")
# rwend = find_runway_end("36", runway, include=include)
# pp.pprint(rwend.to_dict(include=include))

# print("#  JOT VOR ###########################")
# navaid = find_navaid("JOT", "VOR/DME")
# pp.pprint(navaid)
