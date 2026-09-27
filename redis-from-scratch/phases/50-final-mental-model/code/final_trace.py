#!/usr/bin/env python3
def print_complete_command_journey():
    print("""
========================================================================================
             THE COMPLETE LIFE CYCLE OF: redis-cli SET user:42 Tushar
========================================================================================

[ 1. User Terminal ]
     └── User types: redis-cli SET user:42 Tushar

[ 2. redis-cli Process ]
     └── Formats arguments into binary-safe RESP bytes:
         *3\r\n$3\r\nSET\r\n$7\r\nuser:42\r\n$6\r\nTushar\r\n

[ 3. Operating System Network Stack ]
     └── Client writes bytes to TCP socket FD -> Kernel TCP/IP packet framing -> NIC

[ 4. Network Transport ]
     └── Traverses loopback / Ethernet / Switch (0.1ms - 1ms latency)

[ 5. Server Kernel & I/O Multiplexer ]
     └── Server NIC receives packet -> Kernel buffer -> kqueue/epoll flags FD as READABLE

[ 6. Redis aeEventLoop (ae.c) ]
     └── Single-threaded event loop wakes from epoll_wait() -> invokes readQueryFromClient()

[ 7. RESP Parser & Tokenizer (networking.c) ]
     └── Slices query buffer into argv array: ['SET', 'user:42', 'Tushar']

[ 8. Command Dispatch Table (server.c) ]
     └── Looks up 'setCommand' in server.commands hash table; checks arity & permissions

[ 9. Memory Allocator & Keyspace (dict.c & jemalloc) ]
     └── Allocates robj metadata header (16 bytes)
     └── Allocates SDS string buffer for key and value
     └── Inserts dictEntry into server.db[0].dict; updates 24-bit LRU clock
     └── Checks maxmemory eviction threshold budget

[ 10. Persistence & Replication Hooks ]
     └── If AOF enabled: Feeds raw RESP command to server.aof_buf for next fsync cycle
     └── If Replicas connected: Appends command to server.repl_backlog circular ring buffer

[ 11. Client Output Serialization ]
     └── Formats RESP status reply: +OK\r\n -> writes to client output buffer

[ 12. Response Network Return ]
     └── Server socket write() -> Kernel TCP Tx -> Client socket read() -> Terminal displays OK

========================================================================================
                           REDIS IS NO LONGER A BLACK BOX.
========================================================================================
    """)

if __name__ == "__main__":
    print_complete_command_journey()
