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

# import the database for persisting our data
import redislite
import redis_collections
rdb = redis_collections.Dict(redis=redislite.StrictRedis('example.rdb'))

# a queue to manage the servers
import Queue
serverqueue = Queue.Queue()

f = open('file.txt')
IP = f.read()
conn = httplib.HTTPConnection (IP, "8080")
serverqueue.put(conn)

f2 = open('file2.txt')
IP2 = f2.read()
conn2 = httplib.HTTPConnection (IP2, "8080")
serverqueue.put(conn2)

# Load balancing related stuff
Load_balance_enabled = False
A_server_req_count = 0
B_server_req_count = 0






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
    #print "Welcome to Assignment 1 relay Server! dope"
    print "extra swag"
    print "T3 S1: " + IP
    print "T3 S2: " + IP2

    server = get_server_conn()
    resp = send_req (server, request)

    print resp

    #return "hello world"

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
    server = get_server_conn()
    resp = send_req (server, request)

    # stop the timer
    end_time = time.time ()

    # let us get the json version of the reply coming from our main server
    resp_dict = json.loads (resp.read ())

    # encode our findings as a json object
    local_dict = {"op" : "dummy_op",
                  "server" : "Assign1_RelayServer",
                  "time" : end_time - start_time,
                  "final server": server.host}

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


    # pull out what kind of load balancing we want to do
    query = request.args

    if 'lb' in query:
        # there is a request to activate the load balancer
        strategy = query['lb']

        if strategy == 'RR':
            rdb['lb_scheme'] = 'RR'

            rdb['balancing_enabled'] = True
            lb_status = "The server has successfully been set to a Round Robin load-balancing scheme!"

        elif strategy == 'PD':
            rdb['lb_scheme'] = 'RR'
            rdb['conn1_max_val'] = 1
            rdb['conn2_max_val'] = 2

            rdb['balancing_enabled'] = True
            lb_status = "The server has successfully been set to a Proportional Dispatch load-balancing scheme!"

        else:
            lb_status = "Invalid load-balancing strategy specified"
        print lb_status
        return lb_status
    else:
        # there is not a request for load balancing
        lb_status = 'No load balancing parameter specified'
        print lb_status
        return lb_status


    IP
    this.fdsa = Load_balance_enabled






    print "Relay Server: relaying autoscale request %s" % request
    resp = send_req (conn, request)

    # simply relay the response (note that the read method reads the content)
    return resp.read ()


# A route designed to return simple info about the state of the appp
@app.route("/status")
def status ():

    if 'count' in rdb:
        rdb['count'] += 1
    else:
        print 'Current keys: \n' + str(rdb.keys())
        rdb['count'] = 0
    return 'The current count is ' + str(rdb['count'])


# This function launches a new server
def launch_server ():
    f = 9


# This function returns a server connection to handle a request
def get_server_conn ():

        if 'balancing_enabled' not in rdb or rdb['balancing_enabled'] == False:
            # return the first server regardless
            return conn
        elif rdb['lb_scheme'] == 'RR':
            # pop the first server and put it at the end of the queue
            server_connection = serverqueue.get()
            serverqueue.put(server_connection)
            return server_connection
        elif rdb['lb_scheme'] == 'PD':
            # proportional distribution at a rate of 1:2 requests for the servers
            while true:
                # traverse the order available server connections
                if rdb['conn1_count'] > 0:
                    rdb['conn1_count'] -= 1
                    print 'Relayed to conn1, new count: ' + str(rdb['conn1_count'])
                    return conn

                elif rdb['conn2_count'] >0:
                    rdb['conn2_count'] -= 1
                    print 'Relayed to conn2, new count: ' + str(rdb['conn2_count'])
                    return conn2

                else:
                    # reset the values and start over
                    rdb['conn1_count'] = rdb['conn1_max_val']
                    rdb['conn2_count'] = rdb['conn2_max_val']


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

