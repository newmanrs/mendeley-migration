# mendeley-migration

Parsing papers for DOIs so I can migrate away from Mendeley Desktop.  Features continue to be removed, and the replacement application works so poorly that I'm fed up with it.

This repo contains scripts to parse over a folder (inbox) of PDFs and runs [pdf2doi](https://github.com/MicheleCotrufo/pdf2doi) to obtain DOIs and then queries http://dx.doi.org to obtain bibtex files.  If this is successful, the pdf is renamed and moved to the outbox folder alongside the bibtex. The script works reasonably, but some PDFs do fail, and the process is slow.  Except a few crashes if porting a large number of files.  DOIs can also be inserted into problematic pdfs manually using the [pdf2doi](pdf2doi "path\to\pdf" -id "doi1234") cli. 

More tooling to search these files is likely forthcoming.
