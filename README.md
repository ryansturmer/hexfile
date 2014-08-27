hexfile
=======

This is a simple library for parsing hex files.  Currently only intel hex files are supported.

Installation
------------
You can use the included setup.py or use your pip to install it from PyPI

Usage
-----
To create a HexFile object use hexfile.load:

```python
import hexfile

f = hexfile.load('memory.hex')
```

The `HexFile` object is composed of one or more memory segments, which may be discontinuous.  You can access the contents of the hex file as though it were an array of bytes:

```python
print f.size       # Total number of bytes in the hexfile (NOT the total span of all addresses)

byte = f[16]       # Returns the byte at address 16 (as an int)

bytes = f[256:512] # Returns 256 bytes as a list

print f.segments   # Display all the segments in the hex file

```

The `HexFile` object also supports iteration, but rather than iterating over byte values as if it were a list, it includes the byte addresses, as if it were enumerated.  This is because the file might be discontinuous, so addresses are frequently needed during iteration.

```
for addr, data in f:
    print '0x%08x : 0x%02x' % (addr, data) # Print every byte in the hex file and its 32-bit address
```
