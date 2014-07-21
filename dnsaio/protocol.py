"""
    Asyncio protocol for dns
"""

import asyncio
import logging
import struct

import dns.message


logger = logging.getLogger(__name__)

class DnsProtocol(asyncio.StreamReaderProtocol):
    """
        Common code for our node<>pop connexion protocol

    """
    def __init__(self, *args, **kwargs):
        super().__init__(asyncio.StreamReader(), self.client_connected)
        self.open = True

    def connection_made(self, transport):
        super().connection_made(transport)
        logger.info("New tcp connection")
        self.open = True

    def connection_lost(self, exc):
        super().connection_lost(exc)
        self.open = False
        logger.warning("we lost the connexion sir %s", str(exc))

    def eof_received(self):
        super().eof_received()
        self.open = False

    def client_connected(self, reader, writer):
        self.reader = reader
        self.writer = writer

    @asyncio.coroutine
    def read_frame(self, query):
        """
            Read a DNS frame
        """
        wire_length_p = yield from self.reader.readexactly(2)
        (payload_length, ) = struct.unpack('!H', wire_length_p)
        payload = yield from self.reader.readexactly(payload_length)
        return payload

    @asyncio.coroutine
    def write_wire(self, wire):
        wire_len = len(wire)
        wire_len_p = struct.pack('!H', wire_len)
        self.writer.write(wire_len_p)
        self.writer.write(wire)
        print(wire)
        yield from self.writer.drain()

    @asyncio.coroutine
    def query(self, query, one_rr_per_rrset=False):
        wire = query.to_wire()
        yield from self.write_wire(wire)

        response = (yield from self.read_frame(wire))
        r = dns.message.from_wire(
            response,
            keyring=query.keyring,
            request_mac=query.mac,
            one_rr_per_rrset=one_rr_per_rrset
        )
        return r