Network IPC: Sockets
====================

    struct sockaddr {
        sa_family_t sa_family; /* address family */
        char        sa_data[]; /* variable-length address */
        ...
    };

    struct sockaddr_in {
        sa_family_t     sin_family;     /* address family */
        in_port_t       sin_port;       /* port number */
        struct in_addr  sin_addr;       /* IPv4 address */
        unsigned char   sin_zero[8];    /* filler */
    };

    struct sockaddr_in6 {
        sa_family_t     sin6_family;    /* address family */
        in_port_t       sin6_port;      /* port number */
        uint32_t        sin6_flowinfo;  /* traffic class and flow info */
        struct in6_addr sin6_addr;      /* IPv6 address */
        uint32_t        sin6_scope_id;  /* set of interfaces for scope */
    }

Although the sockaddr_in and sockaddr_in6 structures are quite different, they are both passed to the socket routines cast to a sockaddr structre.