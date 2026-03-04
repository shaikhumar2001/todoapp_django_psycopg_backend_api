import psycopg2
from psycopg2.extras import RealDictCursor
from django.conf import settings
import os
from pprint import pprint

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoapp_project.settings')

db_set = settings.DATABASES['default']

conn = psycopg2.connect(**{
        'dbname': db_set['NAME'],
        'user': db_set['USER'],
        'password': db_set['PASSWORD'],
        'host': db_set['HOST'],
        'port': db_set['PORT'],
    })

cur = conn.cursor(cursor_factory=RealDictCursor)

cur.execute('SELECT * FROM todoapp.tusertbl')

result = cur.fetchall()

pprint(result)

conn.close()
