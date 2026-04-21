import pymysql
import json
from datetime import datetime, date
from decimal import Decimal

def custom_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    if isinstance(obj, Decimal):
        return float(obj)

    if isinstance(obj, (bytes, bytearray)):
        return obj.decode("utf-8", errors="ignore")  # safe convert

    raise TypeError(f"Type not serializable: {type(obj)}")

conn = pymysql.connect(
    host="localhost",
    user="django_user",
    password="1234",
    database="dipstick_db"
)

cursor = conn.cursor()

cursor.execute("SHOW TABLES")
tables = [t[0] for t in cursor.fetchall()]

data = {}

for table in tables:
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    cursor.execute(f"DESCRIBE {table}")
    columns = [col[0] for col in cursor.fetchall()]

    data[table] = [
        dict(zip(columns, row))
        for row in rows
    ]

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=4,
        default=custom_serializer
    )

print("Export done!")