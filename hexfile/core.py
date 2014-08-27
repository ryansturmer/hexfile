import itertools

def short(msb,lsb):
    return (msb<<8) | lsb

class HexFile(object):
    def __init__(self, segments):
        self.segments = segments

    def __getitem__(self, val):
        if isinstance(val, slice):
            address = val.start
        else:
            address = val

        for segment in self.segments:
            if address in segment:
                return segment[val]

        raise IndexError('No segment contains address 0x%x' % address)

    def __len__(self):
        return sum(map(len, self.segments))

    @property
    def size(self):
        return len(self)

    def __iter__(self):
        return itertools.chain(*self.segments)

    @staticmethod
    def load(filename):
        segments = [Segment(0)]

        with open(filename) as fp:
            lines = fp.readlines()

        extended_segment_address = 0
        current_address = 0
        end_of_file = False

        lineno = 0
        for line in lines:
            lineno += 1
            line = line.strip();
            if not line.startswith(':'):
                continue

            if end_of_file:
                raise Exception("Record found after end of file on line %d" % lineno)

            bytes = [int(line[i:i+2], 16) for i in range(1,len(line), 2)]
            byte_count = bytes[0]
            address = short(*bytes[1:3])
            record_type = bytes[3]
            checksum = bytes[-1]
            data = bytes[4:-1]
            computed_checksum = ((1 << 8)-(sum(bytes[:-1]) & 0xff)) & 0xff

            if(computed_checksum != checksum):
                raise Exception("Record checksum doesn't match on line %d" % lineno)

            if record_type == 0:
                if byte_count == len(data):
                    #print "Data@0x%08x: %s" % (address | extended_linear_address, data)
                    current_address = (address | extended_linear_address)
                    have_segment = False
                    for segment in segments:
                        if segment.end_address == current_address:
                            segment.data.extend(data)
                            have_segment = True
                            break
                    if not have_segment:
                        segments.append(Segment(current_address, data))
                else:
                    raise Exception("Data record reported size does not match actual size on line %d" % lineno)
            elif record_type == 1:
                end_of_file = True
            elif record_type == 4:
                if byte_count != 2 or len(data) != 2:
                    raise Exception("Byte count misreported in extended linear address record on line %d" % lineno)
                extended_linear_address = short(*data) << 16

            else:
                print "Unknown record type: %s" % record_type 
        return HexFile(segments)

def load(filename):
    return HexFile.load(filename)

class Segment(object):
    def __init__(self, start_address, data = None):
        self.start_address = start_address
        self.data = data or []

    def __str__(self):
        return '<%d byte segment @ 0x%08x>' % (self.size, self.start_address)
    def __repr__(self):
        return str(self)

    @property
    def end_address(self):
        return self.start_address + len(self.data)

    @property
    def size(self):
        return len(self.data)

    def __contains__(self, address):
        return address >= self.start_address and address < self.end_address

    def __getitem__(self, address):
        if isinstance(address, slice):
            if address.start not in self or address.stop-1 not in self:
                raise IndexError('Address out of range for this segment')
            else:
                return self.data[address.start-self.start_address:address.stop-self.start_address:address.step]
        else:
            if not address in self:
                raise IndexError("Address 0x%x is not in this segment" % address)
            return self.data[address-self.start_address]
    @property
    def addresses(self):
        return range(self.start_address, self.end_address)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(zip(self.addresses, self.data))
