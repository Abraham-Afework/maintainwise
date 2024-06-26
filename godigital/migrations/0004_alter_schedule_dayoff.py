# Generated by Django 4.0.6 on 2024-06-06 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_delete_posts_remove_technicians_day_off_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='dayoff',
            field=models.CharField(choices=[('mon-tue', 'Mon-Tue'), ('tue-wed', 'Tue-Wed'), ('wed-thur', 'Wed-Thur'), ('thu-fri', 'Thu-Fri'), ('fri-sat', 'Fri-Sat'), ('sat-sun', 'Sat-Sun'), ('sun-mon', 'Sun-Mon')], max_length=8),
        ),
    ]