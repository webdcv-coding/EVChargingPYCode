from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg
import json
import os

app = FastAPI()
db_password = os.environ['DATABASE_URL']


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)


@app.get('/charging_stations')
def get_charging_stations(xmin,ymin,xmax,ymax):
    with psycopg.connect(db_password).cursor as cursor:
        cursor.execute('SELECT ST_X(CAST(location AS geometry)), ST_Y(CAST(location AS geometry)), api_id FROM ireland_chargers WHERE location && ST_MakeEnvelope(%s,%s,%s,%s,4326);',params=(xmin,ymin,xmax,ymax))
        sql_data = cursor.fetchall()
        return {"stations":sql_data}




