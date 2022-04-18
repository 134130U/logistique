import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import requests
import  psycopg2
from psycopg2 import Error
import json
import ast


def get_data():

    sql_file = open('query/stock.sql')
    sql_file2 = open('query/age.sql')
    sql_text = sql_file.read()
    sql_text2 = sql_file2.read()
    try:
        connection = psycopg2.connect(user='postgres',
                                      password='3uyePAXP6J',
                                      host='212.47.226.25',
                                      port='5432',
                                      database='oolusolar_analytics')
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print('You are Successfully connected to - ', record, '\n')

        kpi_data = pd.read_sql_query(sql_text, connection)
        age = pd.read_sql_query(sql_text2, connection)
        kpi_data.to_csv('Data/stock.csv', index=False)
        age.to_csv('Data/age.csv', index=False)
        print('data updated')
    except (Exception, Error) as error:
        print(" Connection failed, try again", error)
        cursor.close()

    cursor.close()
    connection.close()

    return ''