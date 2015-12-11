#!/usr/bin/env python
# coding: utf-8

# Copyright (C) PyZMQ Developers
# Distributed under the terms of the Modified BSD License.
#
#  Some original test code Copyright (c) 2007-2010 iMatix Corporation,
#  Used under LGPLv3

import time

import zmq

from parse_args import parse_args


def local_thr(url, count, size, poll, copy):
    """recv a bunch of messages on a PULL socket
    
    Should be started before `pusher`
    """
    ctx = zmq.Context()
    s = ctx.socket(zmq.PULL)

    #  Add your socket options here.
    #  For example ZMQ_RATE, ZMQ_RECOVERY_IVL and ZMQ_MCAST_LOOP for PGM.

    if poll:
        p = zmq.Poller()
        p.register(s)

    s.bind(url)

    watch = zmq.Stopwatch()
    block = zmq.NOBLOCK if poll else 0

    # Wait for the other side to connect.
    msg = s.recv()
    assert len(msg) == size

    watch.start()
    for i in range(count - 1):
        if poll:
            res = p.poll()
        msg = s.recv(block, copy=copy)
    elapsed = watch.stop()
    if elapsed == 0:
        elapsed = 1

    throughput = (1e6 * float(count)) / float(elapsed)
    megabits = float(throughput * size * 8) / 1e6

    print ("message size   : %8i     [B]" % (size,))
    print ("message count  : %8i     [msgs]" % (count,))
    print ("mean throughput: %8.0f     [msg/s]" % (throughput,))
    print ("mean throughput: %12.3f [Mb/s]" % (megabits,))
    print ("test time      : %12.3f [s]" % (elapsed * 1e-6,))


def main():
    args = parse_args()

    print ("Running program...")
    tic = time.time()
    local_thr(args.url, args.count, args.size, args.poll, args.copy)
    toc = time.time()

    if (toc - tic) < 3:
        print ("For best results, tests should take at least a few seconds.")


if __name__ == '__main__':
    main()
