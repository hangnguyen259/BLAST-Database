#load big alignments
import sys
import os
from HeadersCheck import *
from model_project import *
from Bio.Blast import NCBIXML
from sqlobject import SQLObjectNotFound

if len(sys.argv) != 3:
    print('Please provide 2 xml files')
    sys.exit(1)
fileA = sys.argv[1]
fileB = sys.argv[2]

init()

def percent_id(identity,align_len):
    per_id = (identity/align_len)*100
    return per_id
def query_coverage(end,start,query_length):
    query_cov = ((end-start)/query_length)*100
    return query_cov

par_files = (fileA,fileB)
for n in par_files:
    if not os.path.isfile(n):
        print('File does not exist',n)
        sys.exit(1)
    #else:
       # print('File does not exist',n)
        #sys.exit()

for item in par_files:
    h = open(item)
    for blast_result in NCBIXML.parse(h):
        check = checking(blast_result.query) #send to HeadersCheck module
        q_accession = check[0]#query accession
        q_protein = Protein.byAccession(q_accession) #instance 
        for alignment in blast_result.alignments:
            #try:
            check_hit = checking(alignment.hit_def)
            ref_accession = check_hit[0] #subject accession
            ref_protein = Protein.byAccession(ref_accession) #map it by accession 
            for hsp in alignment.hsps: #parse high scoring pairs
                if hsp.expect <= 1e-10:
                    evalue = float(hsp.expect)
                    per_id = float(percent_id(hsp.identities,hsp.align_length))
                    bitscore = float(hsp.bits)
                    query_cov = query_coverage(hsp.query_end,hsp.query_start,blast_result.query_length)
                    a = Alignment(evalue = evalue,  bitscore = bitscore, query_cov = query_cov, per_id = per_id, q_protein = q_protein, ref_protein = ref_protein)
##            except SQLObjectNotFound:
##                print('object not find')
##                continue
    h.close()
                
                
            
