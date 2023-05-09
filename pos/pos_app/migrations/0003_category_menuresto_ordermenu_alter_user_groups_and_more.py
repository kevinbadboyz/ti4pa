# Generated by Django 4.0 on 2023-04-17 05:04

from django.db import migrations, models
import django.db.models.deletion
import pos_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('pos_app', '0002_tableresto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif', max_length=15)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuResto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=pos_app.models.increment_menu_resto_code, editable=False, max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=200)),
                ('image_menu', models.ImageField(blank=True, default='default_images/empty.jpg', null=True, upload_to='menu_images/')),
                ('menu_status', models.CharField(choices=[('Ada', 'Ada'), ('Habis', 'Habis')], default='Ada', max_length=15)),
                ('status', models.CharField(choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif', max_length=15)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_menu', to='pos_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=pos_app.models.increment_order_menu_code, editable=False, max_length=20)),
                ('order_status', models.CharField(choices=[('Belum Bayar', 'Belum Bayar'), ('Sudah Bayar', 'Sudah Bayar')], default='Belum Bayar', max_length=15)),
                ('total_order', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('tax_order', models.FloatField(blank=True, default=0, null=True)),
                ('total_payment', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('payment', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('changed', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif', max_length=15)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default='default_images/person.jpg', null=True, upload_to='profile_images/')),
                ('bio', models.TextField()),
                ('status', models.CharField(choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif', max_length=15)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='user_profile', to='pos_app.user')),
                ('user_create', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_create_profile', to='pos_app.user')),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_update_profile', to='pos_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMenuDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('order_menu_detail_status', models.CharField(choices=[('Sedang disiapkan', 'Sedang disiapkan'), ('Sudah disajikan', 'Sudah disajikan')], default='Sedang disiapkan', max_length=30)),
                ('status', models.CharField(choices=[('Aktif', 'Aktif'), ('Hapus', 'Hapus')], default='Aktif', max_length=15)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('menu_resto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='menu_resto_order_menu_detail', to='pos_app.menuresto')),
                ('order_menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_menu_order_menu_detail', to='pos_app.ordermenu')),
                ('user_create', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_create_order_menu_detail', to='pos_app.user')),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_update_order_menu_detail', to='pos_app.user')),
            ],
        ),
        migrations.AddField(
            model_name='ordermenu',
            name='cashier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cashier_order_menu', to='pos_app.user'),
        ),
        migrations.AddField(
            model_name='ordermenu',
            name='table_resto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='table_resto_order_menu', to='pos_app.tableresto'),
        ),
        migrations.AddField(
            model_name='ordermenu',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_create_order_menu', to='pos_app.user'),
        ),
        migrations.AddField(
            model_name='ordermenu',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_update_order_menu', to='pos_app.user'),
        ),
        migrations.AddField(
            model_name='ordermenu',
            name='waitress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='waitress_order_menu', to='pos_app.user'),
        ),
        migrations.AddField(
            model_name='menuresto',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_create_menu', to='pos_app.user'),
        ),
        migrations.AddField(
            model_name='menuresto',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_update_menu', to='pos_app.user'),
        ),
        migrations.AddField(
            model_name='category',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_create_category', to='pos_app.user'),
        ),
        migrations.AddField(
            model_name='category',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_update_category', to='pos_app.user'),
        ),
    ]
