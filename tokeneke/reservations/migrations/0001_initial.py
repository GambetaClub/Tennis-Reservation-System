# Generated by Django 4.1.10 on 2023-07-13 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import recurrence.fields
import reservations.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('member_n', models.CharField(blank=True, max_length=10, verbose_name='Member #')),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('level', models.IntegerField(null=True, validators=[reservations.validators.validate_percentage])),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=7)),
                ('team', models.CharField(blank=True, choices=[('A', 'A-Team'), ('B', 'B-Team'), ('C', 'C-Team'), ('No-Team', 'No-Team')], max_length=7)),
                ('profile_pic', models.ImageField(default='profile_pics/default.jpeg', upload_to='profile_pics')),
                ('is_playing', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('private', 'Private Lesson'), ('court', 'Court Reservation'), ('clinic', 'Clinic')], max_length=20)),
                ('title', models.CharField(blank=True, max_length=120, verbose_name='Activity Title')),
                ('recurrences', recurrence.fields.RecurrenceField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='End Time')),
                ('capacity', models.IntegerField(default=4, verbose_name='Capacity')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_start', models.DateTimeField()),
                ('datetime_end', models.DateTimeField()),
                ('capacity', models.IntegerField(default=12, verbose_name='Capacity')),
                ('court', models.CharField(choices=[('Stadium', 'Stadium Court'), ('1', 'Court 1'), ('2', 'Court 2'), ('3', 'Court 3'), ('4', 'Court 4'), ('5', 'Court 5'), ('6', 'Court 6'), ('7', 'Court 7')], default='Stadium', max_length=20)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.activity')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Event Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('MIXED', 'Mixed')], max_length=7, verbose_name='Gender')),
                ('team', models.CharField(blank=True, choices=[('A', 'A-Team'), ('B', 'B-Team'), ('C', 'C-Team'), ('No-Team', 'No-Team')], max_length=12, verbose_name='Team')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Venue Name')),
                ('address', models.CharField(max_length=300)),
                ('zip_code', models.CharField(max_length=10, verbose_name='Zip Code')),
                ('phone', models.CharField(max_length=30, verbose_name='Contact Phone')),
                ('web', models.URLField(verbose_name='Website Address')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_registered', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.date')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='date',
            name='participants',
            field=models.ManyToManyField(blank=True, through='reservations.Participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='event',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservations.event'),
        ),
        migrations.AddConstraint(
            model_name='participation',
            constraint=models.UniqueConstraint(fields=('member', 'date'), name='member_can_sign_in_once'),
        ),
    ]
