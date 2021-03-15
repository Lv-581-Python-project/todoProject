# Generated by Django 3.1.7 on 2021-03-11 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=256)),
                ('is_completed', models.BooleanField(default=False)),
                ('deadline', models.DateField()),
                ('list_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.todolist')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
