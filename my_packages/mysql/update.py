import pymysql
import pymysql.cursors
import pandas as pd
from sqlalchemy import create_engine

"""
upload pandas.DataFrame to mysql database
"""
def upload_df(host, port, sid, user, password, table, df, if_exists='append'):
    
    connection = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                db=sid,
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)

    engine = create_engine("mysql+pymysql://{user}:{password}@{host}/{db}"
                        .format(user=user, password=password, host=host, db=sid))


    try:
        with connection.cursor() as cursor:
            df.to_sql(name=table, con=engine, if_exists=if_exists, index=False)
            connection.commit()
    
    except Exception as e:
        print(e)
                
    finally:
        connection.close()
        
        
        
"""
update mysql database using 'sql' command
"""     
def update_db(host, port, sid, user, password, sql, values, option='one'):
    
    connection = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                db=sid,
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            if option == 'one':
                cursor.execute(sql, values)
            elif option == 'many':
                cursor.executemany(sql, values)
                
            connection.commit()
    
    except Exception as e:
        print(e)
                
    finally:
        connection.close()