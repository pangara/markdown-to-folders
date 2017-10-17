"""This script converts a markdown file into folders that play nice with the e-guide template"""
import os
import re

with open("test.md", "rt") as mdFile:
    LINES = mdFile.read().split("\n")
    print LINES
    HEADING_PATTERN = re.compile('^(# )')
    SUBHEADING_PATTERN = re.compile('^(## )')

    for lineIndex in range(len(LINES)):
        line = LINES[lineIndex]
        if HEADING_PATTERN.match(line):
            dirName = line[2:]
            fileName = dirName + ".md"
            mainFile = open(fileName, "w")
            mainFile.write(line + "\n")
            if not os.path.exists(dirName):
                os.makedirs(dirName)
            lineIndex += 1
            line = LINES[lineIndex]
            while not HEADING_PATTERN.match(line) and not SUBHEADING_PATTERN.match(line):
                mainFile.write(line+ "\n")
                if lineIndex < len(LINES):
                    lineIndex += 1
                    line = LINES[lineIndex]
                else:
                    break

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
                    lineIndex += 1
                    if lineIndex < len(LINES):
                        line = LINES[lineIndex]
                    else:
                        break
            else:
                break
mdFile.close()
