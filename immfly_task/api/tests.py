import pytest
from api.models import Channel, Content

@pytest.mark.django_db
def test_channel_rating():
    content = Content.objects.create(title="Test Content", rating=7.5)
    channel = Channel.objects.create(title="Test Channel")
    channel.contents.add(content)

    assert channel.calculate_rating() == 7.5
