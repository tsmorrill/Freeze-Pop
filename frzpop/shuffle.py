from additives import list_reader, sip_water


def plain_hunt(row):
    """Genterate plain hunt method permutations of row."""
    length = len(row)
    l_mod_2 = length % 2
    row_copy = row.copy()

    pairs_count = length // 2
    period = 2*length

    rows = [row_copy]
    for t in range(period - 1):
        t_mod_2 = t % 2
        pairs_adjust = t_mod_2 * (1 - l_mod_2)  # don't adjust if length is odd
        for n in range(pairs_count - pairs_adjust):
            index = 2*n + t_mod_2
            row[index], row[index + 1] = row[index + 1], row[index]
        row_copy = row.copy()
        rows.append(row_copy)

    return list_reader(rows)


if __name__ == "__main__":
    sip_water()
    ph = plain_hunt([3, 2, 1])
    for _ in range(8):
        print(ph())
