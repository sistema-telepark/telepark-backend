from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='personaep',
                    name='idpersona',
                ),
                migrations.AddField(
                    model_name='personaep',
                    name='persona_ptr',
                    field=models.OneToOneField(
                        db_column='idPersona',
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='personas.persona',
                    ),
                    preserve_default=False,
                ),
                migrations.AlterUniqueTogether(
                    name='personaep',
                    unique_together=set(),
                ),
                migrations.AlterField(
                    model_name='tipoparentesco',
                    name='idpersonaep',
                    field=models.ForeignKey(
                        db_column='idPersonaEP',
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='+',
                        to='personas.personaep',
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]
