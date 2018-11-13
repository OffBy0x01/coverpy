#!/usr/bin/env python3

import argparse
import re
import sys

# Console colour codes
color_warning = '\033[93m'
color_success = '\033[92m'
color_default = '\033[0m'

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
        print(color_warning, "Failed to open file: %s" % (e), color_default)
        return 1

# Write cover letter to file
def write_cl(string, output_file):
    with open(output_file, "w") as of:
        of.write(string)

if __name__ == "__main__":
        # Arg Parsing
        parser = argparse.ArgumentParser()
        parser.add_argument("-file", nargs='?', default="basictemplate.txt")
        args = parser.parse_known_args()[0]

        # Read in template file
        filename = args.file
        file = get_file(filename)
        if file == 1:
            exit(1)

        # Find all template entries
        entries = re.findall("{{(.*?)}}", file)
        for entry in entries:
            parser.add_argument("-%s" % entry, nargs='?', default="UNSET")
            args = vars(parser.parse_known_args()[0])
            if args[entry] == "UNSET" or args[entry] == None:
                file = file.sub("{{%s}}" % entry, input("Enter value for '%s': " % entry))
            else:
                file = file.sub("{{%s}}" % entry, args[entry])


        # Write output
        if "." in filename:
            filename = filename.split(".")[-1]
        parser.add_argument("-outfile", nargs='?', default="%s_out.txt" % filename)
        parser.add_argument("-print", nargs='?', default="true")
        write_cl(file, parser.parse_known_args()[0].outfile)

        # print output by default
        if parser.parse_known_args()[0].print.lower() == "true":
            print(color_success, "\nFinished writing cover letter. That tooks aaaages ;)\n", color_default)
            print(file)

        # All done
        exit(0)
