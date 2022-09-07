def noisy_terrain(PerlinNoise, y_x, y, chunks_list, chunk_identifier):
    blockIndex = gettBlockIndex(chunk_id=1, xy=(y_x[0], y), chunks_list=chunks_list)

    chunk_block = get_blocks_chunks_list(index=len(chunks_list)-1, chunks_list=chunks_list)[blockIndex]

    minimum_layer = 10

    # Minimum Grass Block layer
    if chunk_block.getGridCoords()[1] == minimum_layer:
        setBlock(chunk_id=chunk_identifier, block_index=blockIndex, block_id=1, noise_gen=None, chunks_list=chunks_list)

    # Dirt Block with noise
    if chunk_block.getGridCoords()[1] < (minimum_layer-2) - PerlinNoise:
        setBlock(chunk_id=chunk_identifier, block_index=blockIndex, block_id=3, noise_gen=PerlinNoise, chunks_list=chunks_list)

    # Grass Block with noise
    if chunk_block.getGridCoords()[1] == (minimum_layer-2) - int(PerlinNoise):
        setBlock(chunk_id=chunk_identifier, block_index=blockIndex, block_id=1, noise_gen=PerlinNoise, chunks_list=chunks_list)

    # Minimum Dirt Block layer
    if chunk_block.getGridCoords()[1] < minimum_layer:
        setBlock(chunk_id=chunk_identifier, block_index=blockIndex, block_id=3, noise_gen=None, chunks_list=chunks_list)

    # Stone Block with noise
    if chunk_block.getGridCoords()[1] < (minimum_layer-6) - int(PerlinNoise):
        setBlock(chunk_id=chunk_identifier, block_index=blockIndex, block_id=2, noise_gen=PerlinNoise, chunks_list=chunks_list)

    # Minimum Stone Block layer
    if chunk_block.getGridCoords()[1] <= minimum_layer-5:
        setBlock(chunk_id=chunk_identifier, block_index=blockIndex, block_id=2, noise_gen=None, chunks_list=chunks_list)

    # Bedrock
    if chunk_block.getGridCoords()[1] == 0:
        setBlock(chunk_id=chunk_identifier, block_index=blockIndex, block_id=4, noise_gen=PerlinNoise, chunks_list=chunks_list)



def get_blocks_chunks_list(index, chunks_list):
	return chunks_list[index].blocks

def setBlock(chunk_id, block_index, block_id, noise_gen, chunks_list):
	blocks = get_blocks_chunks_list(len(chunks_list)-1, chunks_list=chunks_list)

	blocks[block_index].setBlock(block_id, noiseValue=noise_gen)

def gettBlockIndex(chunk_id, xy, chunks_list):
	blocks = get_blocks_chunks_list(len(chunks_list)-1, chunks_list)

	block_index = 0

	for s in range(len(blocks)):
		if blocks[s].getGridCoords() == xy:
			block_index = s
			break

	return block_index