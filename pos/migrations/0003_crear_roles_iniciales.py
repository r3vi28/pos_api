from django.db import migrations


def crear_roles(apps, schema_editor):
    Rol = apps.get_model('pos', 'Rol')
    Rol.objects.create(nombre='Admin')
    Rol.objects.create(nombre='Usuario estándar')


def eliminar_roles(apps, schema_editor):
    Rol = apps.get_model('pos', 'Rol')
    Rol.objects.filter(nombre__in=['Admin', 'Usuario estándar']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0002_rol_alter_venta_atendido_por_perfil'),
    ]

    operations = [
        migrations.RunPython(crear_roles, eliminar_roles),
    ]