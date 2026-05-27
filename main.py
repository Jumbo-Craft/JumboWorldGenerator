import os

import amulet
from amulet.api.block import Block
import nbtlib


level = amulet.load_level('C:\\Users\\hojit\\workspace\\mc1.21.11\\saves\\Jumbo Test')
version = ('java', (1, 21, 11))
dimension = 'minecraft:overworld'
def main():
    #set_jmb_block(20, -60, -40, './tnt.nbt')
    field(0, 0, 0)
    level.save()
    level.close()


def set_jmb_block(x: int, y: int, z: int, path):
    st = nbtlib.load(path)
    blocks = st['blocks']
    palette = st['palette']
    for block in blocks:
        x1,y1,z1= block['pos']
        state = block['state']
        block_name = palette[state]['Name'].split(':')[1]
        if block_name == 'barrier':
            continue
        new_block = Block('minecraft', block_name)
        level.set_version_block(
            x=x1 + x, y=y1 + y, z=z1 + z,
            dimension=dimension,
            version=version,
            block=new_block
        )

def tree(x, y, z):
    tree_st = nbtlib.load('input/tree.nbt')
    blocks = tree_st['blocks']
    palette = tree_st['palette']

    for block in blocks:
        x1,y1,z1= block['pos']
        state = block['state']
        block_name = palette[state]['Name'].split(':')[1]
        if block_name != 'air':
            set_jmb_block(x + x1 * 16, y + y1 * 16, z + z1 * 16, f'./input/blocks/{block_name}.nbt')

def field(x, y, z):
    field_st = nbtlib.load('input/field.nbt')
    blocks = field_st['blocks']
    palette = field_st['palette']
    jmb_blocks = [f.split('.')[0] for f in os.listdir('./input/blocks')]

    for block in blocks:
        x1,y1,z1= block['pos']
        state = block['state']
        block_name = palette[state]['Name'].split(':')[1]
        if block_name != 'air' and block_name in jmb_blocks:
            set_jmb_block(x + x1 * 16, y + y1 * 16, z + z1 * 16, f'./input/blocks/{block_name}.nbt')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
