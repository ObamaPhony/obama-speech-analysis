#!/usr/bin/env python3
#
# Short description of the program/script's operation/function.
#

import sys
import json
import nltk

def split_speeches(text):
    speeches = text.split(SPEECH_SEPARATOR)
    return speeches

def split_paragraphs(text):
    # 2, not 1? ok, weird
    title_offset = 2

    speeches = []
    for speech in text:
        # split & remove title (for now)
        paragraphs = speech.split(PARAGRAPH_SEPARATOR)[title_offset:]

        # remove empty elements
        paragraphs = list(filter(None, paragraphs))

        speeches.append(paragraphs)
    return speeches

def split_sentences(text):
    speeches = []
    for speech in text:
        paragraphs = []
        single_sentence_buffer = ""
        for i in range(len(speech)):
            sentences = speech[i].split(SENTENCE_SEPARATOR)

            # join single-sentence paragraphs
            # TODO: doesn't work for single-sentence paragraphs at the end (they
            #       are separated)
            if len(sentences) == 1 and i != len(speech) - 1:
                if sentences[0] != "":
                    # valid single-sentence found: add to buffer
                    single_sentence_buffer += speech[i] + " "
                    continue
            else:
                if single_sentence_buffer != "":
                    # if buffer is present, format & insert it
                    # [:-1] removes extra space from SENTENCE_SEPARATOR
                    buffer_sentences = single_sentence_buffer[:-1].split(SENTENCE_SEPARATOR)

                    # remove fullstops
                    # TODO: doesn't remove other ending punctuation
                    # TODO: code duplication LMFAO wHo cAREAS HAHA Xd
                    if buffer_sentences[-1].endswith("."):
                        buffer_sentences[-1] = buffer_sentences[-1][:-len(".")]

                    # insert it
                    paragraphs.append(buffer_sentences)

                    # clear buffer
                    single_sentence_buffer = ""

            sentences = speech[i].split(SENTENCE_SEPARATOR)

            # remove fullstops
            if sentences[-1].endswith("."):
                sentences[-1] = sentences[-1][:-len(".")]


            paragraphs.append(sentences)
        speeches.append(paragraphs)
    return speeches

def parse_speeches(full_text):
    speeches = full_text

    speeches = split_speeches(speeches)
    speeches = split_paragraphs(speeches)
    speeches = split_sentences(speeches)

    return speeches

def analyse_speeches(parsed_speeches):
    a_speeches = []

    for speech in parsed_speeches:
        a_paragraphs = []
        for paragraph in speech:
            a_sentences = []
            for i in range(len(paragraph)):
                sentence = paragraph[i]
                summary = summary_of(sentence)
                position = percent_at_index(i, paragraph)

                analysed_sentence = {
                        "sentence": sentence,
                        "summary": summary,
                        "position": position
                        }
                a_sentences.append(analysed_sentence)
            a_paragraphs.append(a_sentences)
        a_speeches.append(a_paragraphs)

    return a_speeches

def print_analysis_info(info):
    # DEBUG
    print(json.dumps(info, indent=2))

    #print(json.dumps(info))

def percent_at_index(index, array):
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
    summary = summary_of(sentence)

    position = percent_of_index(i, speech)

    info = {"sentence": sentence,
            "summary": summary,
            "position": position
            }
    return info

def summary_of(sentence):
    tokens_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))

    return tokens_tagged

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
    #summary_words = [ tagged_word[0] for tagged_word in list(filter(lambda word: word[1] in allowed_tags, tokens_tagged)) ]




SENTENCE_SEPARATOR = ". "
PARAGRAPH_SEPARATOR = "\n"
SPEECH_SEPARATOR = "\n" * 3

full_speeches_text = sys.stdin.read()
parsed_speeches = parse_speeches(full_speeches_text)

analysis_info = analyse_speeches(parsed_speeches)

print_analysis_info(analysis_info)
