# Generated by Django 3.1.3 on 2021-05-15 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210512_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.role'),
        ),
    ]
