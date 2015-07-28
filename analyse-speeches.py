#!/usr/bin/env python3
#
# Short description of the program/script's operation/function.
#

import sys
import json

def get_percent_of(index, array):
    """Get the percent position of the string in a string array."""
    # 1. get length before
    # 2. get half length of array[index] string
    # 3. get length of all strings in array
    # 4. return length before + half length / length of all strings

    length_before = 0
    for i in range(index):
        length_before += len(array[i])

    length_full = length_before
    for i in range(index, len(array)):
        length_full += len(array[i])

    length_at_index = length_before + (len(array[index])/2)
    percent_at_index = length_at_index / length_full

    return percent_at_index

def form_json(sentence, summary, previous_summary, position):
    """Form JSON."""
    json = {"sentence": sentence,
            "summary": summary,
            "prev_summary": previous_summary,
            "position": position
            }
    return json


SENTENCE_SEPARATOR = ". "
PARAGRAPH_SEPARATOR = "\n"
SPEECH_SEPARATOR = "\n" * 3

full_speeches_text = sys.stdin.read()

## Split input into speeches, sentences {{{

# separate text into speeches
speeches = full_speeches_text.split(SPEECH_SEPARATOR)

# separate speeches into paragraphs
speeches_paragraphs = []
for speech in speeches:
    speeches_paragraphs.append(speech.split(PARAGRAPH_SEPARATOR))

# separate paragraphs into sentences
speeches_sentences = []
for speech in speeches_paragraphs:
    current_speech = []
    for paragraph in speech:
        sentences = paragraph.split(SENTENCE_SEPARATOR)
        if sentences[-1].endswith("."):
            sentences[-1] = sentences[-1][:-len(".")]
        current_speech.extend(sentences)

    speeches_sentences.append(current_speech)

# remove empty elements
speeches_no_empty = []
for speech in speeches_sentences:
    current_speech = []
    current_speech.extend(filter(None, speech))
    speeches_no_empty.append(current_speech)

# remove speech titles (for now we're not using them)
speeches_no_title = []
for speech in speeches_no_empty:
    speeches_no_title.append(speech[1:])

# set finished variable
formatted_speeches = speeches_no_title

# }}}

data = {"data": []}

for speech in formatted_speeches:
    for i in range(len(speech)):
        sentence = speech[i]
        summary = ["example summary", "ex. sum. pt 2"]
        previous_summary = ["example previous summary", "ex. summary pt. 2"]
        position = get_percent_of(i, speech)

        sentence_json = form_json(sentence, summary, previous_summary, position)
        data["data"].append(sentence_json)
        print(position)

print(json.dumps(data, indent=2))
