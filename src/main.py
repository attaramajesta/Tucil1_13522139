import time
import sys
import random
import numpy as np

def cli_input():
    while True:
        try:
            num_unique_tokens = int(input("\nJumlah token: "))
            tokens = input("Masukkan token (dipisahkan spasi): ").split()
            if len(tokens) < num_unique_tokens:
                raise ValueError("Tidak sesuai dengan jumlah token unik.")
            buffer_size = int(input("Masukkan ukuran buffer: "))
            matrix_size = tuple(map(int, input("Masukkan ukuran matriks (baris kolom): ").split()))
            num_sequences = int(input("Masukkan jumlah sekuens: "))
            max_sequence_size = int(input("Masukkan ukuran maksimal sekuens: "))

            matrix = np.random.choice(tokens, matrix_size)

            sequences = []
            for _ in range(num_sequences):
                sequence = ''.join(random.choices(tokens, k=max_sequence_size))
                reward = random.choice([10, 20, 30])
                sequences.append((sequence, reward))

            return buffer_size, matrix, sequences

        except ValueError:
            print("Error: Input tidak sesuai. Proses input diulang... \n\n")

def file_input(filename):
    with open(filename, 'r') as file:
        buffer_size = int(file.readline())
        matrix_size = tuple(map(int, file.readline().split()))
        matrix = np.array([file.readline().split() for _ in range(matrix_size[0])])
        num_of_sequences = int(file.readline())
        sequences = []
        for _ in range(num_of_sequences):
            sequence = ''.join(file.readline().split())
            reward = int(file.readline())
            sequences.append((sequence, reward))
    return buffer_size, matrix, sequences

def KMPSearch(pat, txt, lps_cache):
    if (pat, txt) in lps_cache:
        return lps_cache[(pat, txt)]

    M = len(pat)
    N = len(txt)
    lps = [0] * M
    j = 0
    found = 0

    length = 0
    lps[0] = 0
    i = 1

    while i < M:
        if pat[i] == pat[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    i = 0
    while (N - i) >= (M - j):
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            found += 1
            j = lps[j - 1]

        elif i < N and pat[j] != txt[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    lps_cache[(pat, txt)] = found
    return found


def calculate_reward(path, sequences, lps_cache):
    reward = 0
    path_str = ''.join(path)
    for sequence, reward_value in sequences:
        found = KMPSearch(sequence, path_str, lps_cache)
        if found != 0:
            reward += found * reward_value
    return reward

def search_token(matrix, sequences, x, y, visited, path, max_path, max_reward, lps_cache, buffer_size):
    rows, cols = matrix.shape

    if x < 0 or x >= rows or y < 0 or y >= cols or visited[x][y]:
        return

    visited[x][y] = True
    path.append((x, y, matrix[x, y]))

    if len(path) == buffer_size:
        reward = calculate_reward([id for _, _, id in path], sequences, lps_cache)
        if reward > max_reward[0]:
            max_reward[0] = reward
            max_path.clear()
            max_path.extend(path)
    else:
        if len(path) % 2 == 0:
            for j in range(-(rows - 1), rows - 1):
                if j != 0:
                    search_token(matrix, sequences, x, y + j, visited, path, max_path, max_reward, lps_cache, buffer_size)
        elif len(path) % 2 == 1:
            for i in range(-(cols - 1), cols - 1):
                if i != 0:
                    search_token(matrix, sequences, x + i, y, visited, path, max_path, max_reward, lps_cache, buffer_size)

    visited[x][y] = False
    path.pop()

def find_buffer(buffer_size, matrix, sequences, lps_cache):
    rows, cols = matrix.shape
    max_reward = [0]
    max_path = []
    visited = np.zeros_like(matrix, dtype=bool)

    for j in range(cols):
        search_token(matrix, sequences, 0, j, visited, [], max_path, max_reward, lps_cache, buffer_size)

    return max_path

def save_all_paths(filename, max_path, execution_time, reward):
    with open(filename, 'w') as file:
        file.write(f'Reward: {reward}\n')
        file.write('Path: ' + ' -> '.join([f'{y + 1},{x + 1}' for x, y, _ in max_path]) + '\n')
        file.write('IDs: ' + ' '.join([id for _, _, id in max_path]) + '\n\n')
        file.write(execution_time + '\n')

if __name__ == "__main__":
    print("\nWELCOME!\n\nApakah Anda ingin menggunakan input dari file atau generate input?")
    print("1. File\n2. Generate\n")
    choice = input("Pilihan: ")
    if choice == "1":
        buffer_size, matrix, sequences = file_input('input.txt')
    elif choice == "2":
        buffer_size, matrix, sequences = cli_input()
    else:
        print("Error: Pilihan tidak valid. Keluar... \n\n")
        sys.exit(1)

    lps_cache = {}
    start_time = time.time()
    max_path = find_buffer(buffer_size, matrix, sequences, lps_cache)
    reward = calculate_reward([id for _, _, id in max_path], sequences, lps_cache)
    execution_time = f'{(time.time() - start_time) * 1000:.2f} ms'

    if choice == "2":
        print("\nMATRIX:\n")
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                print(matrix[i, j], end=' ')
            print()
        print("\nSEQUENCES:\n")
        for seq, reward in sequences:
            print(seq)
            print(reward)

    if reward == 0:
        print("\nTidak ada path yang memenuhi syarat.")
    else:
        print(f'\n{reward}')
        print(' '.join([id for _, _, id in max_path]))
        print('\n'.join([f'{y + 1},{x + 1}' for x, y, _ in max_path]) + '\n')

    print(execution_time + '\n')
    save = input("Apakah Anda ingin menyimpan hasil ke file? (y/n): ")
    if save == "y":
        save_all_paths('output.txt', max_path, execution_time, reward)
        print("Berhasil disimpan ke 'output.txt'.\n\n")
    else:
        print("Keluar... \n\n")
        sys.exit(1)
