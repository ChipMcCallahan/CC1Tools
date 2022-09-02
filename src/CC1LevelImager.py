import io
import requests
from PIL import Image

class CC1LevelImager:
    def __init__(self, path="https://storage.googleapis.com/file-hosting-abcdef/chips/cc2tiles.png"):
        self.cc2_img = Image.open(io.BytesIO(requests.get(path).content))
        self.ARROWS_BMP={"N":(14,31,0,0,15,15,8,2),
                         "E":(14,31,16,0,31,15,14,8), 
                         "S":(15,31,0,0,15,15,8,14),
                         "W":(15,31,16,0,31,15,2,8)}
        self.cc1Elem2cc2BmpMapper = {
            0x00: [(0,2)],# FLOOR
            0x01: [(1,2)],# WALL
            0x02: [(11,3)],# CHIP
            0x03: [(12,24)],# WATER
            0x04: [(12,29)],# FIRE
            0x05: [(9,31)],# INV_WALL_PERM
            0x06: [(0,2),(1,10,0,0,31,2)],# PANEL_N
            0x07: [(0,2),(2,10,0,0,2,31)],# PANEL_W
            0x08: [(0,2),(1,10,0,29,31,31,0,29)],# PANEL_S
            0x09: [(0,2),(2,10,29,0,31,31,29,0)],# PANEL_E
            0x0A: [(9,1)], #[(8, 1)]# BLOCK
            0x0B: [(4,31)],# DIRT
            0x0C: [(10,1)],# ICE
            0x0D: [(1,19)],# FORCE_S
            0x0E: [(9,1), self.ARROWS_BMP["N"]],# CLONE_BLOCK_N
            0x0F: [(9,1), self.ARROWS_BMP["W"]],# CLONE_BLOCK_W
            0x10: [(9,1), self.ARROWS_BMP["S"]],# CLONE_BLOCK_S
            0x11: [(9,1), self.ARROWS_BMP["E"]],# CLONE_BLOCK_E
            0x12: [(0,19)],# FORCE_N
            0x13: [(2,19)],# FORCE_E
            0x14: [(2,20)],# FORCE_W
            0x15: [(6,2)],# EXIT
            0x16: [(1,1)],# BLUE_DOOR
            0x17: [(0,1)],# RED_DOOR
            0x18: [(3,1)],# GREEN_DOOR
            0x19: [(2,1)],# YELLOW_DOOR
            0x1A: [(14,1)],# ICE_SE
            0x1B: [(13,1)],# ICE_SW
            0x1C: [(11,1)],# ICE_NW
            0x1D: [(12,1)],# ICE_NE
            0x1E: [(10,31)],# BLUE_WALL_FAKE
            0x1F: [(0,10)],# BLUE_WALL_REAL
            0x20: [(0,0)],# NOT_USED_0
            0x21: [(3,2)],# THIEF
            0x22: [(4,2)],# SOCKET
            0x23: [(9,6)],# GREEN_BUTTON
            0x24: [(10,6)],# CLONE_BUTTON
            0x25: [(0,9),(8,9,2,2,29,29,2,2)], # plus 0,9# TOGGLE_WALL
            0x26: [(0,9)],# TOGGLE_FLOOR
            0x27: [(11,6)],# TRAP_BUTTON
            0x28: [(8,6)],# TANK_BUTTON
            0x29: [(0,2),(4,10)],# TELEPORT
            0x2A: [(5,4)],# BOMB
            0x2B: [(9,9)],# TRAP
            0x2C: [(11,31)],# INV_WALL_APP
            0x2D: [(9,10)],# GRAVEL
            0x2E: [(8,10)],# POP_UP_WALL
            0x2F: [(5,2)],# HINT
            0x30: [(0,2),(1,10,0,29,31,31,0,29),(2,10,29,0,31,31,29,0)],# PANEL_SE
            0x31: [(15,1)],# CLONER
            0x32: [(2,21)],# FORCE_RANDOM
            0x33: [(0,0)],# DROWN_CHIP
            0x34: [(0,0)],# BURNED_CHIP0
            0x35: [(0,0)],# BURNED_CHIP1
            0x36: [(0,0)],# NOT_USED_1
            0x37: [(0,0)],# NOT_USED_2
            0x38: [(0,0)],# NOT_USED_3
            0x39: [(0,0)],# CHIP_EXIT
            0x3A: [(0,0)],# UNUSED_EXIT_0
            0x3B: [(0,0)],# UNUSED_EXIT_1
            0x3C: [(0,0)],# CHIP_SWIMMING_N
            0x3D: [(0,0)],# CHIP_SWIMMING_W
            0x3E: [(0,0)],# CHIP_SWIMMING_S
            0x3F: [(0,0)],# CHIP_SWIMMING_E
            0x40: [(0,7), self.ARROWS_BMP["N"]],# ANT_N
            0x41: [(12,7), self.ARROWS_BMP["W"]],# ANT_W
            0x42: [(8,7), self.ARROWS_BMP["S"]],# ANT_S
            0x43: [(4,7), self.ARROWS_BMP["E"]],# ANT_E
            0x44: [(12,9), self.ARROWS_BMP["N"]],# FIREBALL_N
            0x45: [(12,9), self.ARROWS_BMP["W"]],# FIREBALL_W
            0x46: [(12,9), self.ARROWS_BMP["S"]],# FIREBALL_S
            0x47: [(12,9), self.ARROWS_BMP["E"]],# FIREBALL_E
            0x48: [(10,10), self.ARROWS_BMP["N"]],# BALL_N
            0x49: [(10,10), self.ARROWS_BMP["W"]],# BALL_W
            0x4A: [(10,10), self.ARROWS_BMP["S"]],# BALL_S
            0x4B: [(10,10), self.ARROWS_BMP["E"]],# BALL_E
            0x4C: [(0,8), self.ARROWS_BMP["N"]],# TANK_N
            0x4D: [(6,8), self.ARROWS_BMP["W"]],# TANK_W
            0x4E: [(4,8), self.ARROWS_BMP["S"]],# TANK_S
            0x4F: [(2,8), self.ARROWS_BMP["E"]],# TANK_E
            0x50: [(8,8), self.ARROWS_BMP["N"]],# GLIDER_N
            0x51: [(14,8), self.ARROWS_BMP["W"]],# GLIDER_W
            0x52: [(12,8), self.ARROWS_BMP["S"]],# GLIDER_S
            0x53: [(10,8), self.ARROWS_BMP["E"]],# GLIDER_E
            0x54: [(0,11), self.ARROWS_BMP["N"]],# TEETH_N
            0x55: [(6,11), self.ARROWS_BMP["W"]],# TEETH_W
            0x56: [(0,11), self.ARROWS_BMP["S"]],# TEETH_S
            0x57: [(3,11), self.ARROWS_BMP["E"]],# TEETH_E
            0x58: [(0,13), self.ARROWS_BMP["N"]],# WALKER_N
            0x59: [(0,13), self.ARROWS_BMP["W"]],# WALKER_W
            0x5A: [(0,13), self.ARROWS_BMP["S"]],# WALKER_S
            0x5B: [(0,13), self.ARROWS_BMP["E"]],# WALKER_E
            0x5C: [(0,15), self.ARROWS_BMP["N"]],# BLOB_N
            0x5D: [(0,15), self.ARROWS_BMP["W"]],# BLOB_W
            0x5E: [(0,15), self.ARROWS_BMP["S"]],# BLOB_S
            0x5F: [(0,15), self.ARROWS_BMP["E"]],# BLOB_E
            0x60: [(0,12), self.ARROWS_BMP["N"]],# PARAMECIUM_N
            0x61: [(9,12), self.ARROWS_BMP["W"]],# PARAMECIUM_W
            0x62: [(6,12), self.ARROWS_BMP["S"]],# PARAMECIUM_S
            0x63: [(4,12), self.ARROWS_BMP["E"]],# PARAMECIUM_E
            0x64: [(0,2),(5,1)],# BLUE_KEY
            0x65: [(0,2),(4,1)],# RED_KEY
            0x66: [(0,2),(7,1)],# GREEN_KEY
            0x67: [(0,2),(6,1)],# YELLOW_KEY
            0x68: [(0,2),(0,6)],# FLIPPERS
            0x69: [(0,2),(1,6)],# FIREBOOTS
            0x6A: [(0,2),(2,6)],# SKATES
            0x6B: [(0,2),(3,6)],# SUCTION_BOOTS
            0x6C: [(0,22), self.ARROWS_BMP["N"]],# PLAYER_N
            0x6D: [(8,23), self.ARROWS_BMP["W"]],# PLAYER_W
            0x6E: [(0,23), self.ARROWS_BMP["S"]],# PLAYER_S
            0x6F: [(8,22), self.ARROWS_BMP["E"]],# PLAYER_E
        }
    
    def get_pixels(self, x, y, subx1=0, suby1=0, subx2=31, suby2=31, offsetx=0, offsety=0):
        x1, y1 = x * 32 + subx1, y * 32 + suby1
        x2, y2 = x * 32 + subx2, y * 32 + suby2
        tile = Image.new("RGBA", (32, 32))
        tile.paste(self.cc2_img.crop((x1, y1, x2+1, y2+1)), (offsetx, offsety)) # account for the [x0, x1) non inclusive boundary
        return tile
    

    def get_tile(self, index):
        parts = self.cc1Elem2cc2BmpMapper[index]
        new = Image.new("RGBA", (32, 32))
        for part in parts:
            pixels = self.get_pixels(*part)
            new.paste(pixels, (0,0), pixels)
        return new

    def image(self, level, width=32, height=32):
        map_img = Image.new("RGBA", (width*32, height*32))
        for i in range(width):
            for j in range(height):
                spec = level.map[j * 32 + i]
                tile_img = self.get_tile(spec.bottom)
                if spec.top != spec.bottom:
                    paste = self.get_tile(spec.top)
                    tile_img.paste(paste, (0,0), paste)
                map_img.paste(tile_img, (i*32, j*32))
        return map_img
    
    def save_png(self, level, filename, width=32, height=32):
        self.image(level, width, height).save(filename, format='png')
