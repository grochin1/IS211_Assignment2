# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 2. Python Standard Library."""

import urllib2
import csv
import datetime
import argparse
import logging, logging.config
import sys


url = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'

def downloadData(url):
    response = urllib2.urlopen(url)
    bdates = csv.DictReader(response)
    return bdates

def processData(bdates, logger):
    birthdays = {}
    for i, row in enumerate(bdates):
        try:
            dt = datetime.datetime.strptime(row['birthday'], '%d/%m/%Y')
            birthdays[int(row['id'])] = (row['name'], dt)
        except:
            print row
            logger.error('Error processing line %d for ID #%s', i, row['id'])
    return birthdays

def displayPerson(id, personData):
    while True:
        try:
            id = int(input('Please enter the ID of the person you want to know the birthday of:\n'))
        except:
            continue
        if id < 1:
            sys.exit(0)

        if id in personData:
            print('Person ID {} is {} with a birthday of {}.'.format(id, name, personData[name]))
        else:
            print('No user found with that ID')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    # setup looger
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    logger.addHandler(logging.FileHandler('errors.log', mode='w'))

    csvData = downloadData(args.url)
    personData = processData(csvData, logger)