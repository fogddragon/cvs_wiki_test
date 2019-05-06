from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from articles.views import ArticleViewSet, ArticleChangesListViewSet, SetCurrentChangeSetView

router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet)
router.register(r'article_changeset', ArticleChangesListViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^set_changeset/(?P<changeset_id>\d+)/?$', SetCurrentChangeSetView.as_view()),

]