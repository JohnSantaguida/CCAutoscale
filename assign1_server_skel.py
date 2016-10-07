#!/bin/python
#
# Vanderbilt University Computer Science
# Author: Aniruddha Gokhale
# Course: CS4287-5287 Principles of Cloud Computing
# Created: Fall 2016
#
# Purpose: To provide a skeleton to implement the client-facing server
# that handles incoming request types.
#
# In particular, we handle the request to perform the dummy operation on
# the backend (3rd tier) VM. We also handle the request to autoscale and
# the strategy to be used to handle the load balancing
#
# Flask API is described here: http://flask.pocoo.org/docs/0.11/api/

# import system headers
import sys

# import timer stuff to record the time
import time

# number crunching
import numpy as np
from numpy import linalg

# import the Flask class
from flask import Flask
from flask import request
from flask import json

# the following instance of the Flask class will act as the
# WSGI (web server gateway interface) application
app = Flask(__name__)

# the @app.route is a decorator telling flask how to route the incoming
# http web request

# Note that each route method below by default is handling a GET request
# If we were to handle other methods, then we will need the methods = 
# The following is a top level request. It just returns a welcome message
@app.route("/")
def welcome ():
    return "Welcome to Assignment 1 Server!"

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
    print "dummy_op"
    start_time = time.time ()

    # @@@@ NOTE @@@
    # this kind of logic which I have shown below should in fact be
    # executed on the 3rd tier server
    #
    # What am I doing below ?
    # We create an array of 1200x1200 and take its inverse. I am observing
    # around 5 secs to get this work done. For 2000x2000, I got around 24 secs.
    # I tried 5000x5000 but it seemed like it was never ending :-) so I gave up
    # I think a 5 sec resp time is good enough. With the machine getting loaded
    # the resp time should shoot up for our client to maybe double what we see.
    #
    # try some large dimensions of the matrix that runs for 5 or so secs
    arr = np.random.random ((2000,2000))
    arr_inv = linalg.inv (arr)
    
    end_time = time.time ()

    # @@@ NOTE @@@
    # Here I am returning a message and the time it took.
    # On receipt of this time, the client should decide if the deviation
    # from historic resp time is greater than some percent, say 20%, in
    # which case, the client should invoke autoscale with the
    # appropriate strategy
    
    # My goal is to encode the response as a json-ified structure
    resp_dict = {"op" : "dummy_op",
                 "server" : "Assign1_Server",
                 "time" : end_time - start_time}

    # dumps converts the json obj to a string. When we return it, Flask will
    # convert it to a response object before actually sending it out.
    return json.dumps (resp_dict)

# The following is to handle an incoming request for autoscaling and the
# suggested policy
@app.route("/autoscale")
def autoscale ():

    # @@@ NOTE @@@
    #
    # Technically, the 3rd tier server should not be handling an autoscale
    # request. In this sample code, I am just relaying everything from
    # the relay server to this server. By doing so, I can try the client
    # talking directly to this server without a relay server.
    
    # @@@ NOTE @@@
    # here you should handle the autoscaling policy and take the steps
    # to start a new 3rd tier VM that will run the same code as the other VM.
    # You should also set the LB policy (round robin or proportional)

    # We expect the incoming request of the form
    # http://IPAddr/autoscale?lb=RR or
    # http://IPAddr/autoscale?lb=PD&ratio=1:5
    #
    else:
    # where RR = round robin (1:1 ratio implied),
    #       PD = proportional dispatch with ratio specified in the next param

    print "Autoscale: Received request = %s" % request  
    
    ret_msg = "Welcome to Assignment 1 Server: autoscale! "
    # make sure that the load balancing strategy is mentioned
    if 'lb' in request.args:
        if request.args['lb'] == "RR":
            print "Round robin"
            ret_msg += "Round Robin specified"
        elif request.args['lb'] == "PD":  
            print "proportional dispatch"
            ret_msg += "Proportional Dispatch specified, "
        else:
            print "unrecognized lb"
            ret_msg += "Unrecognized lb policy"
    else:
        ret_msg += "Request must provide at least the lb parameter"
        return ret_msg

    if request.args['lb'] == "PD":
        if 'ratio' in request.args: # expect the ration arg
            ret_msg += "Ratio = "
            ret_msg += request.args['ratio']
        else:
            ret_msg += "Ratio expected for proportional dispatch"
        
    return ret_msg

# main function
if __name__ == "__main__":

    # @@@ NOTE @@@
    # As part of the initialization, you should start the first
    # 3rd tier VM so that subsequent requests to this front tier
    # server will be relayed to this 3rd tier VM where
    # the code such as the one I showed in dummy_op will be executed
    
    app.run ()
