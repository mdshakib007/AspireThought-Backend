from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from tag.models import Tag
from tag.serializers import TagSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend



class AddTagAPIView(APIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success" : "Tag Added!"})
        return serializer.errors


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Tag.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.request.query_params.get('tag_id')

        if tag_id:
            queryset = queryset.filter(id=tag_id)

        return queryset