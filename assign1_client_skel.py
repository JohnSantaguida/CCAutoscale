#!/bin/python
#
# Vanderbilt University Computer Science
# Author: Aniruddha Gokhale
# Course: CS4287-5287 Principles of Cloud Computing
# Created: Fall 2016
#
# Purpose: To provide a skeleton to implement the client side code skeleton
#

# system facilities
import sys

# http related facilities
import httplib

# import timer stuff to record the time
import time

# json stuff
import json

#server create module 
from nova_server_create import create
import subprocess as sp


# print the response (for debugging purposes)
def print_response (resp):
    print "printing response headers"
    try:
        for hdr in resp.getheaders ():
            print hdr
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    print "printing received data"
    try:
        data = resp.read ()
        print "Length of data = ", len(data)
        print data
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

# send a http request to the server.
def send_req (conn, arg):

    # send GET request to the server using the args
    try:
        conn.request ("GET", arg)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # retrieve the response
    try:
        resp = conn.getresponse ()
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    return resp

# main: In this sample code, we send a few requests:
# first a simple http message to the web server's main page and
# then the dummy_op request multiple times, an autoscale request with
# round robin policy, and finally an autoscale request with the proportional
# dispatch policy along with the ratio in which subsequent requests are
# going to be handled 
def main ():
   
    #Specify the Floating IP for accessing the 2nd tier VM 
    FINAL_FLOATING_IP = "129.59.107.47"
    print "floating ip is " + FINAL_FLOATING_IP
    print "Instantiating a connection obj"
    #This block creates the 2nd tier VM and the first 3rd tier VM
    name = 'jspm_tier2'
    print "creating server: " + name
    create(name, FINAL_FLOATING_IP)
    print name + " created"
    name = 'jspm_tier3_1'
    print "creating server: " + name
    TIER_3_1_IP_ADDRESS = create(name)
    print name + " created"  
    print "Tier 3 IP address: " + str(TIER_3_1_IP_ADDRESS)
    try:
        # @@@ NOTE @@@
        # if you are trying this locally, use this and by using
        # 8081, I am sending to the relay server
#        conn = httplib.HTTPConnection ("localhost", "8081")
#        conn = httplib.HTTPConnection ("localhost", "8080")

        # if you try this to talk to your server which has a floating IP, 
        # then you use the following and parametrize it with the
        # actual floating IP
        conn = httplib.HTTPConnection (FINAL_FLOATING_IP, "8080")
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise
    
    #EXECUTE NECESSARY REMOTE COMMANDS - DOES NOT WORK
    args = 'ssh -i ~/.ssh/santaguida.pem ubuntu@' + str(FINAL_FLOATING_IP) + ' sudo apt-get install python-dev python-pip '

    try:
        p = sp.Popen (args, shell=True)
        retcode = p.wait ()
        print 'Subprocess exited with status: ', retcode
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise
    # @@@ NOTE @@@
    # In your code, you should first start the main client-facing server on the
    # horizon cloud. See my sample code nova_server_create.py on how to do
    # this. You will need to do a bit more to that file so that it can
    # be imported here and you can use the functions. 
    
    # Once the main server is active, also proceed to start the first VM on the
    # 3rd tier. Inform the client-facing server the IP address of the
    # 3rd tier VM so that the client-facing server can relay your requests
    # to that VM thereafter.

    # In the following I am just doing some client-server activity. For your
    # program modify as appropriate.

    # first make a request to the top level page
    print "Sending request for top level page"
    send_req (conn, "/")

    # send the dummy request which takes some time to execute
    print "Sending request for the dummy op 100 times"
    print "Server Time     Relay Time    Client Time"
    for i in range (1, 100):

        # start timer
        start_time = time.time ()
        
        # send dummy request
        resp = send_req (conn, "/dummy_op")

        # end timer
        end_time = time.time ()
        
        # recall that we will get a jsonified info from response
        # you could save the three results in a file that then you
        # can open in Excel etc to plot the graphs
        json_obj = json.loads (resp.read ())
        
        print json_obj['Orig']['time'], json_obj['Relay']['time'], (end_time - start_time)

    # sending a different kind of request. Here we send the autoscale
    # request.

    # @@@ Note @@@
    # I have not shown any code to start the second VM on the 3rd tier.
    # You should be including the IP addr of the 2nd VM on the 3rd tier
    # in this autoscale request so the client-facing server now has the
    # knowledge of the 2nd VM in the 3rd tier.
    
    print "Sending request for autoscale with RR"
    send_req (conn, "/autoscale?lb=RR")
    
    print "Sending request for autoscale with PD"
    send_req (conn, "/autoscale?lb=PD&ratio=1:4")

    # @@@ Note @@@
    # You could have additional method invocations here to clean things up
    # e.g., stopping the VMs on the 3rd tier and the client-facing server

    conn.close ()
    
# invoke main
if __name__ == "__main__":
    sys.exit (main ())
    
