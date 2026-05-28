#orthologous
#import sqlite3
import sys
from model_project import *
init()

bh = {}
#query coverage and percent identity threshold for good alignmenst
cov = 80
perid = 40
proteinlst = Protein.select()
for p in proteinlst:
    bit= 0 #initial bitscore
    e =1 #initial e-value
    pro_id = p.id #get id in protein table
    for hit in Alignment.selectBy(q_protein=pro_id): #select query protein ids from alignment table
        if cov < hit.query_cov and perid < hit.per_id: 
            if bit < hit.bitscore and hit.evalue < e:
                bh[pro_id] = hit.ref_protein.id #make current query id key and reference id value
                bit = hit.bitscore #set scores to the current highest
                e = hit.evalue
#print(bh)

# Find mutually best hits
seen = set()
mbh = []
for a, b in bh.items():
    if b in bh and bh[b] == a: #check for reciprocal key-value pair
        pairs= tuple(sorted((a,b))) #sorted to make sure the reciprocal key-value pair is the same pair order
        if pairs not in seen: 
            mbh.append(pairs) 
            seen.add(pairs)
            
#print out alignments info
with open("mbh_output.txt", "w") as f:
    for item in mbh:
        accessionA = Protein.get(item[0])
        accessionB = Protein.get(item[1])
        print('****Mutually Best Hits Pairs******',file=f)
        print(accessionA.species,accessionA.accession,accessionA.desc,file=f) #speciesA
        for n in accessionA.q_alignments:
            if n.ref_proteinID == accessionB.id:
                print('E-value',n.evalue,'\n','Bitscore',n.bitscore,'\n','Query Coverage',n.query_cov,'\n','Percent Identity',n.per_id,file=f)
        print(accessionB.species, accessionB.accession,accessionB.desc,file=f) #speciesB
        for n in accessionB.q_alignments:
            if n.ref_proteinID == accessionA.id:
                print('E-value',n.evalue,'\n','Bitscore',n.bitscore,'\n','Query Coverage',n.query_cov,'\n','Percent Identity',n.per_id,file=f)
        print("\n", file=f)
print(len(mbh))

