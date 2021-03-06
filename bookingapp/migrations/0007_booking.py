# Generated by Django 4.0.4 on 2022-05-15 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0006_cinema'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('price', models.IntegerField()),
                ('tickets', models.IntegerField()),
                ('seats', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookingapp.cinema')),
            ],
        ),
    ]
