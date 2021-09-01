def list_to_print_str(list, cols=0):
    if cols == 0:
        cols = len(list)

    row_list = []
    while list:
        temp_list = []
        for i in range(cols):
            temp_list.append(list.pop(0))
        row = " ".join(temp_list)
        row_list.append(row)
    return row_list
