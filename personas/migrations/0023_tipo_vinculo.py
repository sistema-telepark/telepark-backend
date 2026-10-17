from django.db import migrations, models


def deduplicar_y_mapear_tipos(apps, schema_editor):
    TipoVinculo = apps.get_model('personas', 'TipoVinculo')
    Vinculo = apps.get_model('personas', 'Vinculo')

    nombres = list(
        Vinculo.objects.exclude(nombre__isnull=True)
        .exclude(nombre='')
        .values_list('nombre', flat=True)
        .distinct()
    )
    for nombre in nombres:
        tipo_vinculo = TipoVinculo.objects.create(nombre=nombre)
        Vinculo.objects.filter(nombre=nombre).update(tipo_vinculo=tipo_vinculo)

    placeholder, _ = TipoVinculo.objects.get_or_create(nombre='Sin especificar')
    Vinculo.objects.filter(models.Q(nombre__isnull=True) | models.Q(nombre='')).update(
        tipo_vinculo=placeholder
    )


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0022_rename_tipo_parentesco_vinculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoVinculo',
            fields=[
                ('id_tipo_vinculo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'personas_tipo_vinculo',
            },
        ),
        migrations.AddField(
            model_name='vinculo',
            name='tipo_vinculo',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.PROTECT,
                to='personas.tipovinculo',
            ),
        ),
        migrations.RunPython(deduplicar_y_mapear_tipos, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='vinculo',
            name='tipo_vinculo',
            field=models.ForeignKey(
                on_delete=models.PROTECT,
                to='personas.tipovinculo',
            ),
        ),
        migrations.RemoveField(
            model_name='vinculo',
            name='nombre',
        ),
    ]
