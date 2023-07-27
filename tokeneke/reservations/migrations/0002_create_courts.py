from django.db import migrations


def create_courts(apps, schema_editor):
    Court = apps.get_model('reservations', 'Court')
    Court.objects.bulk_create([
        Court(name='Stadium Court'),
        Court(name='Court 1'),
        Court(name='Court 2'),
        Court(name='Court 3'),
        Court(name='Court 4'),
        Court(name='Court 5'),
        Court(name='Court 6'),
        Court(name='Court 7'),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_courts),
    ]
