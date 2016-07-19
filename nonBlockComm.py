#!/usr/bin/env python
"""
 testing mpi4py stuff
"""

from mpi4py import MPI
import numpy as np
import math
import time

#from vtkHelper import saveVelocityAndPressureVTK_binary as writeVTK
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print "hello from rank %d of %d" % (rank, size)

buffSize = 5;
ngb_to_1 = (rank+1)%size # who I am sending to
ngb_to_2 = (rank+2)%size

ngb_from_1 = (rank - 1) % size #who I am recieving from 
ngb_from_2 = (rank - 2) % size

data_out = np.ones([buffSize],dtype=np.float32)*rank;
data_in = np.empty([2,buffSize],dtype=np.float32);

out_requests = [MPI.REQUEST_NULL for i in range(2)] #where is this documented?
in_requests = [MPI.REQUEST_NULL for i in range(2)]

statuses = [MPI.Status() for i in range(2)] # where is this documented?

# initiate Isend to neighbors
out_requests[0] = comm.Isend([data_out[:],buffSize,MPI.FLOAT],ngb_to_1,rank)
out_requests[1] = comm.Isend([data_out[:],buffSize,MPI.FLOAT],ngb_to_2,rank)

# initiate Irecv to get neighbor data
in_requests[0] = comm.Irecv([data_in[0,:],buffSize,MPI.FLOAT],ngb_from_1,MPI.ANY_TAG)
in_requests[1] = comm.Irecv([data_in[1,:],buffSize,MPI.FLOAT],ngb_from_2,MPI.ANY_TAG)


# wait for any extra crap to get done....
MPI.Request.Waitall(in_requests,statuses)

print "rank %d received data %s from %d " % (rank, str(data_in[0,:]), ngb_from_1)
print "rank %d received data %s from %d " % (rank, str(data_in[1,:]), ngb_from_2)

