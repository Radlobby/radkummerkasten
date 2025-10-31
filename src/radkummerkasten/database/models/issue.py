#!/usr/bin/env python3


"""The database model issues on the radkummerkasten map."""


import enum
import uuid

from sqlalchemy.orm import Mapped, mapped_column

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

    issue_type: Mapped[IssueType] = mapped_column(nullable=False)
    lon: Mapped[float] = mapped_column(nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    # address!
