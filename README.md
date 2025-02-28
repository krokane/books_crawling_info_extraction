## Books + Authors Web Crawling and Information Extraction

This project uses web crawling techniques in Scrapy and NLP techniques in SpaCy to crawl Open Library and Wikipedia sites to collect text data, and then extract information from this text regarding books and authors. The web crawler, built with Scrapy, collects information about 100 books from the forever trending pages of Open Library's catelog. The crawler follows links both within the Open Library site and Wikipedia links associated with authors' pages to collect text information about the author. Then, using lexical and syntatic extractors and NLP techniques such as surface text pattern detection, parts of speech tagging, and named entity recognition in SpaCy, information regarding the authors is collected into json files. 

### Required libraries 
scrapy, json, pandas, spacy
