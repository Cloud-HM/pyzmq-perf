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


def remote_thr(url, count, size, copy, poll):
    """send a bunch of messages on a PUSH socket"""
    ctx = zmq.Context()
    s = ctx.socket(zmq.PUSH)

    #  Add your socket options here.
    #  For example ZMQ_RATE, ZMQ_RECOVERY_IVL and ZMQ_MCAST_LOOP for PGM.

    if poll:
        p = zmq.Poller()
        p.register(s)

    s.connect(url)

    msg = zmq.Message(b' ' * size)
    block = zmq.NOBLOCK if poll else 0

    for i in range(count):
        if poll:
            res = p.poll()
            assert (res[0][1] & zmq.POLLOUT)
        s.send(msg, block, copy=copy)

    s.close()
    ctx.term()


def main():
    args = parse_args()

    print ("Running program...")
    tic = time.time()
    remote_thr(args.url, args.count, args.size, args.poll, args.copy)
    toc = time.time()

    if (toc - tic) < 3:
        print ("For best results, tests should take at least a few seconds.")


if __name__ == '__main__':
    main()
