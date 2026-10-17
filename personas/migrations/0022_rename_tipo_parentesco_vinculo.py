from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0021_remove_persona_borrado_persona_activo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TipoParentesco',
            new_name='Vinculo',
        ),
        migrations.RenameField(
            model_name='vinculo',
            old_name='id_tipo_parentesco',
            new_name='id_vinculo',
        ),
        migrations.AlterModelTable(
            name='vinculo',
            table='personas_vinculo',
        ),
    ]
