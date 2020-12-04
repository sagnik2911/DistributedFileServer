import hashlib
import pickle, logging
import sys
import xmlrpc.client

from memoryfs_client import BLOCK_SIZE, TOTAL_NUM_BLOCKS, RSM_LOCKED

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class DiskBlocks():
    def __init__(self):
        # This class stores the raw block array
        self.block = []
        self.checksum = []
        # Initialize raw blocks
        for i in range(0, TOTAL_NUM_BLOCKS):
            putdata = bytearray(BLOCK_SIZE)
            self.block.insert(i, putdata)
            self.checksum.insert(i, hashlib.md5(putdata).digest())


if __name__ == "__main__":

    RawBlocks = DiskBlocks()

    totalarguments = len(sys.argv)
    port_number = int(sys.argv[1])

    corrupted_blocks = []
    for i in range(2, totalarguments):
        corrupted_blocks.append(int(sys.argv[i]))

    # Create server
    server = SimpleXMLRPCServer(("localhost", port_number), requestHandler=RequestHandler)


    def Get(block_number):
        result = RawBlocks.block[block_number]
        # Server is initialized with bytearray of zeros, no need to check checksum as data is not relevant
        if isinstance(result, bytearray):
            return result
        if RawBlocks.checksum[block_number] != hashlib.md5(result.data).digest():
            return -1
        return RawBlocks.block[block_number]


    server.register_function(Get)


    def Put(block_number, data):
        RawBlocks.block[block_number] = data
        # store checksum only when it's not a corrupted block
        if block_number not in corrupted_blocks:
            RawBlocks.checksum[block_number] = hashlib.md5(data.data).digest()
        return 0


    server.register_function(Put)


    def RSM(block_number):
        result = RawBlocks.block[block_number]
        RawBlocks.block[block_number] = RSM_LOCKED
        # RawBlocks.block[block_number] = bytearray(RSM_LOCKED.ljust(BLOCK_SIZE,b'\x01'))
        return result


    server.register_function(RSM)

    # Run the server's main loop
    server.serve_forever()
