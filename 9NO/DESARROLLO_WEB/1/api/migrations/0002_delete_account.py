# Generated manually to drop Account if 0001 already created it.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[],
            database_operations=[
                migrations.RunSQL(
                    sql="DROP TABLE IF EXISTS api_account;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
        ),
    ]
