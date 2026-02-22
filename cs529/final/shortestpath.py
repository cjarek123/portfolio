"""
CS529

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import numpy as np
from PIL import Image

def load_map(path, new_size=(120, 120)):
    image = Image.open(path).convert('L')

    resized = image.resize(new_size, resample=Image.BILINEAR)
    image_array = np.array(resized)
    binary_map = (image_array < 128).astype(int)

    h, w = binary_map.shape
    new_h, new_w = new_size
    block_h = h // new_h
    block_w = w // new_w

    abstracted_map = np.zeros((new_h, new_w), dtype=int)

    for i in range(new_h):
        for j in range(new_w):
            pixel = binary_map[i*block_h:(i+1)*block_h, j*block_w:(j+1)*block_w]
            abstracted_map[i, j] = 1 if np.any(pixel) else 0

    return abstracted_map

def print_abstract_map(abstracted_map):
    """
    . is free, # is obstacle
    """
    for row in abstracted_map:
        print(''.join('#' if cell else '.' for cell in row))

if __name__ == '__main__':
    image_path = 'map1.bmp'
    new_size = (120, 120)

    abstracted_map = load_map(image_path, new_size)
    print_abstract_map(abstracted_map)