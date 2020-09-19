import pandas as pd
import pymysql
import pymysql.cursors
from sqlalchemy import create_engine


host = '127.0.0.1'
port = '3306'
sid = 'League Of Legends'

user = 'root'
password = 'tmddk720'
    

    
def get_data(sql):
    con = pymysql.connect(host=host, user=user, password=password, db=sid, charset='utf8')
    
    try:
        db = pd.read_sql(sql, con=con)
    except Exception as e:
        print(e)
    finally:
        con.close()
        
    return db
    
"""
returns summoners DataFrame whose tier is 'tier' and rank is 'rank'

tier : CHALLENGER, GRANDMASTER, MASTER, DIAMOND
rank : I, II, III, IV
"""
def get_league_queue(tier, rank='I'):
    
    con = pymysql.connect(host=host, user=user, password=password, db=sid, charset='utf8')
    
    try:
        league_queue_db = pd.read_sql("SELECT * FROM league_queue where tier = '" + tier + "' and `rank` = '" + rank + "'", con=con)
    except Exception as e:
        print(e)
    finally:
        con.close()
        
    return league_queue_db



def get_summoner(summonerId):
    
    con = pymysql.connect(host=host, user=user, password=password, db=sid, charset='utf8')
    
    try:
        summoner_db = pd.read_sql("SELECT * FROM summoners where summonerId = '" + summonerId + "'", con=con)
    except Exception as e:
        print(e)
    finally:
        con.close()
        
    return summoner_db



def get_recent_gameId(summonerId):
    
    con = pymysql.connect(host=host, user=user, password=password, db=sid, charset='utf8')
    sql = """SELECT gameId FROM `League Of Legends`.matchlists t1 
                WHERE t1.timestamp = (SELECT t2.timestamp FROM `League Of Legends`.matchlists t2 
                                        WHERE t2.summonerId = '%s' 
                                        ORDER BY t2.timestamp DESC LIMIT 1);""" %(summonerId)
    try:
        with con.cursor() as cursor:
            cursor.execute(sql)
            fetch = cursor.fetchall()
            
            if len(fetch) == 0:
                gameId = np.nan
            else:
                gameId = int(fetch[0][0])
    except Exception as e:
        print(e)
    finally:
        con.close()
    
    return gameId


def get_gameId_list(queue='420', tier='CHALLENGER'):
    
    con = pymysql.connect(host=host, user=user, password=password, db=sid, charset='utf8')
    sql = """SELECT gameId FROM matchlists JOIN league_queue ON matchlists.summonerId = league_queue.summonerId
                WHERE queue = %s AND tier = '%s' ORDER BY timestamp DESC;""" %(queue, tier)

    try:
        with con.cursor() as cursor:
            cursor.execute(sql)
            fetch = cursor.fetchall()
            
            if len(fetch) == 0:
                gameId_list = np.nan
            else:
                gameId_list = [int(x[0]) for x in fetch]
                
    except Exception as e:
        print(e)
    finally:
        con.close()
    
    return gameId_list