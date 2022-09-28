import pdf2doi
import slugify
import calendar
import sys
import requests
import time
import shutil
import glob
import pybtex

from pybtex.database import parse_string as parse_bibtex

def request(url, headers=None, tries=3):

    errors = []  # Someday replace with ExceptionGroup when 3.11 becomes common
    while tries:
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()

            if r.status_code < 300:
                return r
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            errors.append(e)
        tries -= 1
    else:
        print(f"retry loop errors {errors}", file=sys.stderr)
        raise errors[-1]


def getbib(doi):

    print("retrieving DOI bibtex from dx.doi.org")
    url = f"http://dx.doi.org/{doi}"
    headers = {"accept": "application/x-bibtex"}
    # Conveniently this endpoint gives bibtex as desired
    return request(url, headers).text

def month_abbv_to_number(month_str):
    """
    convert 'jan' to '01', 'feb' to '02', etc.
    """
    lookup = {month.lower(): index
        for index, month in enumerate(calendar.month_abbr)}

    return f"{lookup[month_str.lower()]:02}"


def process_pdf(paper):

    """
    Tries to find DOI, and if so writes them to output directory /out/ with a
    single bibtex entry by same name as pdf.  When migrating from mendeley library
    that has corruption/duplicate entries it can be a many to one-write so you 
    probably do *not* want to put this in a multiprocessing pool
    """

    r = pdf2doi.pdf2doi(paper)

    print(f"identifier type : {r['identifier_type']}, value : {r['identifier']}")

    if r["identifier_type"] == "DOI":
        doi = r["identifier"]
        bib = getbib(doi)
        print(bib)

    elif r["identifier_type"] == "arxiv ID":
        # Arxiv IDs as of feb2022 are now DOIs
        doi = f"10.48550/arXiv.{r['identifier']}"
        bib = getbib(doi).replace("@misc", "@article")
        print(bib)
    else:
        print("unable to process {paper}")
        shutil.move(paper, 'failbox')
        return

    #bib = pybtex.database.parse_string(bib, 'bibtex')
    bib = parse_bibtex(bib, 'bibtex')
    for entryname in bib.entries:  #Iterable, one element
        print(entryname)
        entry = bib.entries[entryname].fields
        year = entry['year']
        try:
            month = month_abbv_to_number(entry['month'])
        except KeyError:
            month = '00'  # No month, assign 00.
        title = entry['title']
        filename = slugify.slugify(f"{entryname} {title}")
        filename = filename[:80]
        with open(f"outbox/{filename}.bib",'w') as f:
            f.write(bib.to_string('bibtex'))
        shutil.move(paper, f"outbox/{filename}.pdf")



if __name__ == "__main__":

    papers = glob.glob("inbox/*.pdf")

    for paper in sorted(papers):  # glob.glob not deterministic ordering
        print(f"Processing pdf {paper}")
        process_pdf(paper)
