#!/bin/python
#
# Vanderbilt University Computer Science
# Author: Aniruddha Gokhale
# Course: CS4287-5287 Principles of Cloud Computing
# Created: Fall 2016
#
# Purpose: To show to execute a command on a remote host, which you
# will need in your assignment because a lot of things will need to be
# installed on the remote machine from your client code
#

#

import sys
import subprocess as sp

# main 
def main ():

    # Suppose I want to copy my flask file to remote server. To that end,
    # set up the arg list. You can pass this as one large string or
    # break it down like this and Python subprocess will handle it
    #
    # Path to pem file could be something like ~\.ssh\your_pem_file
    # file that you want to transfer could be something like
    # assign1_server.py
    args = ['scp',
            '-i',
            '<YOUR PEM FILE GOES HERE>',
            '<NAME OF FILE YOU WANT TO TRANSFER GOES HERE>',
            'ubuntu@129.59.107.X:/home/ubuntu'] # replace X

    try:
        p = sp.Popen (args)
        retcode = p.wait ()
        print ('Subprocess exited with status: ', retcode)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # Suppose I want to install pip on my server
    args = ['ssh',
            '-i',
            '<YOUR PEM FILE GOES HERE>',
            'ubuntu@129.59.107.X:/home/ubuntu', # replace X
            'sudo apt-get install python-dev python-pip']

    try:
        p = sp.Popen (args)
        retcode = p.wait ()
        print ('Subprocess exited with status: ', retcode)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # Suppose I want to install flask on my server
    args = ['ssh',
            '-i',
            '<YOUR PEM FILE GOES HERE>',
            'ubuntu@129.59.107.X:/home/ubuntu', # replace X
            'sudo python -m pip install flask']

    try:
        p = sp.Popen (args)
        retcode = p.wait ()
        print ('Subprocess exited with status: ', retcode)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # The code below will run the flask app on the server. I have commented
    # it out but you can uncomment and try. Naturally, you will need to
    # change the IP address, and the key 
#    args = ['ssh',
#            '-i',
#            'PEM FILE',
#            'ubuntu@129.59.107.X',
#            'cd Assignment1; export FLASK_APP=assign1_server_skel.py; python -m flask run --host=0.0.0.0 --port 8080']

#    try:
#        p = sp.Popen (args)
#    except:
#        print "Exception thrown: ", sys.exc_info()[0]
#        raise

# invoke main
if __name__ == "__main__":
    sys.exit (main ())
    

