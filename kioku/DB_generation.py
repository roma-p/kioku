import sqlite3
import os
import logging

log = logging.getLogger()


def generateDB(dbPath):

    dbName = dbPath.split('/')[-1]
    dirPath = dbPath.split(dbName)[0]

    if not os.path.exists(dirPath):
        log.error('path not found :' + dirPath)
        return False
    elif os.path.exists(dbPath):
        log.error('Database already exists :' + dbPath)
        return False

    log.info('generating new empty kioku db.')
    kioku = sqlite3.connect(dbPath)
    cursor = kioku.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocab(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        word TEXT,
        prononciation TEXT,
        meaning TEXT,
        exemple TEXT,
        categorie TEXT,
        tag TEXT
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorie(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT)
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT)
        """)

    kioku.commit()
    kioku.close()

    log.info('generation complete :' + dbPath)

    return True
