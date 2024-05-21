import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct
import math

MAX_RGB_VALUE = 16777216

class Bernoulli:
    def __init__(self, seed, p):
        np.random.seed(seed)
        self.p = p

    def generate_permutation_matrix(self, rows, cols):
        matrix = np.arange(rows * cols).reshape(rows, cols)
        matrix = np.array(matrix.flat)  # Преобразуем flatiter в массив numpy
        np.random.shuffle(matrix)
        return matrix.reshape(rows, cols)

class DCT:
    def apply_dct(self, block):
        return dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')

    def apply_idct(self, block):
        return idct(idct(block, axis=0, norm='ortho'), axis=1, norm='ortho')

class Scrambler:
    def __init__(self):
        self.bernoulli = None
        self.dct = DCT()

    def modify_matrix(self, block, permutation_matrix):
        result = np.zeros(block.shape)
        for i in range(block.shape[0]):
            for j in range(block.shape[1]):
                new_index = permutation_matrix[i * block.shape[1] + j]  # Исправлено здесь
                new_i = new_index // block.shape[1]
                new_j = new_index % block.shape[1]
                result[new_i, new_j] = block[i, j]
        return result

    def scramble(self, image, seed, p, n):
        self.bernoulli = Bernoulli(seed, p)
        blocks = self.convert_to_blocks(image)
        blocks = [self.dct.apply_dct(block) for block in blocks]
        permutation_matrix = self.bernoulli.generate_permutation_matrix(8, 8)
        blocks = [self.modify_matrix(block, permutation_matrix) for block in blocks]
        blocks = [self.dct.apply_idct(block) for block in blocks]
        return self.from_normalized_rgb(image, MAX_RGB_VALUE, blocks)

    def unscramble(self, scrambled_image, seed, p, n):
        self.bernoulli = Bernoulli(seed, p)
        blocks = self.convert_to_blocks(scrambled_image)
        blocks = [self.dct.apply_dct(block) for block in blocks]
        permutation_matrix = self.bernoulli.generate_permutation_matrix(8, 8)
        inv_permutation_matrix = np.argsort(permutation_matrix.flat).reshape(8, 8)
        blocks = [self.modify_matrix(block, inv_permutation_matrix) for block in blocks]
        blocks = [self.dct.apply_idct(block) for block in blocks]
        return self.from_normalized_rgb(scrambled_image, MAX_RGB_VALUE, blocks)

    def from_normalized_rgb(self, image, MAX, blocks):
        blocks = list(blocks)
        unscrambled_image = Image.new('RGB', image.size)
        width, height = image.size
        for i in range(0, height, 8):
            for j in range(0, width, 8):
                block_width_size = width // 8
                block = blocks[block_width_size * (i // 8) + (j // 8)]
                for k in range(i, i + 8):
                    for l in range(j, j + 8):
                        colors = block[k - i, l - j]
                        colors = np.clip(colors, 0, 255).astype(int)
                        unscrambled_image.putpixel((l, k), tuple(colors))
        return unscrambled_image

    def convert_to_blocks(self, image):
        blocks = []
        width, height = image.size
        block_width_size = width // 8  # Исправлено здесь
        for i in range(0, height, 8):
            for j in range(0, width, 8):
                block = np.zeros((8, 8, 3))
                for k in range(i, i + 8):
                    for l in range(j, j + 8):
                        r, g, b = image.getpixel((l, k))
                        block[k - i, l - j] = [r, g, b]  # Store colors in 3D array
                blocks.append(block)
        return blocks

    def border_value(self, value):
        if value < 0:
            return 0
        elif value > 1:
            return 1
        else:
            return value

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

def main():
    scrambler = Scrambler()

    source_image = Image.open("123.jpg")
    scrambled_image = scrambler.scramble(source_image, 12425245, 0.1, 2)
    scrambled_image.save("image1_s.png")

    source_image_data = np.array(source_image)
    scrambled_image_data = np.array(scrambled_image)
    print("PSNR: ", calculate_psnr(source_image_data, scrambled_image_data))

    unscrambled_image = scrambler.unscramble(scrambled_image, 12425245, 0.1, 2)
    unscrambled_image.save("image1_uns.png")

    unscrambled_image_data = np.array(unscrambled_image)
    print("PSNR(for unscrambled): ", calculate_psnr(source_image_data, unscrambled_image_data))

if __name__ == "__main__":
    main()
