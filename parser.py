# -*- coding: utf-8 -*-
import json
import re
import sys

import six
import unicodecsv as csv
import xlrd

reload(sys)
sys.setdefaultencoding('utf8')

party_list = ['IND', 'REP', 'DEM', 'NA', 'NP', 'CON', 'WIG', 'LIB']

headers = ["county","ward","office","district","total votes","party","candidate","votes"]

def detect_headers(sheet):
    for i in range(3,12):
        row = sheet.row_values(i)
        if row[2].strip() == 'Total Votes Cast':
            parties = [x for x in row[3:] if x != None]
            candidates = [x for x in sheet.row_values(i+1)[3:] if x!= None]
            start_row = i+2
            return candidates, parties, start_row

def get_election_result(filename,output):
  print "Processing %s" % output 
  myfile = open(output, 'wb')
  wr = csv.writer(myfile)
  wr.writerow(headers)
  print "Opening %s" % filename
  results = process_results(filename)
  for i,result in enumerate(results):
    for x,row in enumerate(result):
      row = clean_row(row)
      if "Office Totals:" not in row:
        wr.writerow(row)

def clean_county(item):
  return clean_string(item)

def clean_ward(item):
  return clean_string(item)

def clean_office(item):
  return clean_string(item)

def clean_district(item):
  item = clean_string(item)
  if (re.match(r"^[0-9,]*$",item)):
    return to_int(item)
  else:
    return None

def clean_total(item):
  return to_int(item)

def clean_party(item):
  return item

def clean_votes(item):
  return to_int(item)

def clean_candidate(item):
  return clean_string(item)

def clean_row(row):
  row[0] = clean_county(row[0])
  row[1] = clean_ward(row[1])
  row[2] = clean_office(row[2])
  row[3] = clean_district(row[3])
  row[4] = clean_total(row[4])
  row[5] = clean_party(row[5])
  row[6] = clean_candidate(row[6])
  row[7] = clean_votes(row[7])
  return row

def to_int(item):
  if (item == int(0.0)):
    return 0
  elif (item):
    try:
      int(item)
      return int(item)
    except ValueError:
      item = item.replace(",","")
      return int(item)
  else:
    return 0

def clean_string(item):
  item = item.strip()
  item = item.replace("\n"," ")
  item = item.title()
  return item

def process_results(filename):
    xlsfile = xlrd.open_workbook(filename)
    offices = get_offices(xlsfile)
    results = []
    if offices:
        for i, office in enumerate(offices):
            sheet = xlsfile.sheet_by_index(i + 1)
            results.append(parse_sheet(sheet, office))
    else:
        # no offices found, assume first sheet is not a title sheet
        sheet = xlsfile.sheet_by_index(0)
        for office in offices_without_title_sheet:
            # Look for an office in first column, search first 12 rows
            if office in sheet.col_values(colx=0, start_rowx=0, end_rowx=12):
                results.append(parse_without_title_sheet(sheet, office))
                break
    return results

def parse_sheet(sheet, office):
    output = []
    candidates, parties, start_row = detect_headers(sheet)
    if 'DISTRICT' in office.upper():
        # This '–' is a different character than this '-'
        office = office.replace('–','-')
        split = office.split('-')
        # Office string comes in formats:
        #  * STATE SENATE - DISTRICT 1 - REPUBLICAN
        #  * STATE SENATE   DISTRICT 1 - REPUBLICAN
        if (len(split) == 2):
            try:
                office, district = office.split('-')
            except:
                office, district = office.split(u'-')
        # Assumes STATE SENATE - DISTRICT 1 - REPUBLICAN format
        else:
          try:
              office, district, party  = office.split('-')
          except:
              office, party, district = office.split(u'-')
        district = district.replace('DISTRICT ','')
    else:
        district = office
    if len(office.split(",")) > 1:
      party = district
      district = office.split(",")[1]
      office = office.split(",")[0]
    county = ''
    for i in range(start_row, sheet.nrows):
        results = sheet.row_values(i)
        if "Totals" in results[1]:
            continue
        if results[0].strip() != '':
            county = results[0].strip()
        elif len(district.split(" COUNTY ")) > 1:
          county = office.split(" COUNTY ")[0]
        ward = results[1].strip()
        if isinstance(results[2], six.string_types):
          results[2] = results[2].replace(",","")
        total_votes = int(results[2]) if results[2] else results[2]
        # Some columns are randomly empty.
        candidate_votes = results[3:]
        for index, candidate in enumerate(candidates):
            if (candidate == None or candidate == ''):
                continue
            else:
                party = parties[index]
                output.append([county, ward, office, district, total_votes, party, candidate, candidate_votes[index]])
    return output

def get_offices(xlsfile):
    sheet = xlsfile.sheet_by_index(0)
    offices = sheet.col_values(1)[1:]     # skip first row
    if offices[0] == '':    # if first office empty,
        offices = []            # assume not a title sheet, no offices
    # simulate bug in 2016-02-14 version that skips last row if > 1 rows
    offices = offices[:-1] if len(offices) > 1 else offices
    return offices

filename = sys.argv[1]
output  = sys.argv[2]

get_election_result(filename, output)

