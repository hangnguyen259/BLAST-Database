#format checking

def checking(query):
    if query[0] == 'g':
        return GI(query)
    elif query[0] in ('Y', 'Q'):
        return SGD(query)
    elif query[0] in ('s', 't'):
        return Uniprot(query)
    return None

def GI(chars):
    ls = chars.split('|')
    accession = ls[3]
    sl_desc = ls[4].split('[')
    desc = sl_desc[0]
    species = sl_desc[-1].rstrip("]")
    return accession,desc,species
def SGD(chars):
    ls = chars.split()
    accession = ls[0]
    sl_predesc = chars.split(';')
    sl_desc= sl_predesc[0].split(',')
    desc= sl_desc[-1].lstrip(' "')
    species = 'Saccharomyces cerevisiae'
    return accession,desc,species
def Unipro(chars):
    ls = chars.split('|')
    accession = ls[1]
    desc_spl = ls[2].split(' OS=')
    desc = desc_spl[0]
    sps = desc_spl[1].split(' OX=')
    species = sps[0]
    return accession,desc,species
