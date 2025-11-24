#!/usr/bin/env python


"""Test the database models for radkummerkasten."""


import datetime
import pathlib
import uuid

import pytest

from radkummerkasten.database.models import (
    Address,
    Comment,
    Issue,
    IssueType,
    Media,
    User,
)


class TestDatabaseModels:
    """Test the database models for radkummerkasten."""

    @pytest.mark.parametrize(
        ("street", "housenumber", "postcode", "municipality"),
        (("Biene-Maja-Straße", "27", "6969", "Gigritschpatschn"),),
    )
    def test_address(self, engine, street, housenumber, postcode, municipality):
        """Test radkummerkasten.database.models.Address."""
        with engine.session.begin() as session:
            address = Address(
                street,
                housenumber,
                postcode,
                municipality,
            )
            session.add(address)

            assert isinstance(address, Address)
            assert isinstance(address.id, uuid.UUID)
            assert address.street == street
            assert address.housenumber == housenumber
            assert address.postcode == postcode
            assert address.municipality == municipality

            session.rollback()

    @pytest.mark.parametrize(
        ("title", "text"),
        (
            (
                "Uuuur schlecht",
                "In der Biene-Maja-Straße ist ein riesen Loch im Radweg.",
            ),
        ),
    )
    def test_comment(self, engine, title, text):
        """Test radkummerkasten.database.models.Comment."""
        with engine.session.begin() as session:
            user = User("Max", "Mustermann", "max.mustermann@example.com")
            comment = Comment(title, text, user=user)
            issue = Issue(IssueType.ANDERES, 48.1, 16.2)
            issue.comments.append(comment)
            session.add_all([comment, issue, user])

            assert isinstance(comment, Comment)
            assert isinstance(comment.id, uuid.UUID)
            assert comment.title == title
            assert comment.text == text
            assert comment.media == []
            assert comment.user == user
            assert comment.issue_id is None
            assert isinstance(comment.created, datetime.datetime)
            assert isinstance(comment.updated, datetime.datetime)

            session.rollback()

    @pytest.mark.parametrize(
        ("lon", "lat", "issue_type"),
        ((48.1234, 16.9876, IssueType.GEFAHRENSTELLE),),
    )
    def test_issue(self, engine, lon, lat, issue_type):
        """Test radkummerkasten.database.models.Issue."""
        with engine.session.begin() as session:
            issue = Issue(issue_type, lon, lat)
            session.add(issue)

            assert isinstance(issue, Issue)
            assert isinstance(issue.id, uuid.UUID)
            assert issue.lon == lon
            assert issue.lat == lat
            assert issue.comments == []
            assert issue.likes == 0
            assert issue.address is None
            assert isinstance(issue.created, datetime.datetime)
            assert isinstance(issue.updated, datetime.datetime)

            session.rollback()

    def test_media(self, engine, photo_path, instance_directory):
        """Test radkummerkasten.database.models.Address."""
        with engine.session.begin() as session:
            media_item = Media.from_image_file(photo_path, instance_directory)
            session.add(media_item)

            assert isinstance(media_item, Media)
            assert isinstance(media_item.id, uuid.UUID)
            assert isinstance(media_item.file_path, pathlib.Path)
            assert f"{media_item.id}" in f"{media_item.file_path}"

            session.rollback()

    def test_media_app_context(self, application, engine, photo_path):
        """Test radkummerkasten.database.models.Address."""
        with (
            engine.session.begin() as session,
            application.app_context()
        ):
            media_item = Media.from_image_file(photo_path)
            session.add(media_item)

            assert isinstance(media_item, Media)
            assert isinstance(media_item.id, uuid.UUID)
            assert isinstance(media_item.file_path, pathlib.Path)
            assert f"{media_item.id}" in f"{media_item.file_path}"

            session.rollback()

    def test_media_no_app_context(self, engine, photo_path):
        """Test radkummerkasten.database.models.Address."""
        with engine.session.begin() as session:
            with pytest.raises(
                RuntimeError,
                match=(
                      "When using Media.from_image_file.. outside of "
                      "an application context, pass an instance_path."
                  )
            ):
                _ = Media.from_image_file(photo_path)
            session.rollback()
