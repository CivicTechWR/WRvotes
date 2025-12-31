#!/usr/bin/env python3

# Generate .docx/.xlsx/.pdf versions of candidate lists
# Paul "Worthless" Nijjar, 2025-12-30

import csv
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
import os, sys
from datetime import datetime


DATADIR="../docs/_data"
TEST_POSITION='SchoolBoard-Public-English-Kitchener'
TEST_WARD='Kitchener-Ward-09'
OUTDIR="../docs/worksheets"

# I am not happy with reading and appending into a giant list, but
# whatever. The numbers are small enough that inefficiencies should
# not matter. 

# Pandas would probably be better but I can't use NumPy on this
# laptop without yak-shaving. 


# ---- HELPER FUNCTIONS

# From: https://stackoverflow.com/questions/37757203/making-cells-bold-in-a-table-using-python-docx
def make_rows_bold(*rows):
    for row in rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True



# Doesn't work?
def make_rows_vertically_centred(*rows):
    for row in rows:
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER



# --- READ DATA 



# Ugh I hate nested structures
pos_data = {}

"""
  'desc' => '',
  'candidates' => [],
  'num_to_elect' => 1,
  'ward' => '',
  'acclaimed' => False,
"""


static_text = {
  'intro': "Use this handy sheet to figure out the candidates"
      " you want to vote for. ",
  'datestamp': "Worksheet generated on {}".format(
        datetime.now().strftime("%A, %B %e, %Y, %l:%M%P")
        ),
}
 


with open (os.path.join(DATADIR,"internal/position-tags.csv")) as r:
    pos_csv = csv.DictReader(r)

    for row in pos_csv:
        pos_name = row['PositionUniqueName']
        pos_data[pos_name] = {}
        pos_data[pos_name]['desc'] = row['PositionDesc']
        pos_data[pos_name]['candidates'] = []
        pos_data[pos_name]['num_to_elect'] = int(row['NumberToElect'])
        pos_data[pos_name]['ward_municipality'] = row['WardMunicipality']


with open(os.path.join(DATADIR,"sync/nominees.csv")) as r:
    nom_csv = csv.DictReader(r)

    for row in nom_csv:
        pos_data[row['PositionUniqueName']]['candidates'].append(row)

municipality_map = []
with open (os.path.join(DATADIR,"internal/municipality-map.csv")) as r:
    mun_csv = csv.DictReader(r)

    for row in mun_csv:
        municipality_map.append(row)


# Need to sort nominees by last name? 
for pos in pos_data:
  pos_data[pos]['candidates'].sort(
      key = lambda x: "{},{}".format(x['Last_Name'],x['Given_Names'])
      )

  pos_data[pos]['num_candidates'] = len(pos_data[pos]['candidates'])
  pos_data[pos]['acclaimed'] = (
      pos_data[pos]['num_candidates'] <= pos_data[pos]['num_to_elect']
      )
      



# ---- GEN DOCX


for ward in pos_data:
    if pos_data[ward]['ward_municipality'] == 'N/A':
        continue

    races = "NOT-FOUND"

    for m in municipality_map:
        if m['Name'] == pos_data[ward]['ward_municipality']:
            races = m['Races']
            break
      
    if races == 'NOT-FOUND':
        raise NameError

    d = Document()

    d.add_heading("Municipal Election Candidate Sheet", 0)
    d.add_paragraph(static_text['datestamp'])
    d.add_paragraph(static_text['intro'])

    race_list = races.split(",")

    for r in race_list:
        if r == '_SELF':
            r = ward

        d.add_heading("{}".format( pos_data[r]['desc']))

        elected_text = "{} to be elected".format(
            pos_data[r]['num_to_elect']
            )
        if pos_data[r]['acclaimed']:
            elected_text = "{} : ACCLAIMED".format(elected_text)

        d.add_paragraph(elected_text)

        t = d.add_table(rows=1, cols=2)
        header_cells = t.rows[0].cells
        header_cells[0].text = "Candidate Name"
        header_cells[1].text = "Notes"
        make_rows_vertically_centred(t.rows[0])
        make_rows_bold(t.rows[0])

        for nom in pos_data[r]['candidates']:
            row = t.add_row()
            row_cells = row.cells
            row_cells[0].text = "{} {}".format(
                nom['Given_Names'],
                nom['Last_Name'],
                )
            row_cells[1].text = ""
            make_rows_vertically_centred(row)

    d.save(os.path.join(OUTDIR,"docx","{}.docx".format(ward)))



# ---- BAD TESTING

"""
print(pos_data[TEST_POSITION])

for nom in pos_data[TEST_POSITION]['candidates']:
    print("{} {}".format(nom['Given_Names'],nom['Last_Name']))
"""


