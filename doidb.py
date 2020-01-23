#!/usr/bin/env python3

"""
Usage:
    doidb JSON list
    doidb JSON get  DOI
    doidb JSON set  DOI
    doidb JSON del  DOI

"""

from docopt import docopt
import json
import requests


def failwith(message):
    print(message)
    raise SystemExit


def data_of_file(filename):
    """Reads the JSON file and returns the corresponding dictionary"""
    try:
      with open(filename,'r') as f:
        data = json.load(f)
    except FileNotFoundError:
      data = {}
      with open(filename,'w') as f:
        json.dump(data,f)
    return data



def abbreviation_of_journal(journal):
    """
    Returns the string of the abbreviation of a Journal.
    """

    j = journal.upper()
    url = "https://images.webofknowledge.com/images/help/WOS/%s_abrvjt.html"%(j[0])
       
    text = requests.get(url).text.splitlines()
    found = False
    for line in text:
       if found:
         r = line.split('\t',1)[1]
         return r
       elif line.find(j) >= 0:
         found = True
         print(line)

    return None


def doi2bib(doi):
    """
    Returns a bibTeX string of metadata for a given DOI.
    """

    url = "http://dx.doi.org/" + doi
    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers = headers)

    return r.text




def run_list(filename):
    """doidb JSON list"""

    data = data_of_file(filename)
    for key in data:
      print(key)


def run_get(filename,doi):
    """doidb JSON get DOI"""

    data = data_of_file(filename)
    if doi not in data:
      failwith("%s not in %s"%(doi, filename))
    
    print(data[doi])


def run_del(filename,doi):
    """doidb JSON del DOI"""

    data = data_of_file(filename)

    if doi not in data:
      failwith("%s not in %s"%(doi, filename))

    del data[doi]

    with open(filename,'w') as f:
      json.dump(data,f)



def run_set(filename,doi):
    """doidb JSON get DOI"""

    data = data_of_file(filename)

    text = doi2bib(doi)
    print(text)

    def valid(text):
       result = text.strip() is not ""
       result = result and text.find("DOI Not Found") == -1
       return result

    if valid(text):
        data[doi] = text


    with open(filename,'w') as f:
      json.dump(data,f)





def main(arguments):
    filename = arguments["JSON"]
    doi = arguments["DOI"]
    if doi is None: doi = ""

    if doi.startswith("http://dx.doi.org/"):
      doi = doi.replace("http://dx.doi.org/","")

    if (arguments["list"]):
       run_list(filename)

    elif (arguments["get"]):
       run_get(filename,doi)

    elif (arguments["set"]):
       run_set(filename,doi)

    elif (arguments["del"]):
       run_del(filename,doi)

  

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(abbreviation_of_journal("journal of chemical physics"))
    main(arguments)  

