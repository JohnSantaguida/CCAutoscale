#!/usr/bin/env python

# Institution: Vanderbilt University
# Code created for the CS4287-5287 course
# Author: Aniruddha Gokhale
# Created: Fall 2015
# Modified: Fall 2016
#
# The purpose of this code is to show how to create a server using the nova API.
# We use this as a package file without a main function so that we can import
# it from 

# import the system basic files
import os
import sys
import time

# import the openstack nova project
from novaclient.v2 import client

# See http://docs.openstack.org/developer/python-novaclient/index.html
# for Python to nova reference
#
# Other references: http://developer.openstack.org/api-ref-compute-v2.1.html
#
# See example at http://docs.openstack.org/user-guide/sdk_compute_apis.html

# get our credentials from the environment variables. Note that we
# use the same names for the indexes as those needed by the parameters
# in the connection request
def get_nova_creds ():
    d = {}
    d['version'] = '2'  # because we will be using the version 2 of the API
    # The rest of these are obtained from our environment. Don't forget
    # to do "source cloudclass-rc.sh" or whatever is the name of your rc file
    #
    d['region_name'] = os.environ['OS_REGION_NAME']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    d['tenant_id'] = os.environ['OS_TENANT_ID']
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    return d

# create a connection to the cloud using our credentials
def create_connection (creds):
    # Now access the connection from which everything else is obtained.
    try:
        nova = client.client.Client (**creds)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    return nova

# create a vm instance on the cloud. I am hardcoding attribute values
# of my created VM. If you desire, you can pass them as parameters
def create_server (myName, nova):
    #  creating a server needs the "create_server" function on the compute
    # object. To do that we must first create a key-value dictionary of
    # the server's attributes
    #
    # To do that we must first retrieve the UUIDS for various attributes

    # this is the image type we are going to create. 
    imageref = nova.images.find (name="ubuntu-14.04")
    print ("imageref = ", imageref)
    
    # this is the flavor type we are going to use
    flavorref = nova.flavors.find (name="m1.small")
    print ("flavorref = ", flavorref)

    # this is the security group we will belong to
    sgref = nova.security_groups.find (name="default")
    print ("sec group = ", sgref)
    
    # for some reason, this is not working.
    # netref = nova.networks.find (name="networks")
    # print ("net ref = ", netref)
    
    attrs = {
        'name' : myName,  # put your vm name
        'image' : imageref,
        'flavor' : flavorref,
        # providing the ref this way for security group is not working
        #'security_groups' : sgref,
        'key_name' : 'santaguida', # put your key name
        # I was going to do the following but does not work
        # 'nics' : [{'net-id' : netref.id}]
        # So I had to copy-paste as below the ID of the internal n/w
        'nics' : [{'net-id' : 'b16b0244-e1b5-4d36-90ff-83a0d87d8682'}]
        }

    try:
        server = nova.servers.create (**attrs)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # we need to check if server is up
    while (server.status != 'ACTIVE'):
        print "Not active yet; sleep for a while; Name = " + myName 
        time.sleep (2)
        # we need to retrieve the status of the server from
        # the restful API (it does not get updated dynamically in the
        # server object we have)
        server = nova.servers.find (name=myName)

    print ("Server is now running")
    return server

# assign a floating IP address
def assign_floating_ip (server, ip):
    # you should cycle through the floating ips and choose the one that is not
    # taken by someone yet. For now we are hardcoding it but should be
    # parametrized

    print "Adding floating IP"
    try:
        server.add_floating_ip (address=ip)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        server.delete ()
        raise

    return server

# main
def create (name, ip=""):
    
    # get our credentials for version 2 of novaclient
    creds = get_nova_creds()

    # create a connection to the cloud using our credentials
    nova = create_connection (creds)

    # create server
    server = create_server (name, nova)
	
    # assign floating IP
    if ip != "":
	assign_floating_ip (server, ip)
    else:
	return server.networks.get('internal network')[0]
    
# invoke main
if __name__ == "__main__":
    sys.exit (main ())
    
