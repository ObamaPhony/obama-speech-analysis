#!/usr/bin/env python3
#
# Short description of the program/script's operation/function.
#

import sys



SENTENCE_SEPARATOR = ". "
PARAGRAPH_SEPARATOR = "\n"
SPEECH_SEPARATOR = "\n" * 3

full_speeches_text = sys.stdin.read()

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

print(formatted_speeches)
