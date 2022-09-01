import struct
import io
import xml.etree.ElementTree as ET
import re
import os
from .cc1_levelset_pb2 import *
from .CC1LevelsetImporter import CC1LevelsetImporter

def read_byte(bytes):
    return struct.unpack("<B", bytes.read(1))[0]

def read_short(bytes):
    return struct.unpack("<H", bytes.read(2))[0]

def read_long(bytes):
    return struct.unpack("<L", bytes.read(4))[0]


class DATReader:
    def build_movement(self, movement_bytes, level):
        raw_bytes = io.BytesIO(movement_bytes)
        for _ in range(len(movement_bytes) // 2):
            monster_x, monster_y = read_byte(raw_bytes), read_byte(raw_bytes)
            level.movement.append(monster_y * 32 + monster_x)

    def build_cloners(self, cloner_bytes, level):
        raw_bytes = io.BytesIO(cloner_bytes)
        for _ in range(len(cloner_bytes) // 8):
            button_x, button_y = read_short(raw_bytes), read_short(raw_bytes)
            cloner_x, cloner_y = read_short(raw_bytes), read_short(raw_bytes)
            level.clone_controls[button_y * 32 + button_x] = cloner_y * 32 + cloner_x

    def build_traps(self, trap_bytes, level):
        raw_bytes = io.BytesIO(trap_bytes)
        for _ in range(len(trap_bytes) // 10):
            button_x, button_y = read_short(raw_bytes), read_short(raw_bytes)
            trap_x, trap_y = read_short(raw_bytes), read_short(raw_bytes)
            _ = read_short(raw_bytes) # open/closed, unused
            level.trap_controls[button_y * 32 + button_x] = trap_y * 32 + trap_x
    
    def build_map(self, bottom_bytes, top_bytes, level):
        arr = [list(list() for i in range(32)) for j in range(32)]
        for raw_layer in (bottom_bytes, top_bytes):
            raw_bytes = io.BytesIO(raw_layer)
            index = 0
            while index < 32 * 32:
                next_byte = read_byte(raw_bytes)
                if next_byte == 0xFF: # run length encoding
                    length, obj = read_byte(raw_bytes), read_byte(raw_bytes)
                    for _ in range(length):
                        arr[index % 32][index // 32].append(obj)
                        index += 1
                else:
                    arr[index % 32][index // 32].append(next_byte)
                    index += 1
       
        for i in range(32):
            for j in range(32):
                if arr[i][j] != [0, 0]:
                    level.map[j * 32 + i].bottom = arr[i][j][0]
                    level.map[j * 32 + i].top = arr[i][j][1]
    
    def read(self, raw_levelset):
        raw_levelset=io.BytesIO(raw_levelset)
        _ = read_long(raw_levelset) # magic number, unused
        num_levels = read_short(raw_levelset)
        levelset = Levelset()
        for i in range(num_levels):
            level = levelset.levels.add()

            level_size_bytes = read_short(raw_levelset)
            level.number = read_short(raw_levelset)
            level.time = read_short(raw_levelset)
            level.chips = read_short(raw_levelset)
            
            map_detail = read_short(raw_levelset) # 0 or 1, map_detail, unused
            
            nbytes = read_short(raw_levelset)
            top_bytes = raw_levelset.read(nbytes)
            nbytes = read_short(raw_levelset)
            bottom_bytes = raw_levelset.read(nbytes)
            self.build_map(bottom_bytes, top_bytes, level)

            bytes_left = read_short(raw_levelset)
            while bytes_left > 0:
                field = read_byte(raw_levelset)
                length = read_byte(raw_levelset)
                if field == 3:
                    level.title = raw_levelset.read(length)[:-1].decode('utf-8')
                elif field == 4:
                    self.build_traps(raw_levelset.read(length), level)
                elif field == 5:
                    self.build_cloners(raw_levelset.read(length), level)
                elif field == 6:
                    level.password = ''.join([chr(b^0x99) for b in raw_levelset.read(length)[:-1]])
                elif field == 7:
                    level.hint = raw_levelset.read(length)[:-1].decode('utf-8')
                elif field == 10:
                    self.build_movement(raw_levelset.read(length), level)
                else:
                    raise ValueError("Encountered Unexpected Field " + str(field))
                bytes_left -= length + 2
        return levelset


class CCXReader:
    def read_into(self, ccx_bytes, levelset):
        root = ET.fromstring(ccx_bytes)
        levelset.name = root.attrib['description']

        for child in root:
            i = int(child.attrib['number'])
            levelset.levels[i - 1].author = child.attrib['author']
            for gchild in child:
                story = levelset.stories.add()
                story.level_number = i
                story.type = Levelset.Story.Type.EPILOGUE if gchild.tag == "epilogue" else Levelset.Story.Type.PROLOGUE
                text_entries = re.split("<.+?>", gchild[0].text)
                text_entries = [e.replace('\n', '') for e in text_entries]
                text_entries = [e.replace('&nbsp;', '') for e in text_entries if len(e) > 0]
                story.text.extend(text_entries)


class CC1LevelsetReader:
    def __init__(self):
        self.importer = CC1LevelsetImporter()

    def read(self, dat, ccx=None, *, name=None):
        if isinstance(dat, str): # assume passed in a file name
            name = name or dat # store the name if another wasn't supplied
            with open(dat, 'rb') as f:
                dat = f.read()
        if ccx and ccx.endswith('.ccx'):
            with open(ccx, 'r') as f:
                 ccx = f.read()
        dat_reader = DATReader()
        levelset = dat_reader.read(dat)
        if ccx:
            ccx_reader = CCXReader()
            ccx_reader.read_into(ccx, levelset)
        else:
            if name:
                levelset.name = name
        return levelset

    def import_and_read(self, levelset_name):
        return self.read(*self.importer.get_set(levelset_name), name=levelset_name)