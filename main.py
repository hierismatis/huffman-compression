from tkinter import filedialog, ttk
import tkinter as tk

class Node:
    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency
        self.leftChild = None
        self.rightChild = None

def get_data(filename):
    with open(filename, "r") as f:
        text = f.read()
        f.close()
    return text


def build_tree(text):
    frequencies = {}

    for letter in text:
        frequencies[letter] = frequencies.get(letter, 0) + 1

    nodes = [Node(letter, frequencies[letter]) for letter in frequencies]

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda node: node.frequency)

        new_node = Node(None, nodes[0].frequency + nodes[1].frequency)
        new_node.leftChild = nodes[0]
        new_node.rightChild = nodes[1]

        nodes.remove(nodes[0])
        nodes.remove(nodes[0])

        nodes.append(new_node)

    return nodes[0]


def get_codes(node):
    codes = {}

    def get_next_code(node, prefix=''):
        if node.character is not None:
            codes[node.character] = prefix
        else:
            get_next_code(node.leftChild, prefix + '0')
            get_next_code(node.rightChild, prefix + '1')

    get_next_code(node)

    return codes


def huffman_encode(file_path):
    file_name = file_path.split("/")[-1].split(".")
    file_name = f"{file_name[0]}[{file_name[1]}].onno"

    text = get_data(file_path)
    tree = build_tree(text)
    codes = get_codes(tree)
    result = "".join([codes[letter] for letter in text])

    splitcode = []
    for index in range(0, len(result), 8):
        splitcode.append(result[index : index + 8])

    class Byte:
        def __init__(self, char, lenght, key):
            self.char = char
            self.lenght = lenght
            self.key = key

    key_bytes = []

    amount_keys = len(codes)
    for key, value in codes.items():
        key_bytes.append(Byte(ord(key), len(value), value))

    len_last = len(splitcode[-1])
    for byte in key_bytes:

        byte_list = []

    byte_list.append(amount_keys)

    for byte in key_bytes:
        byte_list.append(byte.char)
        byte_list.append(byte.lenght)
        if byte.lenght > 8:
            split = []
            for index in range(len(byte.key), 0, -8):
                step = 8
                if index - 8 <= 0:
                    step = index
                split.append(byte.key[index - step : index])
                split.reverse()
            for i in split:
                byte_list.append(int(i, 2))
        else:
            byte_list.append(int(byte.key, 2))

    byte_list.append(len_last)

    for code in splitcode:
        code = int(code, 2)
        byte_list.append(code)


    with open(file_name, "wb") as f:
        newFileByteArray = bytearray(byte_list)
        print(type(newFileByteArray))
        f.write(newFileByteArray)
        f.close()

def huffman_decode(file_path):
    file_name = file_path.split("/")[-1].split(".")[0][:-1].split("[")
    file_name = f"{file_name[0]}.{file_name[1]}"
    with open(file_path, "rb") as f:
        content = f.read()
        f.close()

    read_bytes = []
    for i in content:
        read_bytes.append(i)


    def filler(string):
        return "0"*(8-len(string))+string

    amount_keys = read_bytes.pop(0)

    keys = {}

    for i in range(amount_keys):
        key_char = read_bytes.pop(0)
        key_len = read_bytes.pop(0)
        if key_len > 8:
            repeats = key_len//8
            key_list = []
            for i in range(0,repeats+1):
                key_list.append(read_bytes.pop(0))
            key = filler(bin(key_list.pop(0))[2:])

            for i in key_list:
                key += filler(bin(i)[2:])

        else:
            key = filler(bin(read_bytes.pop(0))[2:])

        key = key[len(key)-key_len:]

        keys.update({key: chr(key_char)})

    len_last = read_bytes.pop(0)
    last_byte = bin(read_bytes.pop())[2:]
    last_byte = filler(last_byte)[8-len_last:]

    code = ""

    for byte in read_bytes:
        code += filler(bin(byte)[2:])

    code += last_byte

    text = ""
    bfr = ""

    for char in code:
        bfr += char
        if bfr in keys:
            text += keys[bfr]
            bfr = ""

    with open(file_name, "w") as f:
        f.write(text)
        f.close()

def get_filepath(encode=True):
    if encode:
        global encode_filepath
        encode_filepath = tk.filedialog.askopenfilename(initialdir = "\\",title = "Select file",filetypes = (("all files","*.*"),))
        encode_file_name_label.config(text=f"filename:\n{encode_filepath}\n")
        encode_button.config(state=tk.NORMAL)
    else:
        global decode_filepath
        decode_filepath = tk.filedialog.askopenfilename(initialdir = "\\",title = "Select file",filetypes = (("huffman files","*.onno"),))
        decode_file_name_label.config(text=f"filename:\n{decode_filepath}\n") 
        decode_button.config(state=tk.NORMAL)

encode_filepath = ""
decode_filepath = ""

root = tk.Tk()
root.title("Huffman")
root.geometry("500x300")


my_notebook = ttk.Notebook(root)
my_notebook.pack(fill="both", expand=1)

encode_frame = tk.Frame(my_notebook, width=500, height=500)
encode_frame.pack(fill="both", expand=1)

decode_frame = tk.Frame(my_notebook, width=500, height=500)
decode_frame.pack(fill="both", expand=1)

my_notebook.add(encode_frame, text="Encode")
my_notebook.add(decode_frame, text="Decode")

encode_message = tk.Label(encode_frame, text="\nEncode your file with huffman encoding and reduce the size!\n", font="10")
encode_message.pack()
encode_select_file = tk.Button(encode_frame, text="Select your file to encode", command=get_filepath)
encode_select_file.pack()
encode_file_name_label = tk.Label(encode_frame, text="\nfilename:\n")
encode_file_name_label.pack()
encode_button = tk.Button(encode_frame, text="Start encoding", command=lambda: huffman_encode(encode_filepath), state=tk.DISABLED)
encode_button.pack()

decode_message = tk.Label(decode_frame, text="\nDecode the file you encoded using our algorithm!\n", font="10")
decode_message.pack()
decode_select_file = tk.Button(decode_frame, text="Select your file to decode", command=lambda: get_filepath(False))
decode_select_file.pack()
decode_file_name_label = tk.Label(decode_frame, text="\nfilename:\n")
decode_file_name_label.pack()
decode_button = tk.Button(decode_frame, text="Start decoding", command=lambda: huffman_decode(decode_filepath), state=tk.DISABLED)
decode_button.pack()

root.mainloop()
