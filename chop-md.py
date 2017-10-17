"""This script converts a markdown file into folders that play nice with the e-guide template"""
import os
import re

with open("test.md", "rt") as mdFile:
    LINES = mdFile.read().split("\n")
    print LINES
    # Regular expressions to match headings, sub headings and sub sub headings
    HEADING_PATTERN = re.compile('^(# )')
    SUBHEADING_PATTERN = re.compile('^(## )')
    SUBSUBHEADING_PATTERN = re.compile('^(### )')

    for lineIndex in range(len(LINES)):
        line = LINES[lineIndex]
        # If it is the heading,
        # make a folder with the same name as heading
        # make a file with the same name as heading
        if HEADING_PATTERN.match(line):
            dirName = line[2:]
            fileName = dirName + ".md"
            mainFile = open(fileName, "w")
            mainFile.write(line + "\n")
            if not os.path.exists(dirName):
                os.makedirs(dirName)
            lineIndex += 1
            line = LINES[lineIndex]
            # Iterate over the text in the section description and add it to the new md file
            while not HEADING_PATTERN.match(line) and not SUBHEADING_PATTERN.match(line):
                mainFile.write(line+ "\n")
                if lineIndex < len(LINES):
                    lineIndex += 1
                    line = LINES[lineIndex]
                else:
                    break
        # Inside each of the folders make md files for each of the subsections and fill in content
        if SUBHEADING_PATTERN.match(line):
            subFile = open(dirName + "/" + line[3:] + ".md", "w")
            subFile.write("---\n")
            subFile.write("title: " + dirName + "\n")
            subFile.write("navtitle: " + dirName +"\n")
            subFile.write("---\n")
            subFile.write(line)
            lineIndex += 1
            if lineIndex < len(LINES):
                line = LINES[lineIndex]
                while not HEADING_PATTERN.match(line) and not SUBHEADING_PATTERN.match(line):
                    subFile.write(line +"\n")
                    if SUBSUBHEADING_PATTERN.match(line):
                        subFile.write("---\n")
                    lineIndex += 1
                    if lineIndex < len(LINES):
                        line = LINES[lineIndex]
                    else:
                        break
            else:
                break
mdFile.close()
