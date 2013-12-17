#!/usr/bin/python

 

import sys

import re

import base64

import shutil

shutil.copyfile(sys.argv[1],"/tmp/emailrelay_lastmsg_received")

 

def chunks(l, n):

    """

         Yield successive n-sized chunks from l.

    """

    for i in xrange(0, len(l), n):

        yield l[i:i+n]

 

def modify_message(messagelines):

         """

         Modify message and return in same format of short lines

         """

         stagenumber = re.sub(".+172\.19\.(\d+)\..+\n", "\g<1>", messagelines[0])

         messagetext = re.sub("=\\r\\n", "", "".join(messagelines[9:len(messagelines)]))

         new_messagetext = re.sub("http(.+?)\.stage", "http\g<1>.com.{0}.stage".format(stagenumber), messagetext)

         new_messagelines = messagelines[0:9]

         for row in chunks(new_messagetext, 68):

                   new_messagelines.append(row + "=\r\n")

         new_messagelines[-1] = new_messagelines[-1][0:-3]

         return new_messagelines

 

try:

         with open(sys.argv[1]) as file:

                   msg_lines = file.readlines()

         stage_number = re.sub(".+172\.19\.(\d+)\..+\n", "\g<1>", msg_lines[0])

         for row in msg_lines:

                   if "----boundary" in row:

                            content_boundary = row[0:-2]

                            break

         for nrow in enumerate(msg_lines):

                   if "Content-Transfer-Encoding: base64" in nrow[1]:

                            msg_start = nrow[0]

                            break

         parse_lines = msg_lines[msg_start:]

        

         with open(sys.argv[1],'w') as file: file.writelines(modify_message(messagelines))

         shutil.copyfile(sys.argv[1],"/tmp/emailrelay_lastmsg_modified")

         print "Ok"

         LASTEXITCODE = 0

except Exception as e:

         print str(e)

         LASTEXITCODE = 1

sys.exit(LASTEXITCODE)
