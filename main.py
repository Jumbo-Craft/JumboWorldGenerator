import os

import amulet
import numpy as np
from amulet.api.block import Block
import nbtlib


origin = amulet.load_level('C:\\Users\\hojit\\workspace\\mc1.21.11\\saves\\Biome World')
level = amulet.load_level('C:\\Users\\hojit\\workspace\\mc1.21.11\\saves\\Jumbo Test')
version = ('java', (1, 21, 11))
dimension = 'minecraft:overworld'
def main():
    #set_jmb_block(20, -60, -40, './tnt.nbt')
    #field(0, 0, 0)
    #for i in range(32):
    #    for j in range(32):
    #        boring((-32 + i, 65, 131 + j), 10)
    baumkuchen((0,0), (0,0), 4)
    level.save()
    level.close()
    origin.close()

def boring(begin: tuple[int, int, int], height: int):
    x, y, z = begin
    for i in range (height):
        block2jmb_block((x, y + i, z), -65)
    #print('complete boring!')


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
    jmb_blocks = [f.split('.')[0] for f in os.listdir('./input/blocks')]
    #print(block_name)
    if block_name in jmb_blocks:
        set_jmb_block((x * 16, (y + off_y) * 16, z * 16), f'./input/blocks/{block_name}.nbt')

def baumkuchen(center: tuple[int, int], begin: tuple[int, int], roll: int):
    cx, cz = center
    bx, bz = begin
    diff_x = abs(cx - bx)
    diff_z = abs(cz - bz)
    n = 1
    loc = (0, 0)
    shift = np.array([1,0])
    test_block = Block('minecraft', 'tnt')
    for i in range (roll):
        for j in range (n * 4):
            level.set_version_block(
                x=loc[0], y=0, z=loc[1],
                dimension=dimension,
                version=version,
                block=test_block
            )
            if (j + 1) % n == 0:
                shift = np.array([-shift[1], shift[0]])
            loc += np.array([0, -1]) if j == n * 4 - 1 else shift
        n += 2



def set_jmb_block(loc: tuple[int, int, int], path):
    x, y, z = loc
    st = nbtlib.load(path)
    blocks = st['blocks']
    palette = st['palette']
    block_palette = {}
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
