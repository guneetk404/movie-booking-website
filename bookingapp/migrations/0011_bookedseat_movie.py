# Generated by Django 4.0.4 on 2022-05-16 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0010_bookedseat_cinema'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedseat',
            name='movie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookingapp.movie'),
            preserve_default=False,
        ),
    ]
