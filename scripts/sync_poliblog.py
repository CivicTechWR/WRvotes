#!/usr/bin/env python3
"""
Convert Bob Jonkman's candidate listings to a format we can consume

Paul "Worthless" Nijjar, 2022-08-22
"""

import csv, re
import unicodedata
import datetime
from html import unescape

NO_WARD="N/A"

mergedict = {}

# ===== FUNCTIONS ======

def slugify(value):
    """ Normalizes strings. From
    https://stackoverflow.com/questions/5574042/string-slugification-in-python

    Note that this CAN cause collisions if you are using this as a hash
    key (which is what I am doing...)!
    """
    slug = unicodedata.normalize('NFKD', value)
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    slug = slug.lower()

    return slug


# ---------------
def fix_phone(phone_no):
    """ Format phone so that North American humans will recognise
    them
    """

    item = take_first(phone_no)
    if item == "": 
        return ""

    # The .* can match extensions
    simple_phone = re.compile(r'(\d\d\d-\d\d\d-\d\d\d\d.*)$')
    match = simple_phone.search(item)

    if match:
        return match.group()
    else:
        print("Oh no! No phone number found in \"{}\"".format(phone_no))

    return ""



# -----------------
def take_first(item):
    """ Sometimes there are multiple entries separated by spaces.
    Only take the first one.
    """

    entries = item.split(" ")
    for entry in entries:
        if entry != '':
            return entry

    # Empty string
    return ''


# -----------------
def clean_entry(item):
    """ Process an entry so it meets our formatting (one entry, UTF)
    """

    return unescape(take_first(item))

# ------------------
def parse_ward(office):
    """ Given an office, produce the ward number if it exists, 
    and the value of the NO_WARD constant otherwise.
    """

    ward_regexp = re.compile(r'Councillor Ward\s+(\d+)')
    m = ward_regexp.match(office)

    if m:
        return m.groups()[0]
    else:
        return NO_WARD



# -------------------
def parse_unique_position(row):
    """ Given a row with the office and municipality, produce the
    unique ID position string WRV uses.
    """

    office = row['Office']
    municipality = row['Municipality']
    

    if office == "Regional Chair":
        return "Regional-Chair"
    elif office == "Regional Councillor":
        return "Regional-{}".format(municipality)

    elif office == "Trustee Viamonde (French Public)":
        return "SchoolBoard-Public-French"
    elif office == "Trustee catholique MonAvenir (French Separate)":
        return "SchoolBoard-Catholic-French"

    elif office == "Mayor" and municipality == "North Dumfries":
        return "NorthDumfries-Mayor"
    elif office == "Mayor":
        return "{}-Mayor".format(municipality)

    elif office == "Trustee WCDSB - Wilmot":
        return "SchoolBoard-Catholic-English-Kitchener-Wilmot"
    elif office == "Trustee WCDSB - North Dumfries":
        return "SchoolBoard-Catholic-English-Cambridge-NorthDumfries"
    elif office == "Trustee WCDSB - Wellesley - Woolwich":
        return "SchoolBoard-Catholic-English-Waterloo-Wellesley-Woolwich"

    elif office == "Trustee WRDSB" and municipality == "Kitchener":
        return "SchoolBoard-Public-English-Kitchener"
    elif office == "Trustee WRDSB - North Dumfries":
        return "SchoolBoard-Public-English-Cambridge-NorthDumfries"
    elif office == "Trustee WRDSB - Wellesley":
        return "SchoolBoard-Public-English-Woolwich-Wellesley"
    elif office == "Trustee WRDSB - Wilmot":
        return "SchoolBoard-Public-English-Waterloo-Wilmot"
    

    ward = parse_ward(office)

    if ward != NO_WARD:
        if municipality == "North Dumfries":
            return "NorthDumfries-Ward-{}".format(ward.zfill(2))
        else:
            return "{}-Ward-{}".format(municipality,ward.zfill(2))


    
    print("Oh no! Unable to parse position tag! "
        "name: {}, office: {}, municipality: {}".format(
           row['Name'],
           office,
           municipality
           ))


    return "FAILED_PARSE"


# ===== MAIN =======

def sync_poliblog(srcfile, overrides, mergefile):
    """ Merge the srcfile and overrides into the mergefile.
    """

    with open(srcfile, encoding='utf-8-sig') as src_csv:
        # Skip one line
        src_csv.readline()

        src = csv.DictReader(src_csv)
        for row in src:
            fullname = unescape(row['Name'])
            position_tag = parse_unique_position(row)
            row_key = "{}-{}".format(
                  position_tag,
                  slugify(fullname),
                  )

            if row_key in mergedict:
                print("Uh oh! Key \"{}\" is already in dict! "
                  "conflict?".format(row_key))
            else:
                mergedict[row_key] = {}
                mergedict[row_key]['Last_Name'] = fullname
                mergedict[row_key]['Nominated_Office'] = unescape(row['Office'])
                mergedict[row_key]['Phone'] = fix_phone(row['Phone'])
                mergedict[row_key]['Twitter'] = clean_entry(row['Twitter'])
                mergedict[row_key]['Facebook'] = clean_entry(row['Facebook'])
                mergedict[row_key]['LinkedIn'] = clean_entry(row['LinkedIn'])
                mergedict[row_key]['Instagram'] = clean_entry(row['Instagram'])
                mergedict[row_key]['Website'] = clean_entry(row['Website'])
                mergedict[row_key]['Email'] = clean_entry(row['Email'])
                mergedict[row_key]['PositionUniqueName'] = position_tag
                mergedict[row_key]['Ward'] = parse_ward(row['Office'])
                mergedict[row_key]['UniqueID'] = row_key
                mergedict[row_key]['IDReversed'] = "{}-{}".format(
                  slugify(fullname),
                  position_tag,
                  )
                if (clean_entry(row['Withdrawn'].upper()) == "TRUE"):
                    mergedict[row_key]['Withdrawn'] = "Y"


    with open(overrides, encoding='utf-8-sig') as override_csv:
        override_rows = csv.DictReader(override_csv)
        
        for row in override_rows:

            row_key = row['UniqueID']
            for col, val in row.items():
                if val == "DELETE":
                    mergedict[row_key][col] = None
                elif val != "":
                    mergedict[row_key][col] = val



    # Try to produce this in a reasonable order?
    # Sigh. Why can't people use ISO dates?
    mergekeys = sorted(mergedict, 
      key=lambda x: (
                     mergedict[x]['Last_Name'],
                     mergedict[x]['Given_Names'],
                    ))

    #print(mergekeys)

    poli_fieldnames = [
      'Name',
      'Office',
      'Municipality',
      'Elect',
      'Notes',
      'Website',
      'Email',
      'Phone',
      'Address',
      'ImageURL',
      'Incumbent',
      'Unregistered',
      'Withdrawn',
      'Elected',
      'Twitter',
      'Facebook',
      'LinkedIn',
      'YouTube',
      'Instagram',
      'Pintrest',
      'Flickr',
      'Tumblr',
      'Calendar',
      'MySpace',
      'TikTok',
      'Reddit',
      'MunicipalityURL',
      'MunicipalityLogo',
    ]

    fieldnames = [
      'Last_Name',
      'Given_Names',
      #'Date_Filed',        # die? 
      'PositionUniqueName',
      'Nominated_Office',  # die? - no. Used in candidate card.
      #'Municipality',      # die?
      'Ward',              # die? - no. Used in candidate card. 
      'Phone',
      'Email',
      'Website',
      'Twitter',
      'Facebook',
      'LinkedIn',           # new
      'Instagram',          # new
      'Withdrawn',
      'Votes',
      'Winner',
      'Total_Votes',
      'Percentage',
      'ImageTitle',
      'UniqueID',           # new
      'IDReversed',
     ] 

    with open(mergefile, 'w', newline='') as out_csv:
        writer = csv.DictWriter(
          out_csv, 
          fieldnames=fieldnames,
          quoting=csv.QUOTE_MINIMAL,
          extrasaction='ignore',
          )


        writer.writeheader()

        for k in mergekeys:
            writer.writerow(mergedict[k])
        

#print(mergedict)


