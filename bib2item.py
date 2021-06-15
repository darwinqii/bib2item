#!/usr/bin/env python

"""

"""

import inspect, os
from pathlib import Path
import re
import time

def get_bib(bibfile=None):
    """
    This function reads in the bib file, interpret all publication items and put them into a List of dictionaries that contains all details. 
    """
    dir = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) # script directory
    if not bibfile:  # if bibfile is not given
        bibfile = 'references.bib'
    with open(dir/bibfile,'r',encoding="utf-8") as file:
        # bib = bibtexparser.load(file)
        content = file.read()
    bibs = content.split('@')[1:]
    bibs_cleaned=[]
    for bib in bibs:
        bib_dict={}
        details=bib.split(',\n')  # the content in one publication bib
        bib_dict['doc_type'], bib_dict['cite_key'] = details[0].split('{')
        for detail in details[1:]: #everything after citation key
            detail = detail.split('=')
            detail_key=detail[0].replace(' ','')
            detail_value=re.match('.*',detail[1])[0] # remove the possible \n
            detail_value=re.match('\s*\{(.*)\}',detail_value)[1] # remove the { }
            bib_dict[detail_key] = detail_value
            # print(detail)
        bib_dict['author'] = bib_dict['author'].split(' and ')
        unwanted=['file', 'mendeley-groups', 'url']
        for k in unwanted:
            try:
                del bib_dict[k]
            except:
                pass
        bibs_cleaned.append(bib_dict)
    
    return bibs_cleaned
 

def format_author(authors):
    authors_new=[]
    for a in authors:
        fam_name=a.split(', ')[0]
        fam_name_str=r'\bibnamefont{'+fam_name+r'}'
        giv_name=a.split(', ')[1].split(' ')
        giv_name_str=''
        for name in giv_name:
            name= name[0]+'.'
            giv_name_str=giv_name_str+r'\bibfnamefont{'+name+r'}~'
        # print(giv_name_str)
        full_name_str = r"\bibinfo{author}{"+giv_name_str+fam_name_str+r'}'
        authors_new.append(full_name_str)
    return authors_new


def bib2item(bib):  # one item 
    # authors
    bib_str=''
    authors=format_author(bib['author'])
    if len(authors)==1:
        author_entry=authors[0] 
    else:
        author_entry=", ".join(_ for _ in authors[:-1]) + " and " + authors[-1] + ','
    # print(author_entry)

    if bib['doc_type']=='article':
        # journal
        journal_name = bib['journal']
        journal_entry = r'\bibinfo{journal}{'+journal_name+r'}'

        #volume
        volume = bib['volume']
        volume_entry= r' \textbf{\bibinfo{volume}{'+volume+r'}},'

        # page
        page=bib['pages']
        page_entry=r'\bibinfo{pages}{'+ page +r'}'

        # year
        year=bib['year']
        year_entry=r' (\bibinfo{year}{'+year+r'}).'

        # cite name year
        cite_author = bib['author'][0].split(', ')[0]
        cite_entry = r"{\citenamefont{"+cite_author+r"}("+year+r")}"

        # citation key
        cite_key=bib['cite_key']
        citer_key_entry=r'{'+cite_key+r'}'
        #### Full entry  #####
        full_entry = r'\bibitem['+cite_entry+r']'+citer_key_entry+author_entry+journal_entry+volume_entry + page_entry+ year_entry

        print(full_entry)

    
    return






def write_bibitems():  # write all bibitems to a text file
    return  

if __name__ == '__main__':
    bibs = get_bib()
    for b in bibs:
        bib2item(b)
        break
