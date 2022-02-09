import os

def read_chunks(chunks_list):
    # See the content of the chunk folder
    folder_content = os.listdir("saves/chunks")

    return_chunks_list = chunks_list
    #print(return_chunks_list)
    for i in range(len(folder_content)):
        Read_Chunk = open(f"saves/chunks/{folder_content[i]}", "r")

        chunk_data = []

        chunk_readLines = Read_Chunk.readlines()
        print(chunk_readLines)

        for i in range(len(chunk_readLines)):
            chunk_data.append(str(chunk_readLines[i]).replace("\n", "").split("-"))

        print(chunk_data)

        for j in range(len(return_chunks_list)):
            for b in range(len(return_chunks_list[j]["BLOCKS"])):
                print(j, b)
                block_id = int(chunk_data[b][0])
                grid_pos = chunk_data[b][1]

                # Seek for a block that has the same position
                for s in range(len(return_chunks_list[j]["BLOCKS"])):
                    if return_chunks_list[j]["BLOCKS"][b].getGridCoords() == return_chunks_list[j]["BLOCKS"][s].getGridCoords():
                        return_chunks_list[j]["BLOCKS"][b].setBlock(id=block_id)

        return_chunks_list.append(chunk_data)

    return return_chunks_list

def read_save_files(chunks_list):
    try:
        return read_chunks(chunks_list)
    except:
        return []