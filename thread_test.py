# !/bin/python

#
# Vanderbilt University Computer Science
# Author: Aniruddha Gokhale
# Course: CS4287-5287 Principles of Cloud Computing
# Created: Fall 2016
#
# Purpose: To demonstrate how threads can talk to each other. You will need
# something like this in your assignment code so that the runtime action
# to start the 3rd VM and initialize it etc can be handled concurrently
# in a separate thread so that your client thread that sends request to the
# server does not have to block until the VM has started
#
# 
# You may recognize this as the famous producer-consumer problem we study
# in a basic operating systems course.

# system and time
import os
import sys
import time

# shared data structure and threading
import Queue
import threading

# subclass from the threading.Thread
class MyThread (threading.Thread):
    # constructor
    def __init__(self, name, func, q):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.q = q

    # override the run method which is invoked by start
    def run (self):
        print "Starting " + self.name
        self.func (self.q)
        print "Exiting " + self.name

# logic for the producer thread
def producer (q):
    print ("producer thread")
    for i in range (1, 10):
        print "producer thread, inserting ", i
        q.put (i)
        time.sleep (1)
    print ("producer exit")
    
# logic for the consumer
def consumer (q):
    print ("consumer thread")
    for i in range (1, 10):
        print "Consumer thread, retrieving ", q.get ()
    print ("consumer exit")

# main function
def main ():

    # initialize an array of threads
    threads = []
    
    # first instantiate a Queue object
    q = Queue.Queue ()
    
    # here we start two threads: one producer, one consumer
    print ("main starting the two threads")
    t1 = MyThread ("Producer", producer, q)
    t2 = MyThread ("Consumer", consumer, q)

    t1.start ()
    t2.start ()

    # save the thread objects in our list
    threads.append (t1)
    threads.append (t2)

    # now wait for threads to exit
    print ("main waiting for the two threads to terminate")
    for t in threads:
        t.join ()

    # done
    print ("main program is over")
    
# invoke main
if __name__ == "__main__":
    sys.exit (main ())
    
