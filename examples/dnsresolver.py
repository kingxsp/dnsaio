"""
    Example to use dnspython3 when trying to resolve an address
"""
import asyncio
import sys

from dnsaio import protocol as dns_protocol

import dns.name
import dns.message


def query(transport, protocol):
    qname = dns.name.from_text(sys.argv[1])
    record_type = dns.rdatatype.from_text('MX')
    rdclass = dns.rdataclass.from_text('IN')
    request = dns.message.make_query(qname, record_type, rdclass)
    return (yield from protocol.query(request))

def main():
    loop = asyncio.get_event_loop()

    transport, protocol = loop.run_until_complete(
        loop.create_connection(
            dns_protocol.DnsProtocol,
            host='8.8.8.8',
            port=53,
        )
    )

    response = loop.run_until_complete(query(transport, protocol))
    print(response.to_text())
    
if __name__ == '__main__':
    main()
