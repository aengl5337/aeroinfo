#!/usr/bin/env python

from dotenv import load_dotenv
load_dotenv()

import logging
import os

from sqlalchemy.orm import Load, sessionmaker
from sqlalchemy import create_engine

from .models.apt import Airport, Runway, RunwayEnd
from .models.nav import Navaid

logger = logging.getLogger(__name__)


def get_db_url():
    """
    Get the database URL from environment variables.

    Returns
    -------
    str
        The database URL.
    """
    db_rdbm = os.getenv("DB_RDBM")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")

    if db_rdbm == "sqlite":
        url = "%s://%s" % (db_rdbm, db_host)
    else:
        url = "%s://%s:%s@%s/%s" % (db_rdbm, db_user, db_pass, db_host, db_name)

    logger.debug(f"Database URL: {url}")
    # print(f"Database URL: {url}")
    return url


Engine = create_engine(get_db_url(), echo=False)


def find_airport(identifier, include=None):
    """
    Find an airport by its identifier (FAA or ICAO).

    Parameters
    ----------
    identifier : str
        The identifier of the airport (FAA or ICAO).
    include : list, optional
        A list of related objects to include in the query. The default is None.
        Possible values (native to the Airport object) are:
        - "demographic": Include demographic information associated with the airport. (note: nothing is actually queried here, but the model has a demographic field that it defaults)
        - "ownership": Include ownership information associated with the airport.
        - "geographic": Include geographic information associated with the airport.
        - "faaservices": Include FAA services associated with the airport.
        - "fedstatus": Include federal status information associated with the airport.
        - "inspection": Include inspection information associated with the airport.
        - "aptservices": Include airport services associated with the airport.
        - "facilities": Include facilities associated with the airport.
        - "basedaircraft": Include based aircraft information associated with the airport.
        - "annualops": Include annual operations information associated with the airport.
        - "additional": Include additional information associated with the airport.
        Other related info that can be added to include, but are not native to the Airport object (and thus must be added to the query via .joinedload()):
        - "runways": Include runways associated with the airport.
        - "remarks": Include remarks associated with the airport.
        - "attendance": Include attendance schedules associated with the airport.
        And lastly:
        - "all": Include all above objects.
        
    Returns
    -------
    Airport
        The airport object if found, otherwise None.
    """

    _include = include or [] # Default to an empty list if include is None
    queryoptions = []

    if "runways" in _include or "all" in _include:
        queryoptions.append(Load(Airport).joinedload("runways"))

    if "remarks" in _include or "all" in _include:
        queryoptions.append(Load(Airport).joinedload("remarks"))

    if "attendance" in _include or "all" in _include:
        queryoptions.append(Load(Airport).joinedload("attendance_schedules"))

    Session = sessionmaker(bind=Engine)
    session = Session()

    airport = (
        session.query(Airport)
        .filter(
            (Airport.faa_id == identifier.upper()) 
            | (Airport.icao_id == identifier.upper())
        )
        .order_by(Airport.effective_date.desc())
        .options(queryoptions)
        .first()
    )

    session.close()

    return airport


def find_runway(name, airport, include=None):
    """
    Find a runway by its name and associated airport.

    Parameters
    ----------
    name : str
        The name of the runway.
    airport : str or Airport
        The airport object or its identifier (FAA or ICAO).
    include : list, optional
        A list of related objects to include in the query. The default is None.
        Possible values are:
        - "runway_ends": Include runway ends associated with the runway.
        ***(work to add more options here)

    Returns
    -------
    Runway
        The runway object if found, otherwise None.
    """
    _include = include or []
    queryoptions = []

    if "runway_ends" in _include:
        queryoptions.append(Load(Runway).joinedload("runway_ends"))

    if isinstance(airport, Airport):
        _airport = airport
    elif isinstance(airport, str):
        _airport = find_airport(airport)
    else:
        raise (TypeError("Expecting str or Airport"))

    Session = sessionmaker(bind=Engine)
    session = Session()

    runway = (
        session.query(Runway)
        .with_parent(_airport)
        .filter(Runway.name.like("%" + name + "%"))
        .options(queryoptions)
        .scalar()
    )

    session.close()

    return runway


def find_runway_end(name, runway, include=None):
    """
    Find a runway end by its name and associated runway.

    Parameters
    ----------
    name : str
        The name of the runway end.
    runway : str or Runway
        The runway object or its identifier (FAA or ICAO).
    include : list, optional   
        A list of related objects to include in the query. The default is None.
        Possible values are:
        - "geographic": Include geographic information associated with the runway end.
        - "lighting": Include lighting information associated with the runway end.
        ***(work to add more options here)
        
    Returns
    -------
    RunwayEnd
        The runway end object if found, otherwise None.
    """
    _include = include or []

    if isinstance(runway, Runway):
        _runway = runway
    elif isinstance(runway, tuple):
        __runway, airport = runway

        assert isinstance(__runway, str)

        if isinstance(airport, Airport):
            _airport = airport
        elif isinstance(airport, str):
            _airport = find_airport(airport)
        else:
            raise (TypeError("Expecting str or Airport in runway tuple"))

        _runway = find_runway(__runway, _airport)

    Session = sessionmaker(bind=Engine)
    session = Session()

    rwend = (
        session.query(RunwayEnd)
        .with_parent(_runway)
        .filter(RunwayEnd.id == name.upper())
        .scalar()
    )

    session.close()

    return rwend


def find_navaid(identifier, type, include=None):
    """
    Find a navaid by its identifier and type.

    Parameters
    ----------
    identifier : str
        The identifier of the navaid.
    type : str
        The type of the navaid (e.g., VOR, NDB).
    include : list, optional
        A list of related objects to include in the query. The default is None.
        Possible values are:
        - "demographic": Include demographic information associated with the navaid.
        ***(work to add more options here)

    Returns
    -------
    Navaid
        The navaid object if found, otherwise None.
    """
    _include = include or []

    Session = sessionmaker(bind=Engine)
    session = Session()

    navaid = (
        session.query(Navaid)
        .filter(
            (Navaid.facility_id == identifier.upper())
            & (Navaid.facility_type == type.upper())
        )
        .order_by(Navaid.effective_date.desc())
        .first()
    )

    session.close()

    return navaid
