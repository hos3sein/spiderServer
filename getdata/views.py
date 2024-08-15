from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pandas as pa
import csv
import json
def index(request):
    return HttpResponse("test pass!!!!!!!!")


def no(request):
    return HttpResponse("no route test pass!!!!!!")


def getAllData(request):
    data = dataReader()
    return HttpResponse(data)


def dataReader():
    csvFile = open('../../dataBot/data.csv' , 'r')
    jsonFiel = open('dataFile.json' , 'w')
    logoFile = open('../../dataBot/Rdata.json' , 'r')
    logos =  json.load(logoFile)
    fieldsName = ( "" ,"name" , "price" , "prcent_change_1H" , "percent_change_24H")
    readerData = csv.DictReader(csvFile , fieldsName)
    new_data = []
    for row in readerData:
        # print(row)
        # print(row['name'])
        if (row['name'] != 'name'):
            logo = '';
            if (row['name'] in logos):
                logo = logos[row['name']]
                # print(logo)
                row['logo'] = logo
            json.dump(row, jsonFiel)
            jsonFiel.write('\n')
            new_data.append(row)
    return (new_data)
    





    # data = pa.read_csv('../../dataBot/data.csv')
    # print(data)
    # return(data)    