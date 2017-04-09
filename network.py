import asyncio
import logging
import socket

class AsyncNetwork:
    PORT = 13337

    def __init__(self, evloop, nodeslist):
        self.evloop = evloop
        self.nodeslist = nodeslist

        # dict of nodes connected to
        self.alive = {}

    async def create_server(self):
        proto = TCPProtocol(self.evloop)

        self.server = await self.evloop.create_server(
            proto, port=AsyncNetwork.PORT, family=socket.AF_INET,
            reuse_address=True, reuse_port=True
        )
        logging.info('Created server...')

    def close(self):
        self.server.close()

class Node:
    def __init__(self):
        pass


class TCPProtocol(asyncio.Protocol):
    def __init__(self, evloop):
        self.evloop = evloop
        logging.info('Created protocol!')

    def __call__(self):
        return self

    def connection_made(self, transport):
        self.transport = transport
        self.peer = self.transport.get_extra_info('peername')
        logging.info('Got connection from {}'.format(str(self.peer)))

    def connection_lost(self, exc):
        logging.info('Connection lost with {}'.format(str(self.peer)))
        super().connection_lost(exc)

    def data_received(self, data):
        logging.info(f'Got from {self.peer[0]}: {data}')

    def eof_received(self):
        pass
