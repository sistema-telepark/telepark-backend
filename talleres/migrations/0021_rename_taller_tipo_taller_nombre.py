from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('talleres', '0020_encuentro_taller'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taller',
            old_name='tipo_taller',
            new_name='nombre',
        ),
    ]
