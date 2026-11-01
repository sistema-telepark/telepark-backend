import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0026_alter_vinculo_unique_together_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personaep',
            old_name='fecha_inicio',
            new_name='fecha_ingreso',
        ),
        migrations.AlterField(
            model_name='personaep',
            name='fecha_ingreso',
            field=models.DateField(default=django.utils.timezone.localdate),
        ),
    ]
