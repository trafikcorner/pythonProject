# Generated by Django 4.2.2 on 2023-08-14 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trafik_app', '0002_odbe_rk_kv_delete_kvinfomodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='odberkrv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ndn', models.CharField(max_length=10)),
                ('megnevezes', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='ODBE_RK_KV',
        ),
    ]