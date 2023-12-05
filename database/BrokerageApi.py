import traceback
from fastapi import HTTPException, status
import psycopg2
from datetime import datetime, timedelta
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor
from database import rds_username, rds_password, rds_hostname, db_port, rds_db_name
import psycopg2.pool
# from psycopg2 import errors
import os 

CONNECTION_AWS = f"postgres://{rds_username}:{rds_password}@{rds_hostname}:{db_port}/{rds_db_name}"

connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=15,
    host=rds_hostname,
    port=db_port,
    user=rds_username,
    password=rds_password,
    database=rds_db_name
)
def temp() -> dict:
    return {"Message":"Pass"}

def table_exists(cursor, table_name):
    cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
    return cursor.fetchone()[0]

def create_table_if_not_exists(conn, table_name):
    cursor = conn.cursor()
    if not table_exists(cursor, table_name):
        ddl_file_path = os.path.join("SQL_Files", f"{table_name}.sql")
        if os.path.exists(ddl_file_path):
            with open(ddl_file_path, 'r') as ddl_file:
                ddl_statement = ddl_file.read()
                cursor.execute(ddl_statement)
                conn.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Table '{table_name}' DDL file not found in 'SQL_Files' directory."
            )

def get_credentials(brokerage_setting_id):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            query = f"SELECT password, vc, api_secret_key, imei, brokerage_user_id ,brokerage_id,token FROM sharkcap_db_brokerage_setting where brokerage_setting_id = {brokerage_setting_id}"
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query)
            data = cur.fetchone() 
            cur.close()
            conn.close()
            return data
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)
def get_brokerage_option():
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_list")

        try:
            query = "SELECT * FROM sharkcap_db_brokerage_list"
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            conn.close()
            return data
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)


def get_brokerage_user(brokerage_setting_id: int):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            query = "SELECT is_active FROM sharkcap_db_brokerage_setting WHERE brokerage_setting_id = %s"
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute(query, (brokerage_setting_id,))
            data = cur.fetchone()
            cur.close()
            conn.close()
            return data
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)

def get_subsctiber_user(brokerage_setting_id: int):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_strategy_subscriber")

        try:
            query = """SELECT brokerage_is_active FROM sharkcap_db_strategy_subscriber WHERE brokerage_setting_id = %s"""
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute(query, (brokerage_setting_id, ))
            data = cur.fetchone()
            cur.close()
            conn.close()
            return data
            
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)

def get_brokerage_info(user_id: int):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")
        try:
            query = """SELECT brokerage_id, brokerage_setting_id, brokerage_user_id, api_key, api_secret_key, is_active FROM sharkcap_db_brokerage_setting WHERE user_id = %s"""
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute(query, (user_id, ))
            data = cur.fetchall()
            cur.close()
            conn.close()
            return data
            
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)


def is_user_present(userid: int):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_strategy_subscriber")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT EXISTS(SELECT 1 FROM sharkcap_db_strategy_subscriber WHERE user_id = %s)"

            cur.execute(query, (userid,))
            user_exists = cur.fetchone()['exists']
            cur.close()
            conn.close()
            return user_exists
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)

def activate_brokerage_subscriber(brokerage_setting_id):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_strategy_subscriber")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "UPDATE sharkcap_db_strategy_subscriber SET brokerage_is_active = TRUE WHERE brokerage_setting_id = %s"

            cur.execute(query, (brokerage_setting_id, ))
            conn.commit()
            cur.close()
            conn.close()
            return {"message" : "Brokerage activated successfully."}
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("deactivate_brokerage: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)

def activate_brokerage(brokerage_setting_id):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "UPDATE sharkcap_db_brokerage_setting SET is_active = TRUE WHERE brokerage_setting_id = %s"

            cur.execute(query, (brokerage_setting_id, ))
            conn.commit()
            cur.close()
            conn.close()
            return {"message" : "Brokerage activated successfully."}
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("deactivate_brokerage: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)
    

def activate_paper(brokerage_setting_id):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "UPDATE sharkcap_db_brokerage_setting SET is_active = TRUE WHERE brokerage_setting_id = %s"

            cur.execute(query, (brokerage_setting_id, ))
            conn.commit()
            cur.close()
            conn.close()
            return {"message" : "Paper brokerage activated successfully."}
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("activate_paper: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)
    

def get_all_brokerage_list(userid: int) -> dict:
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT brokerage_setting_id, brokerage_id, is_active FROM sharkcap_db_brokerage_setting Where user_id = %s"
            cur.execute(query, (userid,))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("get_brokerage_list: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)

def get_active_brokerage_list(userid: int) -> dict:
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT brokerage_setting_id ,brokerage_id, is_active FROM sharkcap_db_brokerage_setting Where user_id = %s AND is_active = %s"
            cur.execute(query, (userid, True))
            data = cur.fetchall()
            cur.close()
            conn.close()
            return data
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("get_brokerage_list: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)


# def connect_brokerage(user_id: str, brokerage_user_id: str, password: str, factor2: str, vc: str, api_key: str, api_secret_key: str, imei: str, brokerage: str, brokerage_id: int) -> dict:
#     try:
#         conn = psycopg2.connect(CONNECTION_AWS)
#         conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#         try:
#             # query1 = f"""INSERT INTO sharkcap_db_brokerage_setting (id, user_id, password, factor2, vc, api_key, api_secret_key, imei, brokerage) VALUES ('{id}', '{user_id}', '{password}', '{factor2}', '{vc}', '{api_key}', '{api_secret_key}', '{imei}', '{brokerage}')"""
#             query1 = f"""INSERT INTO sharkcap_db_brokerage_setting (user_id, password, factor2, vc, api_key, api_secret_key, imei, brokerage, brokerage_user_id, is_active, brokerage_id) SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, false, %s WHERE NOT EXISTS (SELECT 1 FROM sharkcap_db_brokerage_setting WHERE user_id = %s AND brokerage_id = %s)"""
#             cur = conn.cursor()
#             cur.execute(query1, (user_id,password,factor2,vc,api_key,api_secret_key,imei, brokerage, brokerage_user_id,brokerage_id ,user_id, brokerage_id))
#             conn.commit()
#             cur.close()
#             conn.close()
#             if cur.rowcount:
#                 return {"message": "Brokerage connected successfully."}
#             else:
#                 return {"message": "Brokerage credential already exists."}
#         except Exception as e:
#             return {'Error': f"{e}, while fetching data"}
#     except Exception as ex:
#         print("connect_brokerage: exception in connecting to database")
#         print(ex)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="sorry for inconvenience! please contact admin!!")

# def activate_brokerage(userid: int, api_key: str, api_secret_key: str, brokerage: str) -> dict:

def connect_paper(user_id: str ,brokerage_id: str) -> dict:
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            query1 = f"""INSERT INTO sharkcap_db_brokerage_setting (user_id, brokerage_id) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM sharkcap_db_brokerage_setting WHERE user_id = %s AND brokerage_id = %s)"""
            cur = conn.cursor()
            cur.execute(query1, (user_id,brokerage_id ,user_id, brokerage_id))
            conn.commit()
            cur.close()
            conn.close()
            if cur.rowcount:
                return {"message": "Brokerage connected successfully."}
            else:
                return {"message": "Brokerage credential already exists."}
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("connect_brokerage: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)
#     try:
#         conn = psycopg2.connect(CONNECTION_AWS)
#         conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#         try:
#             query1 = """UPDATE sharkcap_db_brokerage_setting SET is_active = %s WHERE user_id = %s AND brokerage = %s AND (api_key = %s OR api_secret_key = %s)"""
#             cur = conn.cursor()
#             cur.execute(query1, (True, userid, brokerage, api_key, api_secret_key,))
#             conn.commit()
#             cur.close()
#             conn.close()
#             if cur.rowcount:
#                 return {"message": "Brokerage activated successfully."}
#             else:
#                 return {"message": "Invalid key."}
#         except Exception as e:
#             return {'Error': f"{e}, while fetching data"}
#     except Exception as ex:
#         print("activate_brokerage: exception in connecting to database")
#         print(ex)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="sorry for inconvenience! please contact admin!!")


# def activate_brokerage(id:int,  brokerage: str, user_id: str, password: str, factor2: str, vc: str, api_key: str, api_secret_key: str, imei: str, brokerage_user_id: str) -> dict:
#     try:
#         conn = psycopg2.connect(CONNECTION_AWS)
#         conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#         try:
#             is_active = True
#             query = """INSERT INTO sharkcap_db_strategy_subscriber(
# 	user_id, brokerage_setting_id, password, factor2, vc, api_key, api_secret_key, imei, brokerage, brokerage_user_id, is_active)
# 	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
#             cur = conn.cursor()
#             cur.execute(query, (user_id,id,password,factor2,vc,api_key,api_secret_key,imei, brokerage, brokerage_user_id, is_active))
#             conn.commit()
#             cur.close()
#             conn.close()
#             return {"message": "Brokerage activated successfully."}
#         except Exception as e:
#             return {'Error': f"{e}, while fetching data"}
#     except Exception as ex:
#         print("activate_brokerage: exception in connecting to database")
#         print(ex)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="sorry for inconvenience! please contact admin!!")

def get_brokerage_setting_id(user_id: int,brokerage_id:str):
    """get the brokerage setting id using user_id and brokerage_id"""
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT brokerage_setting_id FROM sharkcap_db_brokerage_setting WHERE user_id = %s and brokerage_id = %s"
            cur.execute(query, (user_id,brokerage_id, ))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)
    

def get_strategy_setting_id(strategy_id: int):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_strategy_setting")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT id FROM sharkcap_db_strategy_setting WHERE strategy_id = %s"
            cur.execute(query, (strategy_id, ))
            result = cur.fetchone()
            cur.close()
            return result
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)


def get_user_details(userid: int, brokerage_id: str):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT * FROM sharkcap_db_brokerage_setting WHERE user_id = %s AND brokerage_id = %s"
            cur.execute(query, (userid, brokerage_id))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)

def get_details(strategy_id:int, brokerage_setting_id: int, strategy_setting_id: int):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_strategy")
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")
        create_table_if_not_exists(conn, "sharkcap_db_strategy_setting")
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            print(strategy_id, brokerage_setting_id, strategy_setting_id)
            query = query = """
                                SELECT t3.brokerage_id, t3.password, t3.factor2, t3.vc, t3.api_key, t3.api_secret_key, t3.imei, t3.brokerage_user_id, t3.is_active as brokerage_is_active
                                FROM sharkcap_db_strategy AS t1
                                JOIN sharkcap_db_brokerage_setting AS t3 ON t3.brokerage_setting_id = %s
                                JOIN sharkcap_db_strategy_setting AS t2 ON t2.id = %s
                                WHERE t1.id = %s;

                            """
            cur.execute(query, (brokerage_setting_id, strategy_setting_id, strategy_id))
            result = cur.fetchone()
            cur.close()
            conn.close()
            print(result)
            return result
            
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("is_user_present: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)

def set_brokerage(id:int,  brokerage_id: str, user_id: str, password: str, factor2: str, vc: str, api_key: str, api_secret_key: str, imei: str, brokerage_user_id: str, strategy_id: int, strategy_setting_id: int, brokerage_is_active: int):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_strategy_subscriber")

        try:
            print(user_id,id,password,factor2,vc, api_key, api_secret_key, imei, brokerage_id, brokerage_user_id, strategy_id, strategy_setting_id, brokerage_is_active,"eegg")            
            query = """INSERT INTO sharkcap_db_strategy_subscriber(
	user_id, brokerage_setting_id, password, factor2, vc, api_key, api_secret_key, imei, brokerage, strategy_is_active, brokerage_user_id, strategy_id, strategy_setting_id, brokerage_is_active)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, false, %s, %s, %s, %s);"""
            cur = conn.cursor()
            cur.execute(query, (user_id,id,password,factor2,vc, api_key, api_secret_key, imei, brokerage_id, brokerage_user_id, strategy_id, strategy_setting_id, brokerage_is_active))
            conn.commit()
            cur.close()
            return {"message": "Brokerage set successfully."}
        # except psycopg2.IntegrityError as e:
        #         if isinstance(e.orig, errors.UniqueViolation):
        #             return {'Error': "Duplicate key value violates unique constraint."}
        except Exception as e:
            print({'Error': f"{e}, while inserting data"})
            return {"Message":f"Brokerage Already Exists"}
    except Exception as ex:
        print("set_brokerage: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)
    

def deactivate_brokerage_and_strategy(brokerage_setting_id) -> dict:
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_strategy_subscriber")
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            conn.autocommit = False

            query = "UPDATE sharkcap_db_strategy_subscriber SET brokerage_is_active = FALSE WHERE brokerage_setting_id = %s"
            query2 = "UPDATE sharkcap_db_brokerage_setting SET is_active = FALSE WHERE brokerage_setting_id = %s"
            cur.execute(query, (brokerage_setting_id, ))
            cur.execute(query2, (brokerage_setting_id, ))
            conn.commit()
            if cur.rowcount:
                return {"message": "Brokerage deactivated successfully."}
            else:
                return {"message": "Brokerage does not exists."}
        except Exception as e:
            conn.rollback()
            print(e)
            return {'Error': "Deactivation Failed."}
        finally:
            conn.autocommit = True
            cur.close()
    except Exception as ex:
        print("deactivate_brokerage: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)

def deactivate_brokerage(brokerage_setting_id) -> dict:
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "UPDATE sharkcap_db_brokerage_setting SET is_active = FALSE WHERE brokerage_setting_id = %s"
            cur.execute(query, (brokerage_setting_id,))
            conn.commit()
            cur.close()
            if cur.rowcount:
                return {"message": "Brokerage deactivated successfully."}
            else:
                return {"message": "Brokerage does not exists."}
        except Exception as e:
            print(e)
            return {'Error': "Deactivation Failed."} 
    except Exception as ex:
        print("deactivate_brokerage: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)

def remove_brokerage_setting(userid, brokerage_setting_id):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "DELETE FROM sharkcap_db_brokerage_setting WHERE user_id = %s AND brokerage_setting_id = %s"
            cur.execute(query, (userid, brokerage_setting_id))
            conn.commit()
            cur.close()
            if cur.rowcount:
                return {"message": "Brokerage removed successfully."}
            else:
                return {"message": "Brokerage does not exists."}
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("deactivate_brokerage: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)
        
def remove_stratsub_brokerage_setting(userid, brokerage_setting_id):
    try:
        conn = connection_pool.getconn()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_if_not_exists(conn, "sharkcap_db_strategy_subscriber")

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query = "DELETE FROM sharkcap_db_strategy_subscriber WHERE user_id = %s AND brokerage_setting_id = %s"
            cur.execute(query, (userid, brokerage_setting_id))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            return {'Error': f"{e}, while fetching data"}
    except Exception as ex:
        print("remove_stratsub_brokerage_setting: exception in connecting to database")
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sorry for inconvenience! please contact admin!!")
    finally:
        if conn:
            connection_pool.putconn(conn)
    


def edit_brokerage(brokerage_setting_id, user_id,brokerage_user_id, password, factor2, vc, api_key, api_secret_key, imei, brokerage_id):
    field_mapping = {
        "brokerage_user_id": brokerage_user_id,
        "password": password,
        "factor2": factor2,
        "vc": vc,
        "api_key": api_key,
        "api_secret_key": api_secret_key,
        "imei": imei,
        "brokerage_id": brokerage_id,
    }

    # Create a list of fields to update
    fields_to_update = [f"{field} = %s" for field, value in field_mapping.items() if value is not None]

    # If there are fields to update, proceed with the update query
    if fields_to_update:
        set_clause = ", ".join(fields_to_update)
        query = f"""
            UPDATE sharkcap_db_brokerage_setting
            SET {set_clause}
            WHERE brokerage_setting_id = %s;
        """

        # Construct the parameter values for the query
        parameters = [value for value in field_mapping.values() if value is not None]
        parameters.append(brokerage_setting_id)

        # Continue with the update query
        try:
            conn = connection_pool.getconn()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            create_table_if_not_exists(conn, "sharkcap_db_brokerage_setting")

            cur = conn.cursor()
            cur.execute(query, parameters)
            conn.commit()
            cur.close()
            return {"message": "Brokerage Updated successfully."}
        except Exception as e:
            return {"Error": f"{e}, while updating data"}
        finally:
            if conn:
                connection_pool.putconn(conn)
    else:
        return {"message": "No fields to update."}


        