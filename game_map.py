from sprites import get_image
import random

class Tile(object):
    tile_type = None

    def __init__(self, tile_type='tile', tile_num=0):
        self.tile_type = tile_type
        self.tile_num  = tile_num
        self.image     = get_image('tile')
        self.update_tile(self.tile_type)
        self.contents  = []

    def update_tile(self, tile_type):
        self.tile_type = tile_type
        self.image = get_image(self.tile_type)

    def __repr__(self):
        return "[]" if self.tile_type == 'tile' else '{}'

def generate_map(rows, cols, style):
    if style == 'random':
        return [[Tile(tile_type_generator())
            for row in range(rows)]
            for col in range(cols)]
    if style == 'rooms':
        def generate_room_row(rows):
            room_row = []
            for row in range(rows):
                if (row % 12) < 8:
                    room_row.append(Tile('tile'))
                else:
                    room_row.append(Tile('scroll'))
            return room_row

        def generate_interior_row(rows):
            interior_row = []
            for row in range(rows):
                if (row % 12) in (1, 3, 10, 11):
                    interior_row.append('tile')
                    interior_row.append('scroll')
                else:
                    interior_row.append('tile')
            return interior_row

        def generate_corridor_row(rows):
            corridor_row = []
            for row in range(rows):
                corridor_row.append(Tile('tile'))
            return corridor_row

        floor = []
        for row in range(cols):
            if 0 > row % 10 > 5:
                floor.append(generate_room_row(cols))
            elif 5 >= row % 10 > 7:
                floor.append(generate_interior_row(cols))
            elif 7 >= row % 10 > 10:
                floor.append(generate_corridor_row(cols))

        return [generate_room_row(rows) if col % 10 else generate_corridor_row(rows) for col in range(cols)]



def tile_type_generator():
    if not random.randint(0, 20):
        return 'scroll'
    z = random.randint(0, 16)
    return [
        'tile',
        'tile',
        'tile',
        'tile',
        'tile',
        'tile',
        'tile',
        'tile',
        'tile',
        'tile',
        'tile',
        'tile',
        'othertile',
        'othertile',
        'othertile',
        'othertile',
        'otherothertile',
    ][z]

class Atlas(object):
    def __init__(self, rows=None, cols=None):
        self.rows = rows if rows else 100
        self.cols = cols if cols else 100
        self.atlas = generate_map(self.rows, self.cols, style='rooms')
    def __iter__(self):
        return iter([tile for row in self.atlas for tile in row])

    def is_location(self, x, y):
        if x in range(0, self.rows + 1) and y in range(0, self.cols + 1):
            try:
                return 'tile' in self.atlas[x][y].tile_type
            except IndexError:
                pass
        return False

    def pos(self, x, y):
        if self.is_location(x, y):
            return self.atlas[x][y]

    def has_contents(self, x, y, tile=None):
        if not tile:
            tile = self.pos(x, y)
        if tile.contents:
            return True

        return False

    def is_empty(self,x, y, tile=None):
        if not tile:
            tile = self.pos(x, y)
        if tile and not self.has_contents(0, 0, tile=tile):
            return True

        return False

    def place_on_tile(self, thing, x, y):
        tile = self.pos(x, y)
        if tile:
            tile.contents.append(thing)

    def remove_from_tile(self, thing, x, y):
        tile = self.pos(x,y)
        if tile:
            tile.contents.remove(thing)

    def return_tiles(self, left, right, bottom, top):
        def return_tile(atlas, x, y):
            tile = atlas.pos(x, y)
            if tile:
                return tile
            else:
                return Tile(tile_type='scroll')

        tiles_to_return = [[return_tile(self, i, j)
                for j in range(bottom, top)]
                for i in range(left, right)]
        return tiles_to_return
