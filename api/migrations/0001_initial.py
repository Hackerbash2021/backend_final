# Generated by Django 2.2 on 2021-02-28 04:13

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.EmailField(max_length=320, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=400)),
                ('phone', models.CharField(max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', api.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=100)),
                ('accessibility', models.BooleanField(default=False)),
                ('class_count', models.IntegerField()),
                ('org_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OrgClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_code', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('api.user',),
            managers=[
                ('objects', api.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('org_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.OrgClass')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='UserClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_class', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.OrgClass')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student')),
            ],
        ),
        migrations.CreateModel(
            name='OrgAdmin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('organization', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.user',),
            managers=[
                ('objects', api.models.UserManager()),
            ],
        ),
    ]
