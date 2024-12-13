import logging
from django.core.management.base import BaseCommand
from api.models import Group, Content, Channel

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Populate the database with initial data"

    def handle(self, *args, **kwargs):
        try:
            # Create groups
            group1 = Group.objects.create(name="Movies")
            group2 = Group.objects.create(name="TV Shows")

            # Create contents
            content1 = Content.objects.create(
                title="Inception",
                metadata={"genre": "Sci-Fi", "director": "Christopher Nolan"},
                rating=9.0,
            )
            content2 = Content.objects.create(
                title="Breaking Bad - S1E1",
                metadata={"genre": "Drama", "director": "Vince Gilligan"},
                rating=8.5,
            )

            # Create channels
            channel1 = Channel.objects.create(title="Blockbuster Movies", language="en")
            channel1.groups.add(group1)
            channel1.contents.add(content1)

            channel2 = Channel.objects.create(title="Popular TV Shows", language="en")
            channel2.groups.add(group2)
            channel2.contents.add(content2)

            # Create hierarchical channel
            main_channel = Channel.objects.create(title="Entertainment Hub", language="en")
            main_channel.groups.add(group1, group2)
            main_channel.subchannels.add(channel1, channel2)

            self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
        except Exception as e:
            logger.error(f"Error populating data: {str(e)}")
            self.stderr.write(self.style.ERROR("Failed to populate data."))
