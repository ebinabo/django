from snippets.api.views import SnippetViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('snippets', SnippetViewSet)