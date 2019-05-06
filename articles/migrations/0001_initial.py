# Generated by Django 2.2.1 on 2019-05-06 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=5000)),
                ('creation_datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_diff', models.CharField(max_length=100)),
                ('text_diff', models.TextField(max_length=5000)),
                ('creation_datetime', models.DateTimeField(auto_now=True)),
                ('is_banned', models.BooleanField(default=False)),
                ('is_current', models.BooleanField(default=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Article')),
                ('previous_change', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.ArticleChange')),
            ],
        ),
    ]
