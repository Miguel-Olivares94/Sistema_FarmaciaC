# Generated by Django 5.0 on 2023-12-19 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmacia', '0012_medicamento_historial_ventas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicamento',
            name='historial_ventas',
        ),
    ]