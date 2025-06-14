# Generated by Django 5.2.1 on 2025-06-10 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1_name', models.CharField(max_length=30)),
                ('player2_name', models.CharField(max_length=30)),
                ('player1_score', models.IntegerField()),
                ('player2_score', models.IntegerField()),
                ('played_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
