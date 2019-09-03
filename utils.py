def coord_to_hand(i, j):
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    c1 = cards[12-i]
    c2 = cards[12-j]

    if i < j:
        return c1 + c2 + 'o' # a little bit backwards with the o and s but whatever
    elif i > j:
        return c2 + c1 + 's'
    else:
        return c1 + c1


def count_combos(i, j, dead_cards=None):
    if dead_cards is None:
        if i < j:
            return 12
        elif i > j:
            return 4
        else:
            return 6
    else:
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        c1 = cards[12-i]
        c2 = cards[12-j]
        c1s = len(set([c1 + 'c', c1 + 'h', c1 + 's', c1 + 'd']) - set(dead_cards))
        c2s = len(set([c2 + 'c', c2 + 'h', c2 + 's', c2 + 'd']) - set(dead_cards))
        if i == j:
            return [0, 0, 1, 3, 6][c1s]
        elif i < j:
            #offsuit
            return c1s * c2s - min(c1s, c2s)
        else:
            return min(c1s, c2s)
