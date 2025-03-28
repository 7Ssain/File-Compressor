import heapq
from collections import defaultdict
import os
import json
import hashlib


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCompressor:
    def __init__(self):
        """
        Initialize Huffman Compressor
        """
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    def _make_frequency_dict(self, text):
        """
        Create frequency dictionary for characters
        """
        frequency = defaultdict(int)
        for character in text:
            frequency[character] += 1
        return frequency

    def _build_heap(self, frequency):
        """
        Build priority queue (heap) from frequency dictionary
        """
        for key in frequency:
            node = HuffmanNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def _merge_nodes(self):
        """
        Merge nodes to build Huffman tree
        """
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def _make_codes_helper(self, root, current_code):
        """
        Recursively generate Huffman codes
        """
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self._make_codes_helper(root.left, current_code + "0")
        self._make_codes_helper(root.right, current_code + "1")

    def _get_encoded_text(self, text):
        """
        Convert text to Huffman encoded binary string
        """
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def _pad_encoded_text(self, encoded_text):
        """
        Pad encoded text to make its length a multiple of 8
        """
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def _get_byte_array(self, padded_encoded_text):
        """
        Convert binary string to byte array
        """
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress_file(self, path, output_path=None):
        """
        Compress a file using Huffman coding
        """
        # Read file
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Compute file hash for verification
        file_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

        # Reset compression state
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

        # Create frequency dictionary
        frequency = self._make_frequency_dict(text)

        # Build Huffman tree
        self._build_heap(frequency)
        self._merge_nodes()

        # Generate Huffman codes
        root = self.heap[0]
        self._make_codes_helper(root, "")

        # Encode text
        encoded_text = self._get_encoded_text(text)
        padded_encoded_text = self._pad_encoded_text(encoded_text)

        # Convert to bytes
        byte_array = self._get_byte_array(padded_encoded_text)

        # Determine output path
        if output_path is None:
            output_path = path + '.huffman'

        # Write compressed file with metadata
        with open(output_path, 'wb') as output:
            # Write file hash
            output.write(file_hash.encode('utf-8') + b'\n')

            # Write frequency dictionary as JSON
            freq_json = json.dumps(frequency)
            output.write(freq_json.encode('utf-8') + b'\n')

            # Write compressed data
            output.write(byte_array)

        # Compression ratio
        original_size = len(text.encode('utf-8'))
        compressed_size = len(byte_array)
        compression_ratio = 1 - (compressed_size / original_size)
        print(f"Compression complete. Ratio: {compression_ratio:.2%}")

        return output_path

    def decompress_file(self, path, output_path=None):
        """
        Decompress a Huffman compressed file
        """
        # Read compressed file
        with open(path, 'rb') as file:
            # Read file hash
            file_hash = file.readline().decode('utf-8').strip()

            # Read frequency dictionary
            freq_json = file.readline().decode('utf-8').strip()
            frequency = json.loads(freq_json)

            # Read compressed data
            byte_array = file.read()

        # Reset decompression state
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

        # Rebuild Huffman tree
        self._build_heap(frequency)
        self._merge_nodes()
        root = self.heap[0]
        self._make_codes_helper(root, "")

        # Convert bytes to bit string
        bit_string = ''.join(["{0:08b}".format(byte) for byte in byte_array])

        # Remove padding information
        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)
        bit_string = bit_string[8:]
        encoded_text = bit_string[:-1 * extra_padding]

        # Decode text
        decompressed_text = self._decode_text(encoded_text, root)

        # Verify integrity
        current_hash = hashlib.sha256(decompressed_text.encode('utf-8')).hexdigest()
        if current_hash != file_hash:
            raise ValueError("File integrity check failed")

        # Determine output path
        if output_path is None:
            output_path = path.replace('.huffman', '.decompressed')

        # Write decompressed file
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decompressed_text)

        print("Decompression complete. File integrity verified.")
        return output_path

    def _decode_text(self, encoded_text, root):
        """
        Decode Huffman encoded text
        """
        current = root
        decoded_text = ""

        for bit in encoded_text:
            if bit == '0':
                current = current.left
            else:
                current = current.right

            if current.char is not None:
                decoded_text += current.char
                current = root

        return decoded_text


def main():
    """
    Example usage of HuffmanCompressor
    """
    compressor = HuffmanCompressor()

    try:
        # Compress a file
        compressed_file = compressor.compress_file('example.txt')
        print(f"Compressed file saved as: {compressed_file}")

        # Decompress the file
        decompressed_file = compressor.decompress_file(compressed_file)
        print(f"Decompressed file saved as: {decompressed_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()