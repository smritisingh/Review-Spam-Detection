#-------------------------------------------------------------------------------
# Name:        DatabaseCreator.py
# Purpose:	   to create database
#
# Author:      Smriti
#
# Created:     11/05/2015
# Copyright:   (c) Smriti 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sqlite3
import os
DATABASE = "HotelReview.db"

def getHandle(databasename):
    return sqlite3.connect(databasename)
def clearHandle(conn):
    conn.close()
def CreateReviewTable(conn):
    createstring = '''CREATE TABLE  if not exists REVIEWS
                    (
                        REVIEWID INTEGER PRIMARY KEY,
                        HOTELNAME TEXT NOT NULL,
                        REVIEWTEXT TEXT,
                        POLARITY INTEGER NOT NULL,
                        SPAM BOOL NOT NULL
                    );'''
    conn.execute(createstring)
    conn.commit()
def InsertReview(conn,Reviews,polarity,IsSpam):
    HOTELNAME = Reviews['hotel']
    REVIEWTEXT = Reviews['reviewtext']
    POLARITY = polarity
    SPAM = IsSpam
    conn.execute("INSERT INTO REVIEWS ( HOTELNAME ,REVIEWTEXT ,POLARITY ,SPAM ) VALUES(?,?,?,?)" ,(HOTELNAME,REVIEWTEXT,POLARITY,SPAM,))
    conn.commit()
    return True

def addReviews(conn, folderpath, polarity, isspam):
    Polarity = polarity
    IsSpam = isspam
    for root, dirs, files in os.walk(folderpath):
        for file in files:
            Reviews = {}
            name = file.split('_')
            Reviews['hotel'] = name[1]
            f = open(os.path.join(root,file))
            text = f.read()
            Reviews['reviewtext'] = text
            InsertReview(conn,Reviews,Polarity,IsSpam)


def main():
    #DeceptiveFolderN = "./data/negative_polarity/deceptive_from_MTurk"
    #DeceptiveFolderP = "./data/positive_polarity/deceptive_from_MTurk"
    #TruthfulFolderP = "./data/positive_polarity/truthful_from_TripAdvisor"
    #TruthfulFolderN = "./data/negative_polarity/truthful_from_Web"

    DeceptiveFolderN = "C:/Users/Smriti/Desktop/After Midsem/Code/Feature Extraction/Data/negative_polarity/deceptive_from_MTurk"
    DeceptiveFolderP = "C:/Users/Smriti/Desktop/After Midsem/Code/Feature Extraction/Data/positive_polarity/deceptive_from_MTurk"
    TruthfulFolderP = "C:/Users/Smriti/Desktop/After Midsem/Code/Feature Extraction/Data/positive_polarity/truthful_from_TripAdvisor"
    TruthfulFolderN = "C:/Users/Smriti/Desktop/After Midsem/Code/Feature Extraction/Data/negative_polarity/truthful_from_Web"

    conn = getHandle(DATABASE)
    CreateReviewTable(conn)

    addReviews(conn, DeceptiveFolderN, -1,True)
    addReviews(conn, DeceptiveFolderP,  1,True)
    addReviews(conn, TruthfulFolderN , -1,False)
    addReviews(conn, TruthfulFolderP ,  1,False)

    clearHandle(conn)

if __name__=="__main__":
    main()
