import os

def read_chunks(chunks_list):
    # See the content of the chunk folder
    folder_content = os.listdir("saves/chunks")


    chunk_data = []
    return_chunks_list = chunks_list
    #print(chunks_list)
    #print(return_chunks_list)
    for i in range(len(folder_content)):
        Read_Chunk = open(f"saves/chunks/{folder_content[i]}", "r")

        chunk_data.append([])

        chunk_readLines = Read_Chunk.readlines()

        for k in range(len(chunk_readLines)):
            chunk_data[i].append(str(chunk_readLines[k]).replace("\n", "").split("-"))


    for j in range(len(chunk_data)): # chunk_data lenght its the same as chunks_list (IT WILL CHANGE LATER)
        print("J:",j)
        for b in range(len(return_chunks_list[j]["BLOCKS"])):
            block_id = int(chunk_data[j][b][0])
            grid_pos = chunk_data[j][b][1]

            # Seek for a block that has the same position
            for s in range(len(return_chunks_list[j]["BLOCKS"])):
                if return_chunks_list[j]["BLOCKS"][b].getGridCoords() == return_chunks_list[j]["BLOCKS"][s].getGridCoords():
                    return_chunks_list[j]["BLOCKS"][b].setBlock(id=block_id)

    return return_chunks_list

def read_save_files(chunks_list):
    return read_chunks(chunks_list)