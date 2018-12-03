import numpy as np

if __name__ == '__main__':
    claims = []
    with open('input.txt', encoding='utf-8') as lines:
        for line in lines:
            row, at, coord, size = line.replace('\n', '').split(' ')
            coord = [int(i) for i in coord[:-1].split(',')]
            size = [int(i) for i in size.split('x')]
            claims.append((coord, size))

    claims = np.array(claims)
    coords = claims[:, 0, :]
    sizes = claims[:, 1, :]
    matrix_range = (coords[:, 0].max() + sizes[:, 0].max(), coords[:, 1].max() + sizes[:, 1].max())
    matrix = np.zeros(matrix_range, dtype=np.int32)

    for claim in claims:
        coord = claim[0]
        size = claim[1]
        matrix[coord[0]:coord[0] + size[0], coord[1]:coord[1] + size[1]] += 1

    print(np.sum(matrix > 1))
