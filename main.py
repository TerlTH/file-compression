import heapq
import os

class HuffmanNode:
    def __init__(self, data, frequency):
        self.data = data
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

class HuffmanCoding:
    def __init__(self):
        self.codes = {}

    def build_huffman_tree(self, frequencies):
        min_heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
        heapq.heapify(min_heap)

        while len(min_heap) > 1:
            left = heapq.heappop(min_heap)
            right = heapq.heappop(min_heap)

            new_node = HuffmanNode('\0', left.frequency + right.frequency)
            new_node.left = left
            new_node.right = right

            heapq.heappush(min_heap, new_node)

        return min_heap[0] if min_heap else None

    def generate_codes(self, root, code=""):
        if root is not None:
            if root.data != '\0':
                self.codes[root.data] = code
            self.generate_codes(root.left, code + '0')
            self.generate_codes(root.right, code + '1')

    def compress_file(self, file_path):
        frequencies = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for char in file.read():
                frequencies[char] = frequencies.get(char, 0) + 1

        root = self.build_huffman_tree(frequencies)
        self.generate_codes(root)

        compressed_data = ""
        with open(file_path, 'r', encoding='utf-8') as file:
            compressed_data = ''.join(self.codes[char] for char in file.read())

        return compressed_data

    def write_compressed_file(self, file_path, compressed_data):
        output_file_path = file_path + "_compressed.txt"
        with open(output_file_path, 'w', encoding='utf-8') as file:
            for char, code in self.codes.items():
                file.write(f"{char} {code}\n")
            file.write("\n")
            file.write(compressed_data)

        print(f"Файл {output_file_path} создан.")


if __name__ == "__main__":
    file_path = "input.txt"

    huffman = HuffmanCoding()
    compressed_data = huffman.compress_file(file_path)

    if compressed_data:
        huffman.write_compressed_file(file_path, compressed_data)
        print("Файл создан.")
