from django.test import TestCase
from api.models import Group, Content, Channel
from decimal import Decimal
import os
class GroupTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Movies")

    def test_group_creation(self):
        self.assertEqual(str(self.group), "Movies")

class ContentTestCase(TestCase):
    def setUp(self):
        self.content = Content.objects.create(
            title="Inception",
            metadata={"genre": "Sci-Fi", "director": "Christopher Nolan"},
            rating=Decimal("9.0")
        )

    def test_content_creation(self):
        self.assertEqual(str(self.content), "Inception")
        self.assertEqual(self.content.metadata["genre"], "Sci-Fi")
        self.assertEqual(self.content.rating, Decimal("9.0"))

class ChannelTestCase(TestCase):
    def setUp(self):
        # Create Groups
        self.group1 = Group.objects.create(name="Movies")
        self.group2 = Group.objects.create(name="TV Shows")

        # Create Contents
        self.content1 = Content.objects.create(title="Content 1", rating=Decimal("8.0"))
        self.content2 = Content.objects.create(title="Content 2", rating=Decimal("9.0"))

        # Create Channels
        self.channel = Channel.objects.create(title="Main Channel", language="en")
        self.subchannel = Channel.objects.create(title="Subchannel", parent_channel=self.channel)

        # Add contents and groups
        self.channel.contents.add(self.content1)
        self.channel.groups.add(self.group1)
        self.subchannel.contents.add(self.content2)
        self.subchannel.groups.add(self.group2)

    def test_channel_creation(self):
        self.assertEqual(str(self.channel), "Main Channel")
        self.assertEqual(self.channel.language, "en")

    def test_channel_rating(self):
        self.assertAlmostEqual(self.channel.calculate_rating(), Decimal("8.0"))
        self.assertAlmostEqual(self.subchannel.calculate_rating(), Decimal("9.0"))

    def test_hierarchical_rating(self):
        self.channel.subchannels.add(self.subchannel)
        self.assertAlmostEqual(self.channel.calculate_rating(), Decimal("8"))

    def test_channel_group_inheritance(self):
        self.assertIn(self.group1, self.channel.groups.all())
        self.assertIn(self.group2, self.subchannel.groups.all())

    def test_channel_content_retrieval(self):
        self.assertIn(self.content1, self.channel.contents.all())
        self.assertIn(self.content2, self.subchannel.contents.all())

class ManagementCommandTestCase(TestCase):
    def setUp(self):
        self.content1 = Content.objects.create(title="Content 1", rating=Decimal("8.0"))
        self.channel = Channel.objects.create(title="Test Channel", language="en")
        self.channel.contents.add(self.content1)

    def test_export_ratings_command(self):
        from io import StringIO
        from django.core.management import call_command
        import csv

        csv_path = "channel_ratings.csv"

        # Call the command
        call_command('export_ratings')

        # Verify the file exists
        self.assertTrue(os.path.exists(csv_path))

        # Check the contents of the file
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.assertEqual(rows[0], ["Channel Title", "Average Rating"])
        self.assertIn(["Test Channel", "8.00"], rows)

    def test_populate_data_command(self):
        from django.core.management import call_command
        from django.core.management.base import CommandError

        try:
            call_command('populate')
            self.assertTrue(Channel.objects.exists())
            self.assertTrue(Content.objects.exists())
            self.assertTrue(Group.objects.exists())
        except CommandError as e:
            self.fail(f"populate command failed: {str(e)}")
