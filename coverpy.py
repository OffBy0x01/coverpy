#!/usr/bin/env python3

import argparse
import re
import sys
import os

# Console colour codes
color_success = '\033[92m'
color_warning = '\033[93m'
color_danger = '\033[91m'
color_info = '\033[94m'

# Text Decoration
decoration_bold = '\033[1m'
decoration_underline = '\033[4m'

# Clear all formatting
format_clear = '\033[0m'

def bold(string):
    return decoration_bold + string + format_clear

def underline(string):
    return decoration_underline + string + format_clear

def info(string):
    return color_info + string + format_clear

def danger(string):
    return color_danger + string + format_clear

def warning(string):
    return color_warning + string + format_clear

def success(string):
    return color_success + string + format_clear



# Extend string to use regex
class Substitutable(str):
  def __new__(cls, *args, **kwargs):
    newobj = str.__new__(cls, *args, **kwargs)
    newobj.sub = lambda fro,to: Substitutable(re.sub(fro, to, newobj))
    return newobj

# Get template file
def get_file(filename_ext):
    try:
        return Substitutable(''.join([line for line in open(filename_ext)]))
    except Exception as e:
        print(warning("Failed to open file: %s" % (e)))
        return 1

# Write cover letter to file
def write_cl(string, output_file):
    with open(output_file, "w") as of:
        of.write(string)

if __name__ == "__main__":
        # Arg Parsing
        parser = argparse.ArgumentParser()
        # File in
        parser.add_argument("-file", nargs='?', required=True)
        # Boolean if the file is a tex file
        parser.add_argument("-tex", nargs='?', default=False, required=False)
        # Replace with other file
        parser.add_argument("-fileinclude", nargs='?', default=False, required=False)
        args = parser.parse_known_args()[0]

        # Read in template file
        tex = args.tex
        fileinclude = args.fileinclude
        filename = args.file
        file = get_file(filename)
        if file == 1:
            exit(1)

        print(info("Using template '%s'..." % filename))
        print(file)

        # Find all template entries
        entries = re.findall("{{(.*?)}}", file)

        # For each placeholder
        for entry in entries:
            # Check for a set argument
            parser.add_argument("-%s" % entry, nargs='?', default="UNSET")
            args = vars(parser.parse_known_args()[0])

            if fileinclude:
                # When file include is enabled check for a file with the placeholder name
                fileincludename = "./includes/{}".format(entry)
                substitute = get_file(fileincludename)
                
                while substitute == 1:
                    fileincludename = input(info("'%s' could not be found. Enter an alternative file and path from %s: " % (entry, os.getcwd())))
                    substitute = get_file(fileincludename)
                
                file = file.sub("{{%s}}" % entry, substitute)
                
            else:
                if args[entry] == "UNSET" or args[entry] == None:
                    file = file.sub("{{%s}}" % entry, input(info("Enter value for '%s': " % entry)))
                else:
                    file = file.sub("{{%s}}" % entry, args[entry])

        # Write output
        if "." in filename:
            filename = filename.split(".")[0]
            parser.add_argument("-outfile", nargs='?', default="%s_out" % filename)
            write_cl(file, parser.parse_known_args()[0].outfile)
            if tex:
                os.system("pdflatex %s" % parser.parse_known_args()[0].outfile)

        # print output by default
        parser.add_argument("-print", nargs='?', default="true")
        if parser.parse_known_args()[0].print.lower() == "true":
            print(success("\nFinished writing cover letter.\n"))
            print(file)

        # All done
        exit(0)
