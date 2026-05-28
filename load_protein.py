import sys
import os
from HeadersCheck import *
from Bio.Blast import NCBIXML
from model_project import *
from sqlobject import SQLObjectNotFound

if len(sys.argv) != 3:
    print('Please provide 2 xml files')
    sys.exit(1)
    
filename = sys.argv[1]
filename2 = sys.argv[2]
init(new=True)


files_parsing = (filename, filename2)
for n in files_parsing: #check if file exist
    if not os.path.isfile(n):
        print('File does not exist',n)
        sys.exit(1)
    #else:
        #print('File does not exist',n)
        #sys.exit(1)
for item in files_parsing:
    result_handle = open(item)
    for blast_record in NCBIXML.parse(result_handle):
        check = checking(blast_record.query) #check query header
        try:
            p = Protein.byAccession(check[0]) #check if accession exists
        except SQLObjectNotFound:
            p = Protein(accession=check[0], desc=check[1], species=check[2]) #add to database if not exist.
        for alignment in blast_record.alignments: 
            checkhit = checking(alignment.hit_def) #check hit header
            try:
                p = Protein.byAccession(checkhit[0])
            except SQLObjectNotFound:
                p = Protein(accession=checkhit[0],desc=checkhit[1],species=checkhit[2])
                                           
    result_handle.close()


