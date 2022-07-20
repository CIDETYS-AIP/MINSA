# Generated by Django 3.0.11 on 2022-05-20 04:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('source_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataSourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('type', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('from_date', models.DateTimeField(blank=True, null=True)),
                ('to_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StatisticalModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RealValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('label', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='real_values', to='covid_models.DataSource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ForecastedValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('label', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('forecast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecasted_values', to='covid_models.Forecast')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ForecastDataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('access_date', models.DateTimeField()),
                ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_as_data_in_following_forecasts', to='covid_models.DataSource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='forecast',
            name='forecast_data_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecast', to='covid_models.ForecastDataSource'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='statistical_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecasts', to='covid_models.StatisticalModel'),
        ),
        migrations.AddField(
            model_name='datasource',
            name='source_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_sources', to='covid_models.DataSourceType'),
        ),
    ]