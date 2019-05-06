import difflib
import json

from rest_framework import routers, serializers, viewsets

from articles.models import Article, ArticleChange


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'creation_datetime',)
        read_only_fields = ('id', 'creation_datetime')

    def update(self, instance, validated_data):
        deffer = difflib.Differ()
        diff = deffer.compare(validated_data['text'].split('\n'), instance.text.split('\n'))
        list_diff = list(diff)
        if list_diff or  instance.title != validated_data['title']:
            previous_changeset = ArticleChange.objects.filter(article=instance, is_current=True).first()
            ArticleChange(
                title_diff=validated_data['title'],
                text_diff = json.dumps(list_diff),
                article = instance,
                previous_change = previous_changeset
            ).save()
            if previous_changeset:
                previous_changeset.is_current = False
                previous_changeset.save()
        instance = super().update(instance, validated_data)
        return instance

class ArticleChangeSerializer(serializers.ModelSerializer):
    restored_text = serializers.SerializerMethodField()



    class Meta:
        model = ArticleChange
        fields = (
            'id', 'title_diff', 'restored_text', 'article',
            'previous_change', 'creation_datetime', 'is_current', 'is_banned'
        )

    def get_restored_text(self, instance):
        return instance.restore()
