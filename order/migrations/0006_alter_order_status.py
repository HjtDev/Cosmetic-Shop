# Generated by Django 5.1.2 on 2024-10-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_extra_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('در صف برسی', 'در صف برسی'), ('تایید سفارش', 'تایید سفارش'), ('آماده سازی سفارش', 'آماده سازی سفارش'), ('در حال ارسال', 'در حال ارسال'), ('تکمیل شد', 'تکمیل شد')], default='در صف برسی', max_length=21, verbose_name='وضعیت'),
        ),
    ]
