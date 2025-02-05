# Generated by Django 3.2.6 on 2021-08-16 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='nome')),
                ('num_participants', models.PositiveSmallIntegerField(verbose_name='quantidade de participantes')),
                ('num_chairs', models.PositiveSmallIntegerField(verbose_name='quantidade de cadeiras')),
            ],
            options={
                'verbose_name': 'sala',
                'verbose_name_plural': 'salas',
                'ordering': ('name',),
            },
        ),
    ]
