# Generated by Django 4.1.7 on 2023-02-24 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_alter_member_member_n_alter_member_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_pic',
            field=models.ImageField(default='default.jpeg', upload_to='profile_pics'),
        ),
    ]