<h1>Huffman-compression schoolproject</h1>
<hr>
<p><strong>assignment:</strong></p>
<p>Make a working algorithm to compress files using the hoffman algorithm</p>
<hr>
<p><strong>file explanation:</strong></p>
<p>The: "Huffman app exe" folder contains an executeable that does exactly the same as the "main.py" file. It is a GUI that takes a textfile and compresses it and gives you the option to decompress it.<br><br>
The: "tree_code_generator.py" is a script that takes a string and generates a huffman tree for the string and converts the string into a huffmanencoded string.<br><br>
The: "bytewriter.py" is a script that takes the tree and the encoded string from the treegenerator and makes them writeable in bytes and writes them to a ".onno" file according to the byteformat specified in the "bytestructure.txt" where each value between curlybraces represents a byte.<br><br>
The: "bytereader.py" is a script that can read ".onno" files and translates them back into their original ".txt form.</p>
<hr>
<p><strong>FYI:</strong></p>
<p>I only know that it works on ".txt" files. I tested on base64 encoded strings of images but didn't find any luck compressing images like that. Just a fun project I consider finished.</p>
