import re
from .testLines import replaceLyrics

# input_file = open('input.txt', 'r')
# output_file = open('output.txt', 'w+')

def is_chord_line(line):
    # alt: avg # letters per word

    chords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'F#']
    # need minor chords
    # need / chords e.g. D/F#
    # need # and flat chords
    if any(word in line for word in chords):
        return True
    return False


def is_section_name(line):
    section_names = ['intro', 'verse', 'chorus', 'bridge', 'pre-chorus', 'outro', 'tag']

    if len(line) <= 2:
        for word in line:
            word = word.lower()
            for section_name in section_names:
                if section_name in word:
                    return True
    return False

def make_presentation(text):
# converts input_file to list of lists. Each list is a line from the file
    input_list = []
    for orig_line in text.split('\n'):
        # split oriignal line by /'s
        split_lines = orig_line.split('/')
        # add each line into input_list as list
        for line in split_lines:
            line = line.replace(' - ', '')
            line = line.replace('-', '')
            input_list.append(line.split())


    # filtering
    for i in range(0, len(input_list)):
        line = input_list[i]
        # remove chord lines
        if is_chord_line(line):
            input_list[i] = []

        if is_section_name(line):
            input_list[i] = ['-----']

    # remove empty lines
    output = [line for line in input_list if line]
    print(output)

    # line numbers of section dividers
    section_dividers = [0]
    for i in range(0, len(output)):
        if output[i][0] == '-----':
            section_dividers.append(i)

    output_final = []

    # check if any sections are too large
    for i in range(1, len(section_dividers)):
        beg_section = section_dividers[i-1]
        end_section = section_dividers[i]
        if end_section - beg_section - 1 >= 6:
            midpoint = (beg_section + end_section) // 2
            output_final.extend(output[beg_section:midpoint + 1])
            output_final.append(['-----'])
            output_final.extend(output[midpoint + 1:end_section])
        else:
            output_final.extend(output[beg_section:end_section])

    print(section_dividers)

    lyrics_by_line = [' '.join(l) for l in output_final]

    return replaceLyrics(lyrics_by_line, 'b')

