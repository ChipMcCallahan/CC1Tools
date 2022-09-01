import io
import struct

from .cc1_levelset_pb2 import *


class byte_writer:
    def __init__(self):
        self.output = io.BytesIO(bytes())

    def write_long(self, long):
        self.output.write(struct.pack("<L", long))

    def write_short(self, short):
        self.output.write(struct.pack("<H", short))
    
    def write_shorts(self, shorts):
        for short in shorts:
            self.write_short(short)

    def write_byte(self, byte):
        self.output.write(struct.pack("<B", byte))
    
    def write(self, bytes):
        self.output.write(bytes)
    
    def getvalue(self):
        return self.output.getvalue()


class CC1LevelsetWriter:
    def __init__(self):
        self.encrypted_chars = [0xD8, 0xDB, 0xDA, 0xDD, 0xDC, 0xDF, 0xDE, 0xD1, 0xD0, 0xD3, 0xD2, 0xD5, 0xD4, 0xD7, 0xD6, 0xC9, 0xC8, 0xCB, 0xCA, 0xCD, 0xCC, 0xCF, 0xCE, 0xC1, 0xC0, 0xC3]

    def write(self, levelset, *, filename=None):
        output = byte_writer()
        output.write_long(0x0002AAAC) # magic number
        output.write_short(len(levelset.levels)) # num_levels
        for i in range(len(levelset.levels)):
            level_bytes = self.write_level(levelset.levels[i])
            output.write_short(len(level_bytes))
            output.write(level_bytes)
        if filename:
            with open(filename, "wb") as f:
                f.write(output.getvalue())
            print(f"Wrote set to file {filename}")
        else:
            return output.getvalue()
    
    def write_level(self, level):
        output = byte_writer()
        output.write_short(level.number)
        output.write_short(level.time)
        output.write_short(level.chips)
        output.write_short(1) # 0 or 1, map detail, unused
        layer1, layer2 = self.write_layers(level.map)
        output.write_short(len(layer1))
        output.write(layer1)
        output.write_short(len(layer2))
        output.write(layer2)

        remaining = byte_writer()
        if level.title:
            remaining.write_byte(3) # title field
            title_bytes = level.title.encode('utf-8') + b'\x00'
            remaining.write_byte(len(title_bytes))
            remaining.write(title_bytes )
        if len(level.trap_controls) > 0:
            remaining.write_byte(4) # traps field
            remaining.write_byte(10 * len(level.trap_controls))
            for k, v in level.trap_controls.items():
                remaining.write_shorts((k % 32, k // 32, v % 32, v // 32, 0)) # last short = open/closed, unused
        if len(level.clone_controls) > 0:
            remaining.write_byte(5) # cloners field
            remaining.write_byte(8 * len(level.clone_controls))
            for k, v in level.clone_controls.items():
                remaining.write_shorts((k % 32, k // 32, v % 32, v // 32))
        if level.password:
            remaining.write_byte(6) # password field
            pword_bytes = self.encrypt(level.password.encode('utf-8')) + b'\x00'
            remaining.write_byte(len(pword_bytes))
            remaining.write(pword_bytes)
        if level.hint:
            remaining.write_byte(7) # hint field
            hint_bytes = level.hint.encode('utf-8') + b'\x00'
            remaining.write_byte(len(hint_bytes))
            remaining.write(hint_bytes )
        if len(level.movement) > 0:
            remaining.write_byte(10) # movement field
            remaining.write_byte(2 * len(level.movement))
            for p in level.movement:
                remaining.write_byte(p % 32)
                remaining.write_byte(p // 32)
        
        output.write_short(len(remaining.getvalue()))
        output.write(remaining.getvalue())
        return output.getvalue()
    
    def write_layers(self, map):
        layers = [byte_writer(), byte_writer()]
        for i in range(32 * 32):
            layers[0].write_byte(map[i].top)
            layers[1].write_byte(map[i].bottom)
        return tuple(self.compress_layer(layer.getvalue()) for layer in layers)
    
    # replace any substrings containing [4, 255] of the same character
    # with run length encoding
    def compress_layer(self, layer):
        index = 0
        output = byte_writer()
        while index < len(layer):
            c = layer[index]
            end = index
            while end + 1 < len(layer) and layer[end + 1] == c and end + 1 - index < 255:
                end += 1
            length = end + 1 - index
            if length <= 3:
                output.write(c.to_bytes(1, 'little') * length)
            else:
                output.write(b'\xff') # signify RLE
                output.write_byte(length)
                output.write_byte(c)
            index += length
        return output.getvalue()

    def encrypt(self, input):
        output = byte_writer()
        for c in input:
            if c < 65 or c > 90:
                raise f"password must be all caps, was {input}"
            index = c - int.from_bytes(b'A', "big")
            output.write_byte(self.encrypted_chars[index])
        return output.getvalue()