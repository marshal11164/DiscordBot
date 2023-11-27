import mysql.connector

def connexion():
    try:
        
        conn = mysql.connector.connect(
            host='192.168.31.117',
            port=3306,
            user='pablo',
            password='Saragata1',
            db='LeagueOfLegends'
    )
        if conn.is_connected():
            
            print('Conexion Correcta')
            info_server=conn.get_server_info()
            print(info_server)
    except Exception as ex:
        print(ex)
    return conn