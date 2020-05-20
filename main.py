#!/usr/bin/env python3

import os
import mark_parser
import sendemail

course = "COURSE NAME"

def main():
    diff = mark_parser.get_diff()
    msg = ""

    msg = "Hello,\n\n"
    for key in diff:
        value = diff[key]
        msg += ("Column \"%s\" in %s\'s grade book changed from %s to %s.\n" % (key, course, str(diff[key][0]), str(diff[key][1])))

    msg += "\nCongrats! :)"

    if diff:
        sendemail.send_email(msg)

if __name__ == '__main__':
    main()
