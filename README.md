# mendeley-migration

For years I've been using Mendeley Desktop to store/manage my research articles.  However, since its purchase my Elsevier years ago the product has languished, and features continue to be removed, and its internal database at least for me is fully broken, so the program cannot even rename my papers by Author_Year_Title correctly.  I could probably move to zotero, but at this point I'm pretty content so long as I can get proper file renaming and obtain reliable citations.

Thus far this repo contains scripts to parse over a folder (inbox) of PDFs and runs [pdf2doi](https://github.com/MicheleCotrufo/pdf2doi) to obtain DOIs and then queries http://dx.doi.org to obtain bibtex files for the PDFs.  If this operation is successful, the pdf is renamed and moved to the outbox folder alongside the bibtex. The script works reasonably well, but some PDFs do fail to parse (ofc some of these also failed to open).  Expect a few crashes if porting a large number of files.  The pdf2doi library cleverly falls back to google searches using title information and then the early words in the pdf - the accuracy of this was probably harmed by Mendeley naming the articles entirely wrong, leading to mismatches.  DOIs can also be resolved to PDFs manually using the pdf2doi package's cli as follows: `pdf2doi "path\to\pdf" -id "doi1234"`.

A crude correctness checking script is provided in check_images.sh, which uses imagemagic to superimpose the text of the `.bib` files over the PDFs, allowing for manual inspection in your favorite gallery viewer of choice.  I recommend then deleting correct images, and then resolving the errors manually.

The individual bibtex files associated with the pdfs can be combined into a single `.bib` file with the script[compilebibtex.sh](compilebibtex.sh).  If the given bibtex cite keys have collisions, md5-sums of the bib files are added to the cite keys.  While a bit cumbersome in appearance, this should prevent issues with citations breaking if additional works by same author name and year are added.  That said using the md5 hash implies we're also relying on dx.doi.org to not update their citations.  

# Future work / TODO

I likely will try to make basic author, title, and article search features to look over the PDFs.  And perhaps the collision resolution should just append more information before immediately going to an md5-sum, maybe either by adding more than author_year such as title/journal/month.  For now you can grep/pdfgrep and your favorite cli bibtex tool to search for authors.
