# Levenshtein editing distance algorithm
def calc_edit_distance(s1:str, s2:str):
    l1 = len(s1)
    l2 = len(s2)
    table = []

    for y in range(l2+1):
        if y == 0:
            table.append(list(range(l1+1)))
        else:
            table.append([0]*(l1 + 1))
        table[y][0] = y

    for x in range(1, l1+1):
        for y in range(1, l2+1):
            temp = 1
            if s1[x-1] == s2[y-1]:
                temp = 0
            table[y][x] = min(table[y][x-1] + 1, table[y-1][x] + 1, table[y-1][x-1]+temp)
    return table[-1][-1]


def calc_similarities(s1:str, s2:str):
    return 1 - calc_edit_distance(s1, s2) / max(len(s1), len(s2))


if __name__ == '__main__':
    print(calc_edit_distance('听说马上就要放假了','你听说要放假了'))
    print(calc_similarities('abc', 'abe'))