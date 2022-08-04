import json
import os

def create_folder(dir):
    try:
        os.makedirs(name=dir)
    except FileExistsError:
        return f"There is already a folder named {dir}"

def chunk_saving(chunks_list):
    # Make a foder that will store the loaded chunks from the game
    create_folder(dir="saves/chunks")

    for i in range(len(chunks_list)):
        F_r = open(f"saves/chunks/chunk{i}.txt", "w+")

        # transfom the blocks list in a json file
        blocks_position_json = json.dumps(
            obj=get_dict_with_blocks_pos(chunk_id=i, chunks_list=chunks_list)
        )
        
        F_r.writelines(f"{blocks_position_json}")

        F_r.close()

def get_dict_with_blocks_pos(chunk_id:int, chunks_list) -> dict:
    dict_output = {} # Each block type will have positions around the chunk

    for block in chunks_list[chunk_id]["BLOCKS"]:
        if not (block.getId() == 0):
            # Check if there is data in block.getId()
            if not (block.getId() in dict_output.keys()):
                dict_output[block.getId()] = []
            
            dict_output[block.getId()].append(tuple(block.getGridCoords()))

    return dict_output

def save(chunks_list):
    print("Saving game...")
    chunk_saving(chunks_list)
    # Entities saving
    # Other values saving

    