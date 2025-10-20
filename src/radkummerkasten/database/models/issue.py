#!/usr/bin/env python3


"""The database model issues on the radkummerkasten map."""


import enum

from geoalchemy2 import Geometry, WKBElement
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from .base import Base

__all__ = ["Issue", "IssueType"]


class IssueType(enum.Enum):
    """The types of issue that can be reported."""

    # Status Quo:

    # a) Frontend:
    # Gefahrenstelle
    # Lückenschluss
    # Einbahn öffnen
    # Radbügel
    # Markierung oder Schild
    # Ampel
    # Hindernis
    # Anderes

    # b) Datenbank
    # Ampelschaltung    1537
    # Anderes           1249
    # Beschilderung        1
    # Bodenmarkierung    907
    # Einbahn öffnen    1351
    # Gefahrenstelle    2899
    # Hindernisse        747
    # Lückenschluss     1293
    # Radabstellanlage  1968

    GEFAHRENSTELLE = "Gefahrenstelle"
    LUECKENSCHLUSS = "Lückenschluss"
    EINBAHN_OEFFNEN = "Einbahn öffnen"
    RADBUEGEL = "Radbügel"
    MARKIERUNG_ODER_SCHILD = "Markierung oder Schild"
    AMPEL = "Ampel"
    HINDERNIS = "Hindernis"
    ANDERES = "Anderes"

    # TODO: make this configurable/dynamic?


class Issue(Base):
    """
    An issue reported to radkummerkasten map.

    Note that the first comment to this issue is shown as the issue text.
    """

    id: Mapped[Uuid] = mapped_column(primary_key=True)
    issue_type: Mapped[IssueType] = mapped_column(nullable=False)
    point: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326)
    )
