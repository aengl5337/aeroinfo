"""
Aeroinfo: A package for importing, parsing, and querying FAA NASR aviation data.
"""

from . import database
from . import parsers
from . import query
from . import import_script  # renamed from import.py to avoid reserved keyword conflict

__version__ = "0.1.0"

__all__ = ["database", "parsers", "query", "import_script"]