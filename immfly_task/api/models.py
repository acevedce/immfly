from django.db import models
import logging

logger = logging.getLogger(__name__)

class Group(models.Model):
    """Represents a group that a channel can belong to."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Content(models.Model):
    """Represents a piece of content, such as a video, PDF, or text."""
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="contents/")  # File upload directory
    metadata = models.JSONField(default=dict)  # Flexible metadata field
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # Rating between 0 and 10

    def __str__(self):
        return self.title

class Channel(models.Model):
    """Represents a channel that organizes content and subchannels."""
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=10)
    picture = models.ImageField(upload_to="channels/")  # Image upload directory
    groups = models.ManyToManyField(Group, related_name="channels", blank=True)
    parent_channel = models.ForeignKey(
        "self", null=True, blank=True, related_name="subchannels", on_delete=models.CASCADE
    )
    contents = models.ManyToManyField(Content, related_name="channels", blank=True)

    def __str__(self):
        return self.title

    def calculate_rating(self) -> float:
        """
        Calculate the average rating for this channel.
        - If the channel has contents, the rating is the average of its contents' ratings.
        - If it has subchannels, the rating is the average of its subchannels' ratings.
        - If no valid ratings are present, the rating is None.
        """
        try:
            if self.contents.exists():  # Case: Channel contains contents
                return self.contents.aggregate(models.Avg("rating"))['rating__avg'] or 0.0

            elif self.subchannels.exists():  # Case: Channel contains subchannels
                ratings = [
                    sub.calculate_rating() for sub in self.subchannels.all()
                    if sub.calculate_rating() is not None
                ]
                return sum(ratings) / len(ratings) if ratings else None

        except Exception as e:
            logger.error(f"Error calculating rating for channel {self.title}: {str(e)}")
            return None
