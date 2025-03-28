# File-Compressor
Compression Utility
Overview
This utility implements Huffman coding to compress and decompress text files. It ensures file integrity using a SHA-256 hash and displays the compression ratio after processing.

Setup
Save the Script:

Save the entire script as huffman_compressor.py.

Prepare a Text File:

Create or select a text file you want to compress (e.g., example.txt).

Basic Usage
There are two primary ways to use the compressor:

A. Running the Script Directly
Modify the Main Function:

Edit the main() function within the script to specify your file paths.

Execute the Script:

bash
Copy
python huffman_compressor.py
B. Importing and Using in Another Script
You can import the HuffmanCompressor class and use it in your own Python code:

python
Copy
from huffman_compressor import HuffmanCompressor

# Create a compressor instance
compressor = HuffmanCompressor()

# Compress a file
compressed_file = compressor.compress_file('your_file.txt')

# Decompress the file
decompressed_file = compressor.decompress_file(compressed_file)
Methods Overview
compress_file(input_path, output_path=None)
Description:

Compresses the file located at input_path.

Parameters:

input_path: Path to the file you want to compress.

output_path (optional): Path to save the compressed file.

Returns:

The path of the compressed file.

decompress_file(input_path, output_path=None)
Description:

Decompresses the file located at input_path.

Parameters:

input_path: Path to the compressed file.

output_path (optional): Path to save the decompressed file.

Returns:

The path of the decompressed file.

Example Terminal Commands
Compress a File:

bash
Copy
python huffman_compressor.py compress example.txt
Decompress a File:

bash
Copy
python huffman_compressor.py decompress example.txt.huffman
Key Points
File Type: Works best with text files.

Extension: Compressed files have the .huffman extension.

Integrity: Handles file integrity via SHA-256 hash.

Feedback: Prints compression ratio upon compressing.
