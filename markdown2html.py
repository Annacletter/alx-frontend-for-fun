#!/usr/bin/python3
'''
Script markdown2html.py converts Markdown files to HTML.
Takes 2 string arguments:
- Markdown file name
- Output file name
'''

import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as markdown:
        with open(sys.argv[2], 'w') as html:
            unordered_list_start, ordered_list_start, paragraph = False, False, False
            # Handling markdown syntax
            for line in markdown:
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # Convert to MD5
                md5_matches = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5_matches:
                    line = line.replace(md5_matches[0], hashlib.md5(md5_inside[0].encode()).hexdigest())

                # Removing 'C' characters
                remove_c_matches = re.findall(r'\(\(.+?\)\)', line)
                remove_c_content = re.findall(r'\(\((.+?)\)\)', line)
                if remove_c_matches:
                    remove_c_content = ''.join(c for c in remove_c_content[0] if c not in 'Cc')
                    line = line.replace(remove_c_matches[0], remove_c_content)

                length = len(line)
                headings = line.lstrip('#')
                heading_num = length - len(headings)
                unordered = line.lstrip('-')
                unordered_num = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_num = length - len(ordered)
                
                # Handling headings and lists
                if 1 <= heading_num <= 6:
                    line = '<h{}>'.format(heading_num) + headings.strip() + '</h{}>\n'.format(heading_num)

                if unordered_num:
                    if not unordered_list_start:
                        html.write('<ul>\n')
                        unordered_list_start = True
                    line = '<li>' + unordered.strip() + '</li>\n'
                if unordered_list_start and not unordered_num:
                    html.write('</ul>\n')

