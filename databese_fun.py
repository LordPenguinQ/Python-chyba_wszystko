import sqlite3
from sqlite3 import Error

def clear_chat(connection):
    sql = '''DELETE FROM chat'''

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    return cursor.fetchall()

def remove_user(connection, nick):
    sql = '''DELETE FROM users WHERE login LIKE ?'''

    cursor = connection.cursor()
    cursor.execute(sql, nick)
    connection.commit()

    return cursor.fetchall()

def check_users_id(connection, user_id):
    sql = '''SELECT id FROM users WHERE id = ?'''

    cursor = connection.cursor()
    cursor.execute(sql, user_id)
    connection.commit()

    login = cursor.fetchone()
    return login[0] if login else None

def add_user_with_id(connection,user_id,login):
    sql = '''INSERT INTO users(id, login) VALUES(?, ?)'''

    send=(user_id,login)

    cursor = connection.cursor()
    cursor.execute(sql, send)
    connection.commit()

    return cursor.lastrowid