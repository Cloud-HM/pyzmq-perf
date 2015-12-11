import argparse


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Run a zmq performance test')
    parser.add_argument('-p', '--poll', action='store_true',
                        help='use a zmq Poller instead of raw send/recv')
    parser.add_argument('-c', '--copy', action='store_true',
                        help='copy messages instead of using zero-copy')
    parser.add_argument('-s', '--size', type=int, default=10240,
                        help='size (in bytes) of the test message')
    parser.add_argument('-n', '--count', type=int, default=10240,
                        help='number of test messages to send')
    parser.add_argument('--url', dest='url', type=str, default='tcp://127.0.0.1:5555',
                        help='the zmq URL on which to run the test')
    return parser.parse_args(argv)
