# Generated by Django 2.2.1 on 2019-10-13 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todonow', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='value',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]