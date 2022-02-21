#!/usr/bin/env python
import asyncio

class Network:
    """
    Class which handles the Scrabble network game protocol.
    """
    def __init__(self, host, port, on_client_connect=None):
        self.host = host
        self.port = port

        self.clients = None
        self.local_client = None

        self.on_client_connect = on_client_connect

        self.loop = asyncio.get_event_loop()

    def __del__(self):
        if self.clients:
            # Cleanup all client connections if the server.
            for _, v in self.clients.items():
                v[1].close()  # Close the writer socket.

        if self.local_client:
            # Cleanup connection to the server if the client.
            self.local_client[1].close()

    async def server(self, reader, writer):
        """
        Called when a new client connects to the server.
        """
        client_address = writer.get_extra_info('peername')
        if not self.clients:
            self.clients = {}

        self.clients[client_address] = (reader, writer)

        # Notify our creator that a new client has established a connection.
        if callable(self.on_client_connect):
            self.on_client_connect(client_address)

    def set_display_name(self, name):
        """
        Tells the server your new display name.
        """
        if self.local_client:
            self.local_client[1].write(f'NAME {name}\n'.encode())

    def establish_connection(self):
        """
        Establish a connection to an existing server.
        """
        async def connect():
            self.local_client = await asyncio.open_connection(self.host, self.port, loop=self.loop)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(connect())

    def start_hosting(self):
        """
        Create a new server to allow other clients to connect to it.
        """
        host = self.loop.run_until_complete(
            asyncio.start_server(self.server, self.host, self.port, loop=self.loop)
        )

        self.loop.run_forever()

        # Cleanup
        host.close()
        self.loop.run_until_complete(host.wait_closed())
        self.loop.close()
