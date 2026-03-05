import psycopg2
from psycopg2.extras import RealDictCursor
from django.conf import settings
from typing import List, Any
from pprint import pprint

db_sett = settings.DATABASES["default"]


class DBHelper:
    # initialize
    def __init__(self):
        self.conn_params = {
            "dbname": db_sett["NAME"],
            "user": db_sett["USER"],
            "password": db_sett["PASSWORD"],
            "host": db_sett["HOST"],
            "port": db_sett["PORT"],
        }

    # db connect
    def _get_connection(self):
        try:
            return psycopg2.connect(**self.conn_params)
        except Exception as e:
            print(f"[DB ERROR] Failed to connect to DB: {e}")
            return None

    # execute query
    def execute_query(self, query: str = None, params: List[Any] = None) -> List[Any]:
        print(f"QUERY: {str(query)}")
        print(f"PARAMS: {str(params)}")
        conn = self._get_connection()
        if not conn:
            return []

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query or "", params or [])
                print("[DB INFO] Query executed successfully!")
                # commit if DML
                if any((x in query.upper()) for x in ("INSERT", "UPDATE", "DELETE")):
                    conn.commit()
                    print("[DB INFO] Changes commited!")
                    print(f"[DB INFO] Records affected: {cur.rowcount}")

                records = cur.fetchall() or []
                print(f"[DB INFO] Records fetched: {len(records)}")
                pprint({"RECORDS": records or []})
                return records if records else []
        except Exception as e:
            print(f"[DB ERROR] Failed to execute query: {e}")
            return []
        finally:
            conn.close()
