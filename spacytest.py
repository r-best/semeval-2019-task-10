import spacy
import json
from pprint import pprint
import re

##
# Takes in a filepath and returns its contents
# read as a JSON object
##
def readData(path):
    text = ""
    with open(path) as fp:
        text = fp.read()
    return json.loads(text)

##
# Takes in the json object containing all the training
# questions and applies preprocessing rules to it.
# Returns the processed json
##
def preprocessing(json):
    json = [x for x in json if x['tags'] == ['closed']]
    json = [x for x in json if 'diagramRef' not in x]
    
    for x in json:
        x['question'] = x['question'].replace(r'\(', '[ ')
        x['question'] = x['question'].replace(r'\)', ' ]')
        x['question'] = x['question'].replace(r'\%', '%')
        x['question'] = re.sub(
            r'\\frac \{ ([\d\w]+) \} \{ ([\d\w]+) \}',
            r'\1 / \2',
            x['question'])
    
    return json

##
# Custom pipeline for Spacy to split sentences
# strictly on newlines, taken from Spacy docs
# https://spacy.io/usage/linguistic-features#sbd-custom
##
def custom_sentence_splitter(doc):
    start = 0
    seen_newline = False
    for word in doc:
        if seen_newline and not word.is_space:
            yield doc[start:word.i]
            start = word.i
            seen_newline = False
        elif word.text == '\n':
            seen_newline = True
    if start < len(doc):
        yield doc[start:len(doc)]


def main():
    nlp = spacy.load('en')
    nlp.add_pipe(
        spacy.pipeline.SentenceSegmenter(nlp.vocab,strategy=custom_sentence_splitter),
        before='parser')

    data = readData('codalab/test_data/truth.json')
    data = preprocessing(data)

    # for x in data:
    #     print(x['question'])

    data = '\n'.join([x['question'] for x in data])
    doc = nlp(data)

    i = 0
    for sent in doc.sents:
        print("{} --- {}".format(i, sent))
        i = i+1
    
    print("PIPES:", nlp.pipe_names)
    
    # spacy.displacy.serve(doc, style='dep')


if __name__ == '__main__':
    main()
