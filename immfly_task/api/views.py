from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Channel, Content, Group
from .serializers import ChannelSerializer, ContentSerializer, GroupSerializer
import logging

logger = logging.getLogger(__name__)

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    def list(self, request, *args, **kwargs):
        try:
            group = request.query_params.get('group', None)
            if group:
                self.queryset = self.queryset.filter(groups__name=group)
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error listing channels: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
