# Generated by Django 3.0.1 on 2020-02-11 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0014_auto_20200211_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='height',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='Height'),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumb_height',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='Thumb height'),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumb_width',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='Thumb width'),
        ),
        migrations.AlterField(
            model_name='image',
            name='width',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='Width'),
        ),
    ]
