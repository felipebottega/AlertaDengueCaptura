#!/usr/bin/env python
#coding:utf8
"""
Este script captura series de clima do servidor da Weather Underground em um
período determinado.


Copyright 2014 by Flávio Codeço Coelho
license: GPL v3
"""
import argparse
from datetime import datetime
import time

from crawlclima.wunderground.wu import capture, date_generator
from utilities.models import save, find_all


rows = find_all(schema='Municipio', table='Estacao_wu')
codes = [row['estacao_id'] for row in rows]

date = lambda d: datetime.strptime(d, "%Y-%m-%d")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--inicio", "-i", type=date, help="Data inicial de captura: yyyy-mm-dd")
parser.add_argument("--fim", "-f", type=date, help="Data final de captura: yyyy-mm-dd")
parser.add_argument("--codigo", "-c", choices=codes, metavar='ICAO', help="Codigo da estação" )
args = parser.parse_args()

station, start, end = args.codigo, args.inicio, args.fim
data = []

for date in date_generator(start, end):
    print("Fetching data from {} at {}.".format(station, date))
    data.append(capture(station, date))
    time.sleep(1)

save(data, schema='Municipio', table='Clima_wu')
