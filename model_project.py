#model project
import os.path, sys
from sqlobject import *

#dbfile = 'alignments.db3'
dbfile = 'big_alignments.db3'
def init(new=False):
    conn_str = os.path.abspath(dbfile)
    conn_str = 'sqlite:'+ conn_str
    sqlhub.processConnection = connectionForURI(conn_str)
    if new:
        Protein.dropTable(ifExists=True)
        Alignment.dropTable(ifExists=True)
        Protein.createTable()
        Alignment.createTable()

class Protein(SQLObject):
    accession = StringCol(unique= True, alternateID=True)
    desc = StringCol()
    species = StringCol()
    q_alignments = MultipleJoin('Alignment',joinColumn = 'q_protein_id')
    ref_alignments = MultipleJoin('Alignment',joinColumn = 'ref_protein_id')
    
    
class Alignment(SQLObject):
    q_protein = ForeignKey('Protein')
    ref_protein = ForeignKey('Protein')
    evalue = FloatCol()
    bitscore = FloatCol()
    query_cov = FloatCol()
    per_id = FloatCol()
    
