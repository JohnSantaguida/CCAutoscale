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

# server create module
from nova_server_create import create, connect
import subprocess as sp

# threading for launching all servers
import threading

# Function takes a shell command as a string and executes it using a subprocess
def remote_cmd(args):
    try:
        p = sp.Popen (args, shell=True)
        retcode = p.wait ()
        print 'Subprocess exited with status: ', retcode
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

# Prints the contents of an HTTP response, useful for debugging
def print_response(resp):
    print "printing response headers"
    try:
        for hdr in resp.getheaders():
            print hdr
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    print "printing received data"
    try:
        data = resp.read()
        print "Length of data = ", len(data)
        print data
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

# Send a http request to the server.
def send_req(conn, arg):

    # send GET request to the server using the args
    try:
        conn.request("GET", arg)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # retrieve the response
    try:
        resp = conn.getresponse()
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    return resp

# These three functions execute all the necessary shell code to configure the specified server (packages etc)
def config_tier_2(tier_2_IP, project_path):

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(tier_2_IP) + ' sudo apt-get -y update'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(tier_2_IP) + ' sudo apt-get -y install python-dev python-pip'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(tier_2_IP) + ' sudo python -m pip install flask'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(tier_2_IP) + ' sudo python -m pip install redislite'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(tier_2_IP) + ' sudo python -m pip install redis_collections'
    remote_cmd(args)

    args = 'scp -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ' + project_path + '/assign1_relay_server.py ubuntu@' + str(tier_2_IP) + ':/home/ubuntu/'
    remote_cmd(args)

    args = 'scp -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ~/.ssh/santaguida.pem ubuntu@' + str(tier_2_IP) + ':/home/ubuntu/'
    remote_cmd(args)

    args = 'scp -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ' + project_path + '/assign1_server_skel.py ubuntu@' + str(tier_2_IP) + ':/home/ubuntu/'
    remote_cmd(args)

    args = 'scp -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ' + project_path + '/file.txt ubuntu@' + str(tier_2_IP) + ':/home/ubuntu/'
    remote_cmd(args)

def config_tier_3_1(tier_3_1_IP, relay_external_IP):
    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(tier_3_1_IP) + ' sudo apt-get -y update'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(tier_3_1_IP) + ' sudo apt-get -y install python-dev python-pip'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(tier_3_1_IP) + ' sudo python -m pip install flask'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(tier_3_1_IP) + ' sudo python -m pip install numpy'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(tier_3_1_IP) + ' sudo apt-get install stress'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' scp -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem /home/ubuntu/assign1_server_skel.py ubuntu@' + str(tier_3_1_IP) + ':/home/ubuntu'
    remote_cmd(args)

def config_tier_3_2(tier_3_2_IP, relay_external_IP):
    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(tier_3_2_IP) + ' sudo apt-get -y update'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(tier_3_2_IP) + ' sudo apt-get -y install python-dev python-pip'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(tier_3_2_IP) + ' sudo python -m pip install flask'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(tier_3_2_IP) + ' sudo python -m pip install numpy'
    remote_cmd(args)

    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' scp -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem /home/ubuntu/assign1_server_skel.py ubuntu@' + str(tier_3_2_IP) + ':/home/ubuntu'
    remote_cmd(args)


# These functions invoke the flask webserver in the already configured servers
def launch_flask_tier_2(relay_external_IP):
    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' env FLASK_APP=assign1_relay_server.py python -m flask run --host=0.0.0.0 --port=8080'
    remote_cmd(args)

def launch_flask_tier_3(host_server_IP, relay_external_IP):
    args = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ubuntu@' + str(relay_external_IP) + ' ssh -o StrictHostKeyChecking=no -i /home/ubuntu/santaguida.pem ubuntu@' + str(host_server_IP) + ' env FLASK_APP=assign1_server_skel.py python -m flask run --host=0.0.0.0 --port=8080'
    remote_cmd(args)


# ***** Begin threading stuff *****
def launch_all_flask_servers(relay_external_IP, tier_3_1_IP, tier_3_2_IP):
    # initialize an array of threads
    threads = []

    print "Launching flask on all servers using independent threads"

    # create the threads
    relay_thread = MyThread("Relay Server", launch_flask_tier_2(relay_external_IP), relay_external_IP)
    tier_3_1_thread = MyThread("Tier 3_1 Server", launch_flask_tier_3(tier_3_1_IP, relay_external_IP), tier_3_1_IP)
    tier_3_2_thread = MyThread("Tier 3_2 Server", launch_flask_tier_3(tier_3_2_IP, relay_external_IP), tier_3_2_IP)


    # actually launch the threads
    print "Thread 1: Launching"
    relay_thread.start()
    print "Thread 1: Running"
    print "Thread 2: Launching"
    tier_3_1_thread.start()
    print "Thread 2: Running"
    print "Thread 3: Launching"
    tier_3_2_thread.start()
    print "Thread 3: Running"

    print "All server-launching threads have begun execution"

    return  # The code below is useful but unnecessary for this application
    # threads.append(relay_thread)
    # threads.append(tier_3_1_thread)
    # threads.append(tier_3_2_thread)
    #
    # # now wait for threads to exit
    # print ("main waiting for the two threads to terminate")
    # for t in threads:
    #     t.join()
    #
    # # done
    # print ("All connections to flask servers have been lost")

class MyThread (threading.Thread):
    # constructor
    def __init__(self, name, func, args=()):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        #self.IP = IP

        self.daemon = True

    # override the run method which is invoked by start
    def run (self):
        print self.name + ': Launching'
        #self.func(self.IP)
        self.func
        print self.name + ': Running'
# ****** End threading stuff ******







# main: In this sample code, we send a few requests:
# first a simple http message to the web server's main page and
# then the dummy_op request multiple times, an autoscale request with
# round robin policy, and finally an autoscale request with the proportional
# dispatch policy along with the ratio in which subsequent requests are
# going to be handled
def main ():

    # Use this variable to set the home directory where all the project files are located
    # project_path = '/home/cloud/assgn1/proj/CCAutoscale'
    project_path = '/media/sf_cloud_computing/Assignments/CCAutoscale'

    #Specify the Floating IP for accessing the 2nd tier VM
    relay_external_IP = "129.59.107.47"
    #relay_external_IP = "129.59.107.207"
    print "floating ip is " + relay_external_IP
    print "Instantiating a connection obj"


    # Debugging - use when a the script crashes and you want to resume arbitrarily
    # connect()
    # tier_3_1_IP = open('file2.txt').readline()
    # tier_3_2_IP = open('file.txt').readline()


    #This block creates the 2nd tier VM and the first 3rd tier VM
    name = 'jspm_tier2'
    print "creating server: " + name
    create(name, relay_external_IP)
    print name + " created"

    name = 'jspm_tier3_1'
    print "creating server: " + name
    tier_3_1_IP = create(name)

    f = open( 'file.txt', 'w' )
    f.write(tier_3_1_IP)
    f.close()

    print name + " created"
    print "Tier 3 IP address: " + str(tier_3_1_IP) #- hardcode for debugging
    try:
        # @@@ NOTE @@@
        # if you are trying this locally, use this and by using
        # 8081, I am sending to the relay server
#        conn = httplib.HTTPConnection ("localhost", "8081")
#        conn = httplib.HTTPConnection ("localhost", "8080")

        # if you try this to talk to your server which has a floating IP,
        # then you use the following and parametrize it with the
        # actual floating IP
        conn = httplib.HTTPConnection (relay_external_IP, "8080")
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise


    # I moved the SSH commands to their own methods
    # Set up tier 2 VM
    config_tier_2(relay_external_IP, project_path)

    #Setup tier 3_1 VM
    config_tier_3_1(tier_3_1_IP, relay_external_IP)

    name = 'jspm_tier3_2'
    print "creating server: " + name
    tier_3_2_IP = create(name)

    f2 = open( 'file2.txt', 'w' )
    f2.write(tier_3_2_IP)
    f2.close()

    time.sleep(30)#MAYBE NO THERE

    args = 'scp -o StrictHostKeyChecking=no -i ~/.ssh/santaguida.pem ' + project_path + '/file2.txt ubuntu@' + str(relay_external_IP) + ':/home/ubuntu/'
    remote_cmd(args)
    print name + " created"
    print "Tier 3 second IP address: " + str(tier_3_2_IP) # - hardcode for debugging


    #Setup tier 3_2 VM
    config_tier_3_2(tier_3_2_IP, relay_external_IP)

    # launch the flask webserver applications on the servers
    launch_all_flask_servers(relay_external_IP, tier_3_1_IP, tier_3_2_IP)



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
#    print "Sending request for the dummy op 100 times"
#    print "Server Time     Relay Time    Client Time"
#    for i in range (1, 100):

        # start timer
#        start_time = time.time ()

        # send dummy request
#        resp = send_req (conn, "/dummy_op")

        # end timer
#        end_time = time.time ()

        # recall that we will get a jsonified info from response
        # you could save the three results in a file that then you
        # can open in Excel etc to plot the graphs
#        json_obj = json.loads (resp.read ())

#        print json_obj['Orig']['time'], json_obj['Relay']['time'], (end_time - start_time)

    # sending a different kind of request. Here we send the autoscale
    # request.

    # @@@ Note @@@
    # I have not shown any code to start the second VM on the 3rd tier.
    # You should be including the IP addr of the 2nd VM on the 3rd tier
    # in this autoscale request so the client-facing server now has the
    # knowledge of the 2nd VM in the 3rd tier.
    #Block dealing with creating second third tier VM






#hjg;luihf'wjg'e
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
