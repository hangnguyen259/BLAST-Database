#retrieve blast from relational database

import sys
from model_project import *
from sqlobject import SQLObjectNotFound

if len(sys.argv) != 3:
    print('Please provide 2 accessions')
    sys.exit(1)
    
init()

accession1 = sys.argv[1]
accession2 = sys.argv[2]

accs = [(accession1,accession2),(accession2,accession1)]

for query,ref in accs:
    ###check if accession in the table
    try:
        query_pro = Protein.byAccession(query)
    except SQLObjectNotFound:
        print('Accession not in table',query)
        sys.exit(1)
    try:
        ref_pro = Protein.byAccession(ref)
    except SQLObjectNotFound:
        print('Accession not in table',ref)
        sys.exit(1)
    #list comprehensive    
    available_alignments = [a for a in query_pro.q_alignments if a.ref_protein.id == ref_pro.id]
    if available_alignments:
        for a in available_alignments:
            print('********Alignment**********','\n', 'Query protein:',query,'and reference protein:',ref,'','\n',
                  'e-value:',a.evalue,'\n','bit score:',a.bitscore,'\n',
                 'query coverage percent:',a.query_cov,'\n','percent identity:', a.per_id)
    else:
        print('Alignments are not available for this pair because of insignificant stats')
