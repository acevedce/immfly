from rest_framework import serializers
from .models import Content, Channel, Group

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class ChannelSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    subchannels = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'title', 'language', 'picture', 'contents', 'subchannels', 'rating']

    def get_subchannels(self, obj):
        return ChannelSerializer(obj.subchannels.all(), many=True).data

    def get_rating(self, obj):
        return obj.calculate_rating()
