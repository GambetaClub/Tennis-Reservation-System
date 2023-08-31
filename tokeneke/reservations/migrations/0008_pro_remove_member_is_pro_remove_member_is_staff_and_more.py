# Generated by Django 4.1.10 on 2023-08-24 15:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import reservations.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('reservations', '0007_date_assigned_pros'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('level', models.IntegerField(default=50, validators=[reservations.validators.validate_percentage])),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=7)),
                ('profile_pic', models.ImageField(default='profile_pics/default.jpeg', upload_to='profile_pics')),
                ('is_active', models.BooleanField(default=True)),
                ('schedule', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=7)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='pros', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='pros_permissions', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='member',
            name='is_pro',
        ),
        migrations.RemoveField(
            model_name='member',
            name='is_staff',
        ),
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(choices=[('private', 'Private Lesson'), ('private', 'Semi-Private Lesson'), ('court', 'Court Reservation'), ('clinic', 'Clinic')], max_length=20),
        ),
        migrations.AlterField(
            model_name='member',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='members', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AlterField(
            model_name='member',
            name='level',
            field=models.IntegerField(default=50, validators=[reservations.validators.validate_percentage]),
        ),
        migrations.AlterField(
            model_name='member',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='members_permissions', to='auth.permission'),
        ),
        migrations.CreateModel(
            name='TeachingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_registered', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.date')),
                ('pro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.pro')),
            ],
        ),
    ]
