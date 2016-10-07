#!/bin/python
#
# Vanderbilt University Computer Science
# Author: Aniruddha Gokhale
# Course: CS4287-5287 Principles of Cloud Computing
# Created: Fall 2016
#
# Purpose: To provide a skeleton to implement the relay server, i.e., it
# serves as the client-facing server accepting requests from the client,
# but in turn relaying it to our 3rd tier VM. It must also relay any
# responses back to the server.
#
# Flask API is described here: http://flask.pocoo.org/docs/0.11/api/

# import system headers
import sys

# because this is a relay server, we also don the role of a client and
# need this library
import httplib

# import timer stuff to record the time
import time

# import the Flask class
from flask import Flask
from flask import request
from flask import json


# the following instance of the Flask class will act as the
# WSGI (web server gateway interface) application
app = Flask (__name__)

# @@@ Note @@@
# I have not found a better way to initialize a conn variable
# as a global variable to something like nothing and then later
# initialize it to the right connection we want. So for now
# the connection is established here. Change it to the IP addr of
# the 3rd tier VM.
f2 = open('file2.txt')
IP2 = f2.read()
conn2 = httplib.HTTPConnection (IP2, "8080")

f = open('file.txt')
IP = f.read()
conn = httplib.HTTPConnection (IP, "8080")



# print the response (for debugging purposes only)
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
        print "Actual Data = ", data
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

# send a http request to the real server.
def send_req (conn, req):
    try:
        # I have to use this logic because for the autoscale operation,
        # we also have a query string starting with the ? sign
        payload = req.path
        if (req.query_string):
            payload = payload + "?" + req.query_string

        # now send the request
        conn.request (req.method, payload)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # receive a response from the other side. Note, in this case we
    # have relayed the request to the real server and we now expect
    # a response from the real server
    try:
        resp = conn.getresponse ()
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # for debugging
    # print_response (resp)

    # return the response to the caller
    return resp

# the @app.route is a decorator telling flask how to route the incoming
# http web request

# Note that each route method below by default is handling a GET request
# If we were to handle other methods, then we will need the methods =
# approach

# The following is a top level request. It just returns a welcome message
@app.route("/")
def welcome ():
    print "Welcome to Assignment 1 relay Server!"
    resp = send_req (conn, request)

    # simply relay the response (note that the read method reads the content)
    return resp.read ()

# The following is to handle an incoming request for the dummy operation
# which is supposed to relay it to our 3rd tier VM according to the load
# balancing strategy
@app.route("/dummy_op")
def dummy_op ():
    # you should be relaying the request to the 3rd tier according to
    # the LB strategy. Moreover, not only that, but you need to time the
    # request and reply the original client with the measured time
    #
    # If you expect to relay a param, that param must be received via
    # the http request. See autoscale method to see how we receive a param

    # start timer so we can time how much is the response time at the
    # relay server
    start_time = time.time ()

    # relay the request
    resp = send_req (conn, request)

    # stop the timer
    end_time = time.time ()

    # let us get the json version of the reply coming from our main server
    resp_dict = json.loads (resp.read ())

    # encode our findings as a json object
    local_dict = {"op" : "dummy_op",
                  "server" : "Assign1_RelayServer",
                  "time" : end_time - start_time}

    # Now combine the two json objects
    combined_dict = {"Orig" : resp_dict,
                     "Relay" : local_dict}

    # the dumps method converts the json obj to a string. We return this string
    # which is internally converted by Flask into a response object before
    # sending it out to the client
    return json.dumps (combined_dict)

# The following is to handle an incoming request for autoscaling and the
# suggested policy
@app.route("/autoscale")
def autoscale ():
    # @@@ NOTE @@@
    # here you should handle the autoscaling policy and take the steps
    # to start a new 3rd tier VM that will run the same code as the other VM.
    # You should also set the LB policy (round robin or proportional)

    # We expect the incoming request of the form
    # http://IPAddr/autoscale?lb=RR or
    # http://IPAddr/autoscale?lb=PD&ratio=1:5
    #
    # where RR = round robin (1:1 ratio implied),
    #       PD = proportional dispatch with ratio specified in the next param

    # @@@ Note @@@
    # In this dummy code, I am just relaying this to the 3rd tier but this
    # is not what you should do
    print "Relay Server: relaying autoscale request %s" % request
    resp = send_req (conn, request)

    # simply relay the response (note that the read method reads the content)
    return resp.read ()

def main ():
    # @@@ NOTE @@@
    # because I am testing this code on my laptop Ubuntu VM, I cannot reuse
    # port 8080 for both the 3rd tier server and 2nd tier relay server because
    # both are on the same host. That will not be the case on horizon VM
    # because each server will be running in their own VMs and so have their
    # own hostnames and port ranges.
    #
    # Thus, for the assignment, you can make this 8080. You can remove the
    # debug flag.
    print ("Starting the Relay Server")
    app.run (host="0.0.0.0", port= 8080)
    
if __name__ == "__main__":
    sys.exit (main ())

