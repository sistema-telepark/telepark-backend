import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0024_alter_departamento_provincia_and_more'),
        ('talleres', '0015_alter_asistenciataller_encuentro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistenciataller',
            name='encuentro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='talleres.encuentro'),
        ),
        migrations.AlterField(
            model_name='asistenciataller',
            name='persona_ep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personas.personaep'),
        ),
    ]
