from snippets.models import Snippet 
from .serializers import SnippetSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters 

class SnippetFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr = 'icontains')

    class Meta:
        model = Snippet
        fields = ('title',)

class SnippetFilter2(filters.FilterSet):
    class Meta:
        model = Snippet
        fields = {
            'id': ['lte', 'gte'],
            'title': ['icontains'],
            'created': ['iexact', 'lte', 'gte']
        }

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    filterset_class = SnippetFilter2

    @action(methods = ['get'], detail = False)
    def newest(self, request):
        newest = self.get_queryset().order_by('created').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)
