import json
import os

from files.Game import chunks_list

def create_folder(dir):
    try:
        os.makedirs(name=dir)
    except FileExistsError:
        return f"There is already a folder named {dir}"

def chunk_saving():
    # Make a foder that will store the loaded chunks from the game
    create_folder(dir="saves/chunks")

    for i in range(len(chunks_list)):
        F_r = open(f"saves/chunks/chunk{i}.txt", "w+")

        for j in range(len(chunks_list[i]["BLOCKS"])):
            blocks_data = f"{chunks_list[i]['BLOCKS'][j].getId()}-{chunks_list[i]['BLOCKS'][j].getGridCoords()}"

            F_r.writelines(f"{blocks_data}\n")

        F_r.close()

def save():
    chunk_saving()

    