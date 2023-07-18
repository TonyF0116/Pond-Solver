def get_block_indices(blocks, block_index):
    indices = []
    for i in range(len(blocks)):
        if blocks[i] == block_index:
            indices.append(i)
    return indices


def blocks_to_map(blocks):
    result = ['00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',
              '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']
    for i in range(1, len(blocks)):
        block = blocks[i]
        if block[2] == 'Horizontal':
            for j in range(block[4], block[6]+1):
                if block[0] < 10:
                    result[block[3]*6+j] = '0' + str(block[0])
                else:
                    result[block[3]*6+j] = str(block[0])
        elif block[2] == 'Vertical':
            for j in range(block[3], block[5]+1):
                if block[0] < 10:
                    result[6*j+block[4]] = '0' + str(block[0])
                else:
                    result[6*j+block[4]] = str(block[0])
        else:
            print('Invalid orientation')
            exit()

    return ''.join(result)


def map_to_blocks(original_map):
    map = []
    # print(original_map)
    for i in range(0, len(original_map), 2):
        map.append(original_map[i:i+2])
    result = []
    result.append(['Empty'])
    for i in range(1, 19):
        block = [0, 'Color', 'Orientation', -1, -1, -1, -1]
        if i < 10:
            indices = get_block_indices(map, '0'+str(i))
        else:
            indices = get_block_indices(map, str(i))
        if len(indices) == 0:
            break
        elif len(indices) == 2:
            if i == 1:
                block[0] = 1
                block[1] = 'Red'
                block[2] = 'Horizontal'
                block[3] = 2
                block[4] = indices[0] - 12
                block[5] = 2
                block[6] = indices[1] - 12
            else:
                if indices[1]-indices[0] == 1:
                    block[0] = i
                    block[1] = 'Yellow'
                    block[2] = 'Horizontal'
                    block[3] = int(indices[0] / 6)
                    block[4] = indices[0] - 6 * block[3]
                    block[5] = block[3]
                    block[6] = indices[1] - 6 * block[3]
                else:
                    block[0] = i
                    block[1] = 'Yellow'
                    block[2] = 'Vertical'
                    block[3] = int(indices[0] / 6)
                    block[4] = indices[0] % 6
                    block[5] = int(indices[1] / 6)
                    block[6] = indices[1] % 6
        elif len(indices) == 3:
            if indices[1]-indices[0] == 1:
                block[0] = i
                block[1] = 'Blue'
                block[2] = 'Horizontal'
                block[3] = int(indices[0] / 6)
                block[4] = indices[0] - 6 * block[3]
                block[5] = block[3]
                block[6] = indices[2] - 6 * block[3]
            else:
                block[0] = i
                block[1] = 'Blue'
                block[2] = 'Vertical'
                block[3] = int(indices[0] / 6)
                block[4] = indices[0] % 6
                block[5] = int(indices[2] / 6)
                block[6] = indices[2] % 6
        else:
            print('Invalid block length')
            exit()

        result.append(block)
    return result


# Takes in the current blocks, return the map format of all possible moves
def get_possible_moves(blocks):
    result = []
    original_map = blocks_to_map(blocks)
    map = []
    for i in range(0, len(original_map), 2):
        map.append(original_map[i:i+2])

    for i in range(1, len(blocks)):
        block = blocks[i]
        # print(block)
        if block[2] == 'Horizontal':
            start = block[3] * 6 + block[4]
            end = block[5] * 6 + block[6]
            for j in range(start-1, block[3]*6-1, -1):
                if map[j] == '00':
                    displacement = start - j
                    tmp = list(map)  # Used to get a deep copy of map
                    if block[0] < 10:
                        for k in range(start, end+1):
                            tmp[k] = '00'
                            tmp[k-displacement] = '0' + str(block[0])
                    else:
                        for k in range(start, end+1):
                            tmp[k] = '00'
                            tmp[k-displacement] = str(block[0])
                    result.append(''.join(tmp))
                else:
                    break

            for j in range(end+1, block[3]*6+6):
                if map[j] == '00':
                    displacement = j - end
                    tmp = list(map)
                    if block[0] < 10:
                        for k in range(end, start-1, -1):
                            tmp[k] = '00'
                            tmp[k+displacement] = '0' + str(block[0])
                    else:
                        for k in range(end, start-1, -1):
                            tmp[k] = '00'
                            tmp[k+displacement] = str(block[0])
                    # print(''.join(tmp))
                    result.append(''.join(tmp))
                else:
                    break

        elif block[2] == 'Vertical':
            start = block[3] * 6 + block[4]
            end = block[5] * 6 + block[6]

            for j in range(start-6, -1, -6):
                if map[j] == '00':
                    displacement = start - j
                    tmp = list(map)
                    if block[0] < 10:
                        for k in range(start, end+1, 6):
                            tmp[k] = '00'
                            tmp[k-displacement] = '0' + str(block[0])
                    else:
                        for k in range(start, end+1, 6):
                            tmp[k] = '00'
                            tmp[k-displacement] = str(block[0])
                    result.append(''.join(tmp))
                else:
                    break

            for j in range(end+6, 36, 6):
                if map[j] == '00':
                    displacement = j - end
                    tmp = list(map)
                    if block[0] < 10:
                        for k in range(end, start-1, -6):
                            tmp[k] = '00'
                            tmp[k+displacement] = '0' + str(block[0])
                    else:
                        for k in range(end, start-1, -6):
                            tmp[k] = '00'
                            tmp[k+displacement] = str(block[0])
                    # print(''.join(tmp))
                    result.append(''.join(tmp))
                else:
                    break
    return result


def solved(blocks):
    original_map = blocks_to_map(blocks)
    map = []
    for i in range(0, len(original_map), 2):
        map.append(original_map[i:i+2])
    for i in range(17, 12, -1):
        if map[i] == '00':
            continue
        elif map[i] == '01':
            return True
        else:
            break
    return False

# def print_map(map):
#     txt = ''
#     for i in range(6):
#         for j in range(0, 12, 2):
#             txt += map[12*i+j:12*i+j+2] + ' '
#         txt += '\n'
#     print(txt)


# The graph for the solver is tree like
# Each blocks have n children, where n refers to the sum of all possible moves from the current blocks
# Use BFS to find the solution with the least moves, then use backtracking to get the solution
def solver(blocks):
    first_map = blocks_to_map(blocks)
    visited = set()  # Set of visited maps
    added = set()
    added.add(first_map)
    to_visit = []  # List of maps to visit
    backtracking = {}  # blocks of children/parent relation between maps
    to_visit.append(first_map)

    last_visited = first_map

    solution_generated = False

    while len(to_visit) != 0:
        # print(len(to_visit))
        cur_map = to_visit.pop(0)
        if cur_map in visited:
            continue
        # print_map(cur_map)
        cur_blocks = map_to_blocks(cur_map)

        visited.add(cur_map)

        if solved(cur_blocks):
            last_visited = cur_map
            solution_generated = True
            break

        possible_moves = get_possible_moves(cur_blocks)
        for move in possible_moves:
            if move in visited or move in added:
                continue
            else:
                # print_map(move)
                to_visit.append(move)
                added.add(move)
                backtracking[move] = cur_map

    if not solution_generated:
        return []

    result = []  # Result in map format
    result.append(last_visited)
    index = 0
    while backtracking.get(result[index]) != None:
        result.append(backtracking[result[index]])
        index += 1
    result.reverse()
    result_blocks = []
    for element in result:
        result_blocks.append(map_to_blocks(element))
    return result_blocks


if __name__ == "__main__":
    # Map format: Row by row, separated by space between each row
    # sample_map = '220356 000356 110450 800477 890000 890000'
    # blocks starting from 1, where 1 is always the red block, 0 reserved for blanks
    sample_blocks = [['Empty'], [1, 'Red', 'Horizontal', 2, 0, 2, 1], [2, 'Yellow', 'Horizontal', 0, 0, 0, 1], [3, 'Yellow', 'Horizontal', 4, 2, 4, 3], [4, 'Yellow', 'Horizontal', 5, 2, 5, 3], [5, 'Yellow', 'Horizontal', 5, 4, 5, 5], [6, 'Yellow', 'Horizontal', 3, 4, 3, 5], [
        7, 'Yellow', 'Vertical', 0, 3, 1, 3], [8, 'Yellow', 'Vertical', 0, 5, 1, 5], [9, 'Yellow', 'Vertical', 2, 3, 3, 3], [10, 'Yellow', 'Vertical', 4, 1, 5, 1], [11, 'Blue', 'Vertical', 3, 0, 5, 0], [12, 'Blue', 'Vertical', 0, 4, 2, 4]]
    # Format: Index, Color, Orientation, x1, y1, x2, y2, ordering in x1, y1 smaller than x2, y2
    # sample_blocks[1] = ['1', 'Red', 'Horizontal', 2, 0, 2, 1]
    # print(blocks_to_map(sample_blocks))
    # print(solved(map_to_blocks(sample_map)))
    # sample_blocks = map_to_blocks(sample_map)
    print(solver(sample_blocks))
