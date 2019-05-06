from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import Article, ArticleChange
from articles.serializers import ArticleSerializer, ArticleChangeSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleChangesListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArticleChange.objects.all()
    serializer_class = ArticleChangeSerializer


class SetCurrentChangeSetView(APIView):
    serializer_class = ArticleSerializer
    queryset = ArticleChange.objects.all()

    def post(self, request, changeset_id=None):
        try:
            instance = self.queryset.get(id=changeset_id)
        except Exception:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        pre_current = self.queryset.filter(article=instance.article, is_current=True).first()
        pre_current.is_current = False
        pre_current.save()
        instance.is_current = True
        instance.save()
        article = instance.article
        article.title = instance.title_diff
        article.text = instance.restore()
        article.save()
        serializer = self.serializer_class(instance=article)
        return Response(serializer.data, status=status.HTTP_200_OK)
