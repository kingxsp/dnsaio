"""
    Simple script to update a DDNS record

"""
import asyncio
import sys

from dnsaio import protocol as dns_protocol

import dns.update
import dns.query
import dns.tsigkeyring


@asyncio.coroutine
def query(transport, protocol):
    keyring = dns.tsigkeyring.from_text({
        'key' : 'secret=='
    })

    zone = 'zone.example.com'
    host = sys.argv[1]
    address = sys.argv[2]
    update = dns.update.Update(zone, keyring=keyring)
    update.replace(host, 300, 'AAAA', address)

    return (yield from protocol.query(update))

def main():
    loop = asyncio.get_event_loop()

    transport, protocol = loop.run_until_complete(
        loop.create_connection(
            dns_protocol.DnsProtocol,
            host='localhost',
            port=53,
        )
    )

    data = loop.run_until_complete(query(transport, protocol))

if __name__ == '__main__':
    main()
