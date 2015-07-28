#!/usr/bin/env python3
#
# Short description of the program/script's operation/function.
#

import sys
import json
import nltk

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

def form_json(info):
    """Form JSON using expected keys in an input dictionary.

    Note that in the end it's basically selecting keys from a dictionary, which
    could be done easier, but the actual operation *isn't* actually that,
    because the keys in the input dictionary shouldn't be forced to be the same
    as the JSON format keys. So I'm not doing a shorter filter function.
    """

    json = {"sentence": info["sentence"],
            "summary": info["summary"],
            "position": info["position"],
            }
    return json

def get_info_for_index(i, speech):
    sentence = speech[i]
    summary = get_summary_of(sentence)

    position = get_percent_of(i, speech)

    info = {"sentence": sentence,
            "summary": summary,
            "position": position
            }
    return info

def get_summary_of(sentence):
    tokens_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    allowed_tags = [
            "NN",
            "NNS",
            "NNP",
            "NNPS",
#            "FW",
#            "JJ",
#            "JJR",
#            "JJS",
#            "VB",
#            "VBD",
#            "VBG",
#            "VBN",
#            "VBP",
#            "VBZ",
#            "RB",
#            "RBR",
#            "RBS"
            ]
    summary_words = [ tagged_word[0] for tagged_word in list(filter(lambda word: word[1] in allowed_tags, tokens_tagged)) ]

    return summary_words

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
        # get all info
        info = get_info_for_index(i, speech)

        # form JSON using info
        sentence_json = form_json(info)

        # add to data dictionary
        data["data"].append(sentence_json)

print(json.dumps(data, indent=2))
