from main import mongoConnect, formatDate
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from multiprocessing.dummy import Pool as ThreadPool
from classify import predictSingle
import re
import sys
from PIL import Image
from datetime import datetime
import requests

def moveArticles():
    currentCollection = mongoConnect()
    oldColl = mongoConnect("Old")
    data = currentCollection.find()
    oldColl.insert_many(data)

def deleteOld():
    oldColl = mongoConnect("Old")
    oldColl.remove()

if __name__ == "__main__":
    n = int(input("choose \n 1.delete all old \n 2.move to old"))
    if(n == 1):
        deleteOld()
    elif(n == 2):
        moveArticles()