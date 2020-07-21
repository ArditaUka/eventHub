# Generated by Django 2.2 on 2020-07-21 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventHub_app', '0014_delete_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('category', models.CharField(max_length=100)),
                ('tickets', models.IntegerField()),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_events', to='eventHub_app.User')),
                ('users', models.ManyToManyField(related_name='events', to='eventHub_app.User')),
            ],
        ),
    ]
