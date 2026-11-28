from django.db import migrations, models


def eliminar_eventos_sin_fecha_desde(apps, schema_editor):
    evento = apps.get_model('eventos', 'Evento')
    evento.objects.filter(fecha_desde__isnull=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('eventos', '0008_alter_tipoevento_nombre'),
    ]

    operations = [
        migrations.RunPython(
            eliminar_eventos_sin_fecha_desde,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='evento',
            name='fecha_desde',
            field=models.DateField(),
        ),
    ]
