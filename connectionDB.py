import psycopg2
from dotenv import load_dotenv
import os

class Database: 

    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    @classmethod
    def connection(cls):
        try:
            conn = psycopg2.connect(
                user=cls.DB_USER,
                password=cls.DB_PASSWORD,
                host=cls.DB_HOST,
                port=cls.DB_PORT,
                dbname=cls.DB_NAME
            )
            return conn
        except Exception as e:
            print(f"Failed to connect: {e}")
            return None  

    @classmethod
    def addRecord(cls, nome, litri):
        conn = cls.connection()
        
        if conn is None:
            print("Connessione al database fallita.")
            return  

        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO records(nome, quantity) VALUES (%s, %s)", (nome, litri))
            conn.commit()
        except Exception as e:
            print("Errore:", e)
        finally:
            conn.close()

    @classmethod
    def deleteRecord(cls, record_id):
        conn = cls.connection()
        
        if conn is None:
            print("Connessione al database fallita.")
            return  
        
        cur = conn.cursor()

        try: 
            cur.execute("""DELETE FROM records WHERE id_rec = %s""", (record_id,))
            conn.commit()
        except Exception as e:
            print("Errore:", e)
        finally:
            conn.close()



if __name__ == "__main__": 

    Database.connection()
    
