import copy
from math import ceil

def get_items_total_volume(item_list):
    volume_T = 0
    for item in item_list:
        volume = item.width * item.height * item.depth
        volume_T += volume

    return volume_T

def sort_by_volume(item_list):
    for i in range(len(item_list)):
        for j in range(len(item_list)):
            if item_list[i].width * item_list[i].height * item_list[i].depth > item_list[j].width * item_list[j].height * item_list[j].depth:
                item_list[i], item_list[j] = item_list[j], item_list[i]

    return item_list

def bp3D(current_bin, Items):
    # Documentation link from where the strategy was taken.
       # https://www.researchgate.net/publication/228974015_Optimizing_Three-Dimensional_current_bin_Packing_Through_Simulation
    # Consider that the strategy and the algorithm from this code have been changed for my needs.
    notPacked = copy.deepcopy(Items)

    # sort items by volume
    notPacked = sort_by_volume(notPacked)

    if len(current_bin.items) == 0:
        # put the first item in the current_bin
        for j in range(len(notPacked)):
            for i in range(6):
                if notPacked[j].rotate(i)[0] > current_bin.width or \
                    notPacked[j].rotate(i)[1] > current_bin.height or \
                    notPacked[j].rotate(i)[2] > current_bin.depth:
                    pass
                else:
                    current_bin.pack(notPacked[j], (0, 0, 0), i)
                    del notPacked[j]
                    break
            if len(current_bin.items) != 0:
                break
    if len(current_bin.items) == 0:
        return Items

    while True:
        # if no change is detected the loop will stop
        not_changes = True

        for i in range(len(notPacked)):
            current_item = notPacked[i]

            for j in range(len(current_bin.items)):
                current_bin_item = current_bin.items[j]

                # choose the available position
                for p in range(3):
                    pivot = [-1, -1, -1]

                    if p == 0: # back lower right corner of current_bin_item
                        pivot = [
                            current_bin_item.pos[0] + current_bin_item.rotate(current_bin_item.RT)[0],
                            current_bin_item.pos[1],
                            current_bin_item.pos[2]
                        ]
                    elif p == 1: # front lower left corner
                        pivot = [
                            current_bin_item.pos[0],
                            current_bin_item.pos[1],
                            current_bin_item.pos[2] + current_bin_item.rotate(current_bin_item.RT)[2]
                        ]
                    else: # back upper left corner
                        pivot = [
                            current_bin_item.pos[0],
                            current_bin_item.pos[1] + current_bin_item.rotate(current_bin_item.RT)[1],
                            current_bin_item.pos[2]
                        ]

                    # try to find a rotation type for packaging
                    for k in range(6):
                        if current_bin.can_be_packed(current_item, pivot, k):
                            current_bin.pack(current_item, pivot, k)
                            del notPacked[i]
                            not_changes = False
                            break

                    if not_changes == False:
                        break

                if not_changes == False:
                    break

            if not_changes == False:
                break

        if not_changes:
            break

    return notPacked