import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            "id" SERIAL PRIMARY KEY,
            "first_name" VARCHAR(40) NOT NULL,
            "second_name" VARCHAR(40) NOT NULL,
            "email" VARCHAR(40) NOT NULL UNIQUE,
            "phone" VARCHAR(20) UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS additional_phone_numbers(
            "id" SERIAL PRIMARY KEY,
            "additional_phone" VARCHAR(20) UNIQUE,
            "fk_clients_id" INTEGER REFERENCES clients("id")
        );
        """)
        conn.commit()
    conn.close()

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO clients("first_name", "last_name", "email")
        VALUES("first_name"=%s, "last_name"=%s, "email"=%s);
        """, (first_name, last_name, email))
        if phone is not None:
            cur.execute("""
            INSERT INTO clients("phone")
            VALUES("phone"=%s)
            """, (phone))
        conn.commit()
        
    conn.close()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO additional_phone_numbers("number", "fk_clients_id")
        VALUES("additional_phone"=%s, "fk_clients_id"=%s);
        """, (phone, client_id))
        conn.commit()
    conn.close()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
            UPDATE clients SET "first_name"=%s 
            WHERE id=%s;
            """, (first_name, client_id))
        if last_name is not None:
            cur.execute("""
            UPDATE clients SET "last_name"=%s 
            WHERE id=%s;
            """, (last_name, client_id))
        if email is not None:
            cur.execute("""
            UPDATE clients SET "email"=%s 
            WHERE id=%s;
            """, (email, client_id))
        if phones is not None:
            if isinstance(phones, list) or isinstance(phones, tuple):
                for i in range(0, len(phones)):
                    if i == 0:
                        cur.execute("""
                        UPDATE clients SET "phone"=%s 
                        WHERE id=%s;
                        """, (phones[i], client_id))
                    else:
                        cur.execute("""
                        UPDATE additional_phone_numbers 
                        SET "additional_phone"=%s 
                        WHERE id=%s;
                        """, (phones[i], client_id))
            else:
                cur.execute("""
                UPDATE clients 
                SET "phone"=%s 
                WHERE id=%s;
                """, (phones, client_id))
            conn.commit()
    conn.close()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM additional_phone_numbers 
        WHERE "fk_clients_id"=%s and "additional_phone"=%s;
        """, (client_id, phone))
        conn.commit()
    conn.close()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM clients WHERE id=%s;
        """, (client_id))
        conn.commit()
    conn.close()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor as cur:
        if first_name is not None:
            cur.execute("""
            SELECT * FROM clients c
            LEFT OUTER JOIN additional_phone_numbers apn on c.id=apn.fk_clients_id
            WHERE first_name=%s
            """, (first_name))
        elif last_name is not None:
            cur.execute("""
            SELECT * FROM clients c
            LEFT OUTER JOIN additional_phone_numbers apn on c.id=apn.fk_clients_id
            WHERE last_name=%s
            """, (last_name))
        elif email is not None:
            cur.execute("""
            SELECT * FROM clients c
            LEFT OUTER JOIN additional_phone_numbers apn on c.id=apn.fk_clients_id
            WHERE email=%s
            """, (email))      
        elif phone is not None:
            cur.execute("""
            SELECT * FROM clients c
            LEFT OUTER JOIN additional_phone_numbers apn on c.id=apn.fk_clients_id
            WHERE phone=%s
            """, (first_name))
        conn.commit()
    conn.close()

with psycopg2.connect(database="clients_db", user="postgres", password="DavidLane88.") as conn:
    create_db(conn)
    add_client(conn, 'Alex', 'Spencer', 'a.spen@gmail.com', '89335467744')
    add_phone(conn, 1, '87884357668')
    change_client(conn=conn, client_id=1, first_name='Alexey')
    delete_phone(conn, 1, '87884357668')
    delete_client(conn, 1)
    find_client(conn=conn, last_name='Spencer')
conn.close()