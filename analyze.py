import json, re

def getTagCounts(arrays):
    counts = { 'geometry': 0, 'open': 0, 'closed': 0, 'other': 0, 'none':0, 'multiple':0, 'total':0 }
    for arr in arrays:
        counts['total'] += 1
        if len(arr) == 0:
            counts['none'] += 1
        elif len(arr) > 1:
            counts['multiple'] += 1
        else:
            counts[arr[0]] += 1
    return counts

def getAnswerCounts(anwsers):
    counts = { 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E':0, 'other':0 }
    for ans in anwsers:
        if ans in counts:
            counts[ans] += 1
        else:
            counts['other'] += 1
    return counts

def getExamCounts(exams):
    counts = {}
    for ex in exams:
        if ex in counts:
            counts[ex] += 1
        else:
            counts[ex] = 1
    return counts

def allAre(opts, regex):
    allAre = True
    for opt in opts:
        if not re.match(regex, opts[opt]):
            allAre = False
    return allAre

def contains(opts, regex):
    contains = False
    for opt in opts:
        if re.match(regex, opts[opt]):
            contains = True
    return contains
    
def getChoiceTypeCounts(choices):
    counts = { 'all_numeric':0, 'word':0, 'equation':0, 'diagram':0, 'combo':0 }
    for options in choices:
        if allAre(options, r'^-?\d+\.?\d*$'):
            counts['all_numeric'] += 1
        elif allAre(options, r'^I+[ ,]'):
            counts['combo'] += 1
        elif contains(options, r'^[\\\(f]'):
            counts['equation'] += 1
        elif allAre(options, r'^diagram\d+'):
            counts['diagram'] += 1
        else:
            counts['word'] += 1
    return counts

with open('data/sat.train.json', 'r') as f:
    questions = json.load(f)

count = 0
section_lengths = 0
section_nums = 0
answers = []
tags = []
dia_tags = []
exams = []
choices = []
for quest in questions:
    count += 1
    section_lengths += quest['sectionLength']
    section_nums += quest['sectionNumber']
    tags.append(quest['tags'])
    answers.append(quest['answer'])
    exams.append(quest['exam'])
    if 'choices' in quest:
        choices.append(quest['choices'])
    if "diagramRef" in quest:
        dia_tags.append(quest['tags'])

description = {}
description['num_questions'] = count
description['num_with_diagram_by_tag'] = getTagCounts(dia_tags)
description['percent_with_diagram'] = 100*len(dia_tags)/count
description['total_tag_counts'] = getTagCounts(tags)
description['answer_counts'] = getAnswerCounts(answers)
description['source_exam_counts'] = getExamCounts(exams)
description['choice_type_counts'] = getChoiceTypeCounts(choices)
description['average_section_length'] = section_lengths/count
description['average_num_in_section'] = section_nums/count

with open("data_demographics.json", 'w') as out:
    json.dump(description, out, sort_keys=True, indent=2, separators=(',', ': '))