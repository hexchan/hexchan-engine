# Generated by Django 2.1.5 on 2019-01-27 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0002_auto_20190127_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ban',
            name='type',
            field=models.CharField(choices=[('ip', 'IP address'), ('network', 'network'), ('session', 'Session')], max_length=8),
        ),
    ]
