from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0007_alter_evento_persona_ep_alter_evento_tipo_evento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoevento',
            name='nombre',
            field=models.CharField(max_length=45),
        ),
    ]
