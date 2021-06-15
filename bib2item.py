#!/usr/bin/env python

"""

"""

import inspect, os
from pathlib import Path
import re
import time

def bib2item(bibfile=None):
    """
    This function reads in the bib file, interpret all publication items and put them into a List of dictionaries that contains all details. 
    """

    dir = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) # script directory
    if not bibfile:  # if bibfile is not given
        bibfile = 'references.bib'
    with open(dir/bibfile,'r',encoding="utf-8") as file:
        # bib = bibtexparser.load(file)
        content = file.read()
    # content  = content.replace('\n', '')
    # content = content.replace('@', '\n @' )  # Add a \n per item for easier pattern matching
    # item_pattern=re.compile('@\w+\{.*\}')
    # # item_pattern=re.compile('@(?P<citekey>\w+)\{()')
    # items = re.findall(item_pattern, content)
    # # item_pattern=re.compile('@(\w+)',re.MULTILINE)
    items = content.split('@')[1:]
    items_cleaned=[]
    for item in items:
        item_dict={}
        details=item.split(',\n')  # the content in one publication item
        item_dict['doc_type'], item_dict['cite_key'] = details[0].split('{')
        for detail in details[1:]: #everything after citation key
            detail = detail.split('=')
            detail_key=detail[0].replace(' ','')
            detail_value=re.match('.*',detail[1])[0] # remove the possible \n
            detail_value=re.match('\s*\{(.*)\}',detail_value)[1] # remove the { }
            item_dict[detail_key] = detail_value
            # print(detail)
        items_cleaned.append(item_dict)
    

    with open(dir/('bibitem.txt'),'w',encoding="utf-8") as file:
        content_new = re.sub(pattern='url = {.*},\n',repl='',string=content)

        file.write(content_new)
    time.sleep(3)
    return         
 
 

if __name__ == '__main__':
    # Set the name of the output file.
    # outfilestem = 'proteinScienceBibItems'
    # home = '/Users/blaine/'
    # Set the name of the input file.   
    bib2item()
