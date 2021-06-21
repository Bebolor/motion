from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response

from comment.models import Comment
from comment.serializers import NewCommentSerializer
from post.models import Post


class ListCreateComment(ListCreateAPIView):
    serializer_class = NewCommentSerializer

    def create(self, request, *args, **kwargs):
        author = self.request.user
        post = self.kwargs['pk']
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, post_id=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(post_id=self.kwargs['pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

