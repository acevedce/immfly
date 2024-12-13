import csv
from django.core.management.base import BaseCommand
from api.models import Channel
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Export channel ratings to a CSV file'

    def handle(self, *args, **kwargs):
        try:
            with open('channel_ratings.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Channel Title', 'Average Rating'])

                for channel in Channel.objects.all():
                    rating = channel.calculate_rating()
                    if rating is not None:
                        writer.writerow([channel.title, round(rating, 2)])

            self.stdout.write(self.style.SUCCESS('Ratings exported successfully!'))
        except Exception as e:
            logger.error(f"Error exporting ratings: {str(e)}")
            self.stderr.write(self.style.ERROR('Failed to export ratings'))
