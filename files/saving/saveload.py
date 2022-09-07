import os, json
from files.terrain.chunk import Chunk

def create_folder(dir):
    try:
        os.makedirs(name=dir)
    except FileExistsError:
        return f"There is already a folder named {dir}"

def read_chunks(chunks_list):
    # If it does not exist chunks folder, create it
    create_folder("saves/chunks")
    
    # See the content of the chunk folder
    folder_content = os.listdir("saves/chunks")

    chunk_data = []
    return_chunks_list = chunks_list

    # Open the chunk.txt files and append the data to chunk_data
    for i in range(len(folder_content)):
        Read_Chunk = open(f"saves/chunks/{folder_content[i]}", "r")

        chunk_readLines = Read_Chunk.readlines()

        # Clean the data, and deconvert from json to a normal dict
        deconverted_file = json.loads(chunk_readLines[0]) # Dict type

        # Append the deconverted_file to chunk_data
        for k in range(len(chunk_readLines)):
            chunk_data.append(deconverted_file)

    # Write the data into chunks_list
    for j in range(len(chunk_data)): # chunk_data lenght its the same as chunks_list
        # Get chunk_data[j] keys
        chunk_keys = dict(chunk_data[j]).keys() # Blocks str(id's)
        for b in chunk_keys:
            data_block_id = int(b) # This is integer b
            # Coords_blocks
            for c in range(len(chunk_data[j][b])):
                data_grid_pos = chunk_data[j][b][c]
                
                # Seek for a block that has the same position
                block = return_chunks_list[j].get_block(position=data_grid_pos)
                if block:
                    block.setBlock(id=data_block_id)
                        

    return return_chunks_list

def read_save_files(chunks_list):
    return read_chunks(chunks_list)