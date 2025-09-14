#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 23.2.2012

@author: David
'''


def bytes2bin(raw_bytes, sz=8):
    """Accepts a string of bytes (chars) and returns an array of bits representing
    the bytes in big endian byte (Most significant byte/bit first) order.  Each byte
    can have it's higher bits ignored by passing a sz."""
    if sz < 1 or sz > 8:
        raise ValueError("Invalid sz value: " + str(sz))
    ret_val = []
    for b in raw_bytes:
        bits = []
        b = ord(b)
        while b > 0:
            bits.append(b & 1)
            b >>= 1

        if len(bits) < sz:
            bits.extend([0] * (sz - len(bits)))
        elif len(bits) > sz:
            bits = bits[:sz]

        bits.reverse()  # Big endian byte order.
        ret_val.extend(bits)

    if len(ret_val) == 0:
        ret_val = [0]
    return ret_val


def bin2bytes(x):
    """Convert an array of bits (MSB first) into a string of characters."""
    bits = []
    bits.extend(x)
    bits.reverse()

    i = 0
    out = ''
    multi = 1
    ttl = 0
    for b in bits:
        i += 1
        ttl += b * multi
        multi *= 2
        if i == 8:
            i = 0
            out += chr(ttl)
            multi = 1
            ttl = 0

    if multi > 1:
        out += chr(ttl)

    out = out[::-1]  # More efficient string reversal
    return out


def bin2dec(x):
    """Convert an array of "bits" (MSB first) to it's decimal value."""
    bits = []
    bits.extend(x)
    bits.reverse()

    multi = 1
    value = 0
    for b in bits:
        value += b * multi
        multi *= 2
    return value


def bytes2dec(raw_bytes, sz=8):
    return bin2dec(bytes2bin(raw_bytes, sz))


def dec2bin(n, p=0):
    """Convert a decimal value to an array of bits (MSB first), optionally padding
    the overall size to p bits. """
    assert (n >= 0)
    ret_val = []

    while n > 0:
        ret_val.append(n & 1)
        n >>= 1

    if p > 0:
        ret_val.extend([0] * (p - len(ret_val)))
        ret_val.reverse()

    return ret_val


def dec2bytes(n, p=0):
    return bin2bytes(dec2bin(n, p))


def bin2synchsafe(x):
    """Convert a list of bits (MSB first) to a synch safe list of bits."""

    if len(x) > 32 or bin2dec(x) > 268435456:  # 2^28
        raise ValueError("Invalid value")
    elif len(x) < 8:
        return x

    n = bin2dec(x)
    bites = ""
    bites += chr((n >> 21) & 0x7f)
    bites += chr((n >> 14) & 0x7f)
    bites += chr((n >> 7) & 0x7f)
    bites += chr((n >> 0) & 0x7f)
    bits = bytes2bin(bites)
    if len(bits) < 32:
        bits = ([0] * (32 - len(x))) + bits

    return bits


def bytes2str(raw_bytes):
    s = ""
    for b in raw_bytes:
        s += ("\\x%02x" % ord(b))
    return s
