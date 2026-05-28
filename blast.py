#blast
import sys
from Bio.Blast.Applications import NcbiblastpCommandline
import os


if len(sys.argv) != 4:
    print('Please provide a pathway to database, and 2 file names')
    sys.exit(1)
    
pathway = sys.argv[1]
file_A = sys.argv[2]
file_B = sys.argv[3]

checkzip = (file_A,file_B)
for item in checkzip:
    if item.endswith('.gz'): 
        print('Please decompress files and make database')
        sys.exit(1)

blast = [(file_A,file_B),(file_B,file_A)]


for query,db in blast:
    query_file = os.path.join(pathway,query+'.fasta')
    db_file = os.path.join(pathway,db)
    if not os.path.isfile(query_file):
        print('File does not exist',query)
        sys.exit(1)
    db_files = [db_file+x for x in ('.phr','.psq','.pin')]
    for n in db_files:
        if not os.path.exists(n):
            print('Essential db files do not exist',n)
            sys.exit(1)
    blast_prog   = '/usr/local/bin/blastp'
    cmdline = NcbiblastpCommandline(cmd=blast_prog,
                                query=query_file,
                                db=db_file,
                                outfmt=5,
                                out=f"{query}.xml")
    #execute the command
    stdout, stderr = cmdline()






