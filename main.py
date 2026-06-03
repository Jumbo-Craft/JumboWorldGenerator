import os
import time

import amulet
import numpy as np
from amulet.api.block import Block
import nbtlib
from amulet.api.chunk import Chunk

origin = amulet.load_level('C:\\Users\\hojit\\workspace\\mc1.21.11\\saves\\Biome World')
level = amulet.load_level('C:\\Users\\hojit\\workspace\\mc1.21.11\\saves\\Jumbo Test2')
version = ('java', (1, 21, 11))
dimension = 'minecraft:overworld'
jmb_blocks = [f.split('.')[0] for f in os.listdir('./input/blocks')]


def main():
    start = time.time()
    #copy_biome((3388,75,8580), off_y=-75)
    baumkuchen((18808, 80, 98115), 24, 80, off_y=-84)
    print('saving...')
    level.save()
    level.close()
    origin.close()
    end = time.time()
    print(f'time: {end - start}')

def boring(begin: tuple[int, int, int], height: int, off_y: int=0):
    x, y, z = begin
    for i in range (height):
        loc = (x, y + i, z)
        copy_biome(loc, off_y)
        block2jmb_block(loc, off_y)
    print(f'complete boring!(x:{x}, z:{z})')


def block2jmb_block(loc: tuple[int, int, int], off_y: int=0):
    x, y, z = loc
    block, block_entity = origin.get_version_block(
        x=x, y=y, z=z,
        dimension=dimension,
        version=version
    )

    if block_entity is not None:
        return

    block_name = block.namespaced_name.split(':')[1]
    if block_name in jmb_blocks:
        set_jmb_block((x * 16, (y + off_y) * 16, z * 16), block_name)

def baumkuchen(center: tuple[int, int, int], height: int, n_max: int, n1: int=1, off_y: int=0):
    cx, cy, cz = center

    if n1 == 1:
        boring(center, height, off_y)
        n = 2
    else:
        n = n1

    loc = (-n + 2, -n + 1)
    shift = np.array([1,0])

    for i in range ((2 * n - 3)**2, (2 * n_max - 1)**2):
        boring((cx + loc[0], cy, cz + loc[1]), height, off_y)

        if i % (2 * (n - 1)) == 0:
            shift = np.array([-shift[1], shift[0]])

        if i == (2 * n - 1)**2 - 1:
            loc += np.array([0, -1])
            n += 1
        else:
            loc += shift

block_palette = {}
jmb_palette = {}

def set_jmb_block(loc: tuple[int, int, int], jmb_name: str):
    x, y, z = loc

    if jmb_name in jmb_palette.keys():
        block_lst = jmb_palette[jmb_name]
        for block in block_lst:
            x1,y1,z1 = block['pos']
            new_block = block['block']
            level.set_version_block(
                x=x1 + x, y=y1 + y, z=z1 + z,
                dimension=dimension,
                version=version,
                block=new_block
            )
    else:
        st = nbtlib.load(f'./input/blocks/{jmb_name}.nbt')
        blocks = st['blocks']
        palette = st['palette']

        block_lst = []
        for block in blocks:
            x1,y1,z1= block['pos']
            state = block['state']
            block_name = palette[state]['Name'].split(':')[1]
            if block_name == 'barrier':
                continue

            if block_name in block_palette.keys():
                new_block = block_palette[block_name]
            else:
                new_block = Block('minecraft', block_name)
                block_palette[block_name] = new_block

            level.set_version_block(
                x=x1 + x, y=y1 + y, z=z1 + z,
                dimension=dimension,
                version=version,
                block=new_block
            )

            block_lst.append({
                    'pos': (x1, y1, z1),
                    'block': new_block,
                })

        jmb_palette[jmb_name] = block_lst



def copy_biome(loc: tuple[int, int, int], off_y: int=0):
    x, y, z = loc
    if not level.has_chunk(x, z, dimension):
        chunk = Chunk(x, z)
        chunk.status = 'full'
        chunk.misc['dimension'] = dimension
        level.put_chunk(chunk, dimension)
    else:
        chunk = level.get_chunk(x, z, dimension)

    biomes = chunk.biomes
    biome_id = level.biome_palette.get_add_biome(get_biome_at(origin, loc))

    biomes.convert_to_3d()
    section = biomes.get_section(y + off_y)
    section[:] = biome_id
    biomes.add_section(y + off_y, section)

    chunk.changed = True


def get_biome_at(lv, loc: tuple[int, int, int]):
    x, y, z = loc
    cx = x >> 4
    cz = z >> 4
    lx = x & 15
    lz = z & 15

    chunk = lv.get_chunk(cx, cz, dimension)
    biomes = chunk.biomes

    biome_id = biomes[lx >> 2, y >> 2, lz >> 2]

    return str(lv.biome_palette[biome_id])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()