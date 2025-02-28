from spacy.matcher import Matcher
import json
import pandas as pd
import spacy

data = pd.read_json("/Users/kevin/Desktop/DSCI558/Homework/hw01/hw01/spiders/Kevin_OKane_hw01_author.json")

nlp = spacy.load("en_core_web_md")
lex_matcher = Matcher(nlp.vocab)
syn_matcher = Matcher(nlp.vocab)

data['docs'] = data['biography'].apply(lambda x: nlp(x) if x != None else None)
data['birthplace_lex'] = None
data['genre_lex'] = None
data['notable_books_lex'] = None
data['awards_lex'] = None
data['education_lex'] = None
data['birthplace_syn'] = None
data['genre_syn'] = None
data['notable_books_syn'] = None
data['awards_syn'] = None
data['education_syn'] = None

### Lexical Extractor    
birthplace1 = [{"LOWER":"born"}, {"LOWER":"in"},{"IS_TITLE":True, "OP":"+"}]
birthplace2 = [{"LOWER":"is"}, {"LOWER":"from"},{"IS_TITLE":True, "OP":"+"}]
birthplace3 = [{"LOWER":"lives"}, {"LOWER":"in"},{"IS_TITLE":True, "OP":"+"}]
birthplace4 = [{"LOWER":"lived"}, {"LOWER":"in"},{"IS_TITLE":True, "OP":"+"}]
birthplace5 = [{"LOWER":"resides"}, {"LOWER":"in"},{"IS_TITLE":True, "OP":"+"}]
birthplace6 = [{"LOWER":"resided"}, {"LOWER":"in"},{"IS_TITLE":True, "OP":"+"}]
birthplace7 = [{"LOWER":"based"}, {"LOWER":"in"},{"IS_TITLE":True, "OP":"+"}]
birthplace8 = [{"LOWER":"located"}, {"LOWER":"in"},{"IS_TITLE":True, "OP":"+"}]
birthplace9 = [{"LOWER":"birthplace"}, {"LOWER":"is"},{"IS_TITLE":True, "OP":"+"}]
birthplace10 = [{"LOWER":"birthplace"}, {"LOWER":"of"},{"IS_TITLE":True, "OP":"+"}]
birthplace11 = [{"LOWER":"grew"},{"LOWER":"up"}, {"LOWER":"in"},{"IS_TITLE":True, "OP":"+"}]
birthplace12 = [{"IS_TITLE":True, "TEXT":{"REGEX":".*ish$"}}]
birthplace13 = [{"IS_TITLE":True, "TEXT":{"REGEX":".*ese$"}}]
birthplace14 = [{"IS_TITLE":True, "TEXT":{"REGEX":".*can$"}}]
birthplace15 = [{"IS_TITLE":True, "TEXT":{"REGEX":".*ian$"}}]

genre = [{"LOWER": {"IN" :['fantasy','science-fiction','sci-fi','history','fiction',
                  'non-fiction', 'mystery', 'young adult', 'mystery', 'horror','self-improvement',
                  'literature', 'novel', 'thriller', 'novella', 'short-story', 'crime', 'biography']}}]

notable_books1 = [{"LOWER": {"IN":["best-seller", "best seller"]}}, {"IS_TITLE": True, "OP": "+"}]
notable_books2 = [{"TEXT": "series"}, {"IS_TITLE": True, "OP": "+"}]
notable_books3 = [{"IS_TITLE": True, "OP": "+"}, {"TEXT": "series"}]

awards1 = [{"IS_TITLE": True, "OP": "+"}, {"LOWER": "award"}]
awards2 = [{"IS_TITLE": True, "OP": "+"}, {"LOWER": "prize"}]
awards3 = [{"IS_TITLE": True, "OP": "+"}, {"LOWER": "medal"}]

education1 = [{"TEXT": "University of"}, {"IS_TITLE":True, "OP": "+"}]
education2 = [{"IS_TITLE":True, "OP": "+"}, {"TEXT": "University"}]
education3 = [{"IS_TITLE":True, "OP": "+"}, {"TEXT": "College"}]

lex_matcher.add("birthplace_lex", [birthplace1, birthplace2, birthplace3, birthplace4, birthplace5, birthplace6,
                               birthplace7, birthplace8, birthplace9, birthplace10, birthplace11, birthplace12,
                               birthplace13, birthplace14, birthplace15])
lex_matcher.add("genre_lex", [genre])
lex_matcher.add("notable_books_lex", [notable_books1, notable_books2, notable_books3])
lex_matcher.add("awards_lex", [awards1, awards2,awards3])
lex_matcher.add("education_lex", [education1, education2, education3])


for i in range(len(data['docs'])):
    doc = data['docs'][i]
    if doc == None: continue    
    matches = lex_matcher(doc)
    for match_id, start, end in matches:
        col = nlp.vocab.strings[match_id]
        match_text = ' '.join([token.text for token in doc[start:end]])
        data.loc[i, col] = match_text

for i in range(len(data['birthplace_lex'])):
    bp = data['birthplace_lex'][i]
    bp_words = ['in', 'born', 'from', 'is', 'lives', 'lived', 'resides', 'resided', 'based',
                'located', 'birthplace', 'grew', 'up', 'of']
    if bp == None: continue
    if (len(bp.split()) > 1):
        data.loc[i,'birthplace_lex'] = " ".join([item for item in bp.split() if item not in bp_words])
    if bp == "American": data.loc[i,'birthplace_lex'] = 'United States'
    if bp == "English": data.loc[i,'birthplace_lex'] = 'United Kingdom'
    if bp == "Italian": data.loc[i,'birthplace_lex'] = 'Italy'   
    if bp == "German": data.loc[i,'birthplace_lex'] = 'Germany'
    if bp == "Canadian": data.loc[i,'birthplace_lex'] = 'Canada'
    if bp == "Japanese": data.loc[i,'birthplace_lex'] = 'Japan'
    if bp == "Spanish": data.loc[i,'birthplace_lex'] = 'Spain'
    if bp == "Chinese": data.loc[i,'birthplace_lex'] = 'China'
    if bp == "Scottish": data.loc[i,'birthplace_lex'] = 'Scotland'
    if bp == "Irish": data.loc[i,'birthplace_lex'] = 'Ireland'
    if bp == "British": data.loc[i,'birthplace_lex'] = 'United Kingdom'
    if bp == "Brazilian": data.loc[i,'birthplace_lex'] = 'Brazil'
    if bp == "Korean": data.loc[i,'birthplace_lex'] = 'Korea'

for i in range(len(data['notable_books_lex'])):
    nb = data['notable_books_lex'][i]
    nb_words = ['best-seller','series','best seller']
    if nb == None: continue
    else: data.loc[i,'notable_books_lex'] = " ".join([item for item in nb.split() if item not in nb_words])

### Syntactic Extractor
for i in range(len(data['docs'])):
    if data['docs'][i] == None: continue
    doc = nlp(data['docs'][i])
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            data.loc[i,'birthplace_syn'] = ent.text
            break
    for ent in doc.ents:
        if ent.label_ == 'WORK_OF_ART' and 'prize' not in ent.text.lower() and 'award' not in ent.text.lower():
            if data.loc[i,'notable_books_syn'] == None:
                data.at[i,'notable_books_syn'] = []
                data.loc[i,'notable_books_syn'].append(ent.text)
            else: data.loc[i,'notable_books_syn'].append(ent.text)
        if 'prize' in ent.text.lower() or 'award' in ent.text.lower() or 'medal' in ent.text.lower():
            if data.loc[i,'awards_syn'] == None:
                data.at[i,'awards_syn'] = []
                data.loc[i,'awards_syn'].append(ent.text)
            else: data.loc[i,'awards_syn'].append(ent.text)
        if 'school' in ent.text.lower() or 'university' in ent.text.lower() or 'college' in ent.text.lower() and ent.label_ == 'ORG':
            if data.loc[i,'education_syn'] == None:
                data.at[i,'education_syn'] = []
                data.loc[i,'education_syn'].append(ent.text)
            else: data.loc[i,'education_syn'].append(ent.text)
    book_words = ['book','books','novel','novels','work','works','lit','literature']
    for token in doc:
        if token.pos_ in ['ADJ','NOUN','PNOUN'] and token.head.text.lower() in book_words and token.text not in book_words and len(token.text) >= 4:
            if data.loc[i,'genre_syn'] == None:
                data.at[i,'genre_syn'] = []
                data.loc[i,'genre_syn'].append(token.text)
            else: data.loc[i,'genre_syn'].append(token.text)

### Dump to JSON
def convert_to_json(row):
    return {
        "syntactic": {
            "birthplace": row['birthplace_syn'],
            "genres": row['genre_syn'],
            "notable_books": row['notable_books_syn'],
            "awards": row['awards_syn'],
            "education": row['education_syn']
            },
        "lexical": {
            "birthplace": row['birthplace_lex'],
            "genres": row['genre_lex'],
            "notable_books": row['notable_books_lex'],
            "awards": row['awards_lex'],
            "education": row['education_lex']
            }
        }

with(open('Kevin_OKane_hw01_authorIE.jsonl','w')) as f:
    for index, row in data.iterrows():
        json_line = convert_to_json(row)
        f.write(json.dumps(json_line) + "\n")