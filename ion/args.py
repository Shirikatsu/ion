## Copyright (c) 2016-2018 Clearmatics Technologies Ltd
## SPDX-License-Identifier: LGPL-3.0+

#!/usr/bin/env python
"""
Provides a set of useful arguements for interacting with ethrpc
"""
from .ethrpc import EthJsonRpc
from .utils import require, scan_bin


def arg_bytes(ctx, param, value):
    if value is None:
        return None
    value = scan_bin(value)
    return value

def make_bytes_n(num_bytes):
    def arg_bytes_n(ctx, param, value):
        value = arg_bytes(ctx, param, value)
        if value is None:
            return None
        require(len(value) == num_bytes, str(num_bytes) + " bytes required")
        return value
    return arg_bytes_n


arg_bytes20 = make_bytes_n(20)
arg_bytes32 = make_bytes_n(32)


def make_uint_n(num):
    def arg_uint_n(ctx, param, value):
        if value is None:
            return None
        value = int(value)
        require(value >= 0)
        require(value <= (1 << (num-1)))
        return value
    return arg_uint_n

arg_uint256 = make_uint_n(256)


def arg_ethrpc(ctx, param, value):
    if value is None:
        return None
    ip_addr, port = value.split(':')
    port = int(port)
    require(port > 0)
    require(port < 0xFFFF)
    if port == 443:
        return EthJsonRpc(ip_addr, port, True)
    return EthJsonRpc(ip_addr, port)

def arg_lithium_api(ctx, param, value):
    if value is None:
        return None
    ip_addr, port = value.split(':')
    port = int(port)
    require(port > 0)
    require(port < 0xFFFF)
    return {'ip_addr': ip_addr, 'port': port}
