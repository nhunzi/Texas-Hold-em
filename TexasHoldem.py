import random


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def get_val(self):
        return self.value

    def get_suit(self):
        return self.suit


def who_wins(hand1, hand2, community):
    if detect_royal_flush(hand1, community) == True and detect_royal_flush(hand2, community) == False:
        return 1
    elif detect_royal_flush(hand2, community) == True and detect_royal_flush(hand1, community) == False:
        return 2

    elif detect_straight_flush(hand1, community) == True and detect_straight_flush(hand2, community) == False:
        return 1
    elif detect_straight_flush(hand2, community) == True and detect_straight_flush(hand1, community) == False:
        return 2

    elif n_of_a_kind(hand1, community) == 5 and n_of_a_kind(hand2, community) < 5:
        return 1
    elif n_of_a_kind(hand2, community) == 5 and n_of_a_kind(hand1, community) < 5:
        return 2
    elif n_of_a_kind(hand1, community) == 5 and n_of_a_kind(hand2, community) == 5:
        if detect_high_card(hand1, hand2) == 1:
            return 1
        if detect_high_card(hand1, hand2) == 2:
            return 2
    # if detect_high_card(hand1, hand2) == 0:
    #    return 0

    elif n_of_a_kind(hand1, community) == 4 and n_of_a_kind(hand2, community) < 4:
        return 1
    elif n_of_a_kind(hand2, community) == 4 and n_of_a_kind(hand1, community) < 4:
        return 2
    elif n_of_a_kind(hand1, community) == 4 and n_of_a_kind(hand2, community) == 4:
        return 0  # this is the case that both are full house. must check high card. didn't do it yet

    elif detect_flush(hand1, community) == True and detect_flush(hand2, community) == False:
        return 1
    elif detect_flush(hand2, community) == True and detect_flush(hand1, community) == False:
        return 2
    # elif detect_flush(hand1, community) == True and detect_flush(hand2, community) == True:
    #    return 0 # must find high card in that suit <-- not just in your hand. haven't done this yet.

    elif detect_straight(hand1, community) > detect_straight(hand2, community):
        return 1
    elif detect_straight(hand2, community) > detect_straight(hand1, community):
        return 2
    # elif detect_straight(hand1, community) == detect_straight(hand2, community):
    #   return 0

    elif n_of_a_kind(hand1, community) == 3 and n_of_a_kind(hand2, community) < 3:
        return 1
    elif n_of_a_kind(hand2, community) == 3 and n_of_a_kind(hand1, community) < 3:
        return 2
    elif n_of_a_kind(hand1, community) == 3 and n_of_a_kind(hand2, community) == 3:
        return 0

    elif n_of_a_kind(hand1, community) == 2 and n_of_a_kind(hand2, community) < 2:
        return 1
    elif n_of_a_kind(hand2, community) == 2 and n_of_a_kind(hand1, community) < 2:
        return 2
    elif n_of_a_kind(hand1, community) == 2 and n_of_a_kind(hand2, community) == 2:
        return 0
    elif n_of_a_kind(hand1, community) == 1 and n_of_a_kind(hand2, community) < 1:
        return 1
    elif n_of_a_kind(hand2, community) == 1 and n_of_a_kind(hand1, community) < 1:
        return 2
    elif n_of_a_kind(hand1, community) == 1 and n_of_a_kind(hand2, community) == 1:
        n = detect_high_card(hand1, hand2)
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return 0
    elif n_of_a_kind(hand1, community) == 0 and n_of_a_kind(hand2, community) == 0:
        n = detect_high_card(hand1, hand2)
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return 0


def create_deck():
    deck = []
    val = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suit = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    # initializes the deck
    for i in range(4):
        for j in range(13):
            deck.append(Card(val[j], suit[i]))
    random.shuffle(deck)
    return deck


def shuffle(deck):
    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)


def print_deck(deck):
    faces = ['Jack', 'Queen', 'King', 'Ace']
    for card in deck:
        val = card.get_val()
        if val > 10:
            face_val = faces[val - 11]
            print(face_val, "of", card.get_suit())
        else:
            print(card.get_val(), "of", card.get_suit())


def create_hand(deck):
    card1 = random.choice(deck)
    deck.remove(card1)
    card2 = random.choice(deck)
    deck.remove(card2)
    return [card1, card2]


# flop 3 cards
def flop(deck, community_cards):
    flop1 = random.choice(deck)
    community_cards.append(flop1)
    deck.remove(flop1)

    flop2 = random.choice(deck)
    community_cards.append(flop2)
    deck.remove(flop2)

    flop3 = random.choice(deck)
    community_cards.append(flop3)
    deck.remove(flop3)


# turn 1 card
def turn(deck, community_cards):
    turn1 = random.choice(deck)
    community_cards.append(turn1)
    deck.remove(turn1)


# river 1 card
def river(deck, community_cards):
    river1 = random.choice(deck)
    community_cards.append(river1)
    deck.remove(river1)


# evaluating hands ----------------------------
def n_of_a_kind(hand, community):
    card_freqs_sum = 0
    if hand[0].get_val() == hand[1].get_val():
        card_freqs_sum = 2
        for card in community:
            if card.get_val() == hand[0].get_val():
                card_freqs_sum += 1
        if card_freqs_sum == 4:
            return 4  # full house
        elif card_freqs_sum == 3:
            return 3  # 3 of a kind
        elif card_freqs_sum == 2:
            return 2  # 2 pair

    card1_count = 1
    for card in community:
        if card.get_val() == hand[0].get_val():
            card1_count += 1
        if hand[1].get_val() == hand[0].get_val():
            card1_count += 1

    card2_count = 1
    for card in community:
        if card.get_val() == hand[1].get_val():
            card2_count += 1
        if hand[0].get_val() == hand[1].get_val():
            card2_count += 1
    card_freqs_sum = card1_count + card2_count
    if card_freqs_sum == 5 and (card1_count == 4 or card2_count == 4):
        return 5  # 4 of a kind
    elif card_freqs_sum == 5 and (card1_count == 3 or card2_count == 3):
        return 4  # full house
    elif card_freqs_sum == 4 and card1_count != 2:
        return 3  # 3-of-a-kind
    elif card_freqs_sum == 4 and card1_count == 2:
        return 2  # 2 pair
    elif card_freqs_sum == 3:
        return 1  # pair
    else:
        return 0  # no pair


def detect_flush(hand, community):
    suit = community[0].get_suit()
    b = False
    for card in community:
        if card.get_suit() == suit:
            b == True
        else:
            b = False
            break
    if b == True:
        return True  # Flush

    count_suits = 0
    count_suit_card_one = 1
    count_suit_card_two = 1
    if hand[0].get_suit() == hand[1].get_suit():
        count_suits = 2
        for card in community:
            if card.get_suit() == hand[0].get_suit():
                count_suits += 1
    else:
        for card in community:
            if card.get_suit() == hand[0].get_suit():
                count_suit_card_one += 1

        for card in community:
            if card.get_suit() == hand[1].get_suit():
                count_suit_card_two += 1

    if count_suits >= 5 or count_suit_card_one >= 5 or count_suit_card_two >= 5:
        return True  # True
    else:
        return False  # False


def detect_straight(hand, community):
    all_cards = []
    a_high = 0
    b_high = 0
    c_high = 0
    a = 0
    b = 0
    c = 0
    arr = [0]
    for card in hand:
        all_cards.append(card)
    for card in community:
        all_cards.append(card)
    all_cards.sort(key=lambda x: x.value)

    if all_cards[-1].get_val() == 14 and all_cards[4].get_val() == 5:
        return 5

    for i in range(4):
        if all_cards[i + 1].get_val() - all_cards[i].get_val() == 1:
            a += 1
        else:
            a = 0
            break
    if a == 4:
        a_high = all_cards[4].get_val()
        arr.append(a_high)

    for i in range(1, 5):
        if all_cards[i + 1].get_val() - all_cards[i].get_val() == 1:
            b += 1
        else:
            b = 0
            break
    if b == 4:
        b_high = all_cards[5].get_val()
        arr.append(b_high)

    for i in range(2, 6):
        if all_cards[i + 1].get_val() - all_cards[i].get_val() == 1:
            c += 1
        else:
            c = 0
            break
    if c == 4:
        c_high = all_cards[6].get_val()
        arr.append(c_high)

    # print(arr)
    high_card = max(arr)

    return high_card

    '''if a == 0 and b == 0 and c == 0:
        return False # No Straight
    else:
        return True # Straight'''


def detect_straight_flush(hand, community):
    if (detect_straight(hand, community) > 0) and (detect_flush(hand, community) == True):
        return True
    else:
        return False


def detect_royal_flush(hand, community):
    if (detect_straight(hand, community) == 14) and (detect_flush(hand, community) == True):
        return True
    else:
        return False


def detect_high_card(hand1, hand2):
    h1_high_card = 0
    h2_high_card = 0

    c1_h1 = hand1[0].get_val()
    c2_h1 = hand1[1].get_val()

    c1_h2 = hand2[0].get_val()
    c2_h2 = hand2[1].get_val()

    if c1_h1 >= c2_h1:
        h1_high_card = c1_h1
    else:
        h1_high_card = c2_h1

    if c1_h2 >= c2_h2:
        h2_high_card = c1_h2
    else:
        h2_high_card = c2_h2

    if h1_high_card > h2_high_card:
        return 1  # 1 wins
    elif h1_high_card < h2_high_card:
        return 2  # 2 wins
    else:
        return 0  # no high card


# evaluating hands ----------------------------


def main():
    deck = create_deck()
    shuffle(deck)
    hand1 = create_hand(deck)
    hand2 = create_hand(deck)
    print()
    print()
    print("----------------------------")
    print("  Welcome to Texas Hold'em")
    print("----------------------------")
    print()
    print()
    hand1 = create_hand(deck)
    print(" ** Hand 1 ** ")
    print("  ----------")
    print_deck(hand1)
    print()
    print()
    print(" ** Hand 2 ** ")
    print("  ----------")
    print_deck(hand2)

    community = []
    flop(deck, community)
    turn(deck, community)
    river(deck, community)

    print()
    print("** Community Cards ** ")
    print(" -------------------")
    print_deck(community)
    print("--------------------------")
    print()
    if who_wins(hand1, hand2, community) == 1:
        print("     *******************")
        print("******** Player 1 Wins! ********")
        print("     *******************")
    elif who_wins(hand1, hand2, community) == 2:
        print("     *******************")
        print("******** Player 2 Wins! ********")
        print("     *******************")
    else:
        print("     *******************")
        print("******** Draw ********")
        print("     *******************")

    print()
    print(" ** Hand 1 ** ")
    print("----------")
    n1 = n_of_a_kind(hand1, community)
    if n1 == 5:
        print("4-of-a-kind")
    elif n1 == 4:
        print("Full House")
    elif n1 == 3:
        print("3-of-a-kind")
    elif n1 == 2:
        print("Two Pair")
    elif n1 == 1:
        print("Pair")
    elif n1 == 0:
        print("No Pair")

    s1 = detect_straight(hand1, community)
    if s1 > 0:
        face = s1
        faces = ['Jack', 'Queen', 'King', 'Ace']
        if s1 > 10:
            face = faces[s1 - 11]

        print("Straight with high", face)
    else:
        print("No Straight")

    f1 = detect_flush(hand1, community)
    if f1 == True:
        print("Flush")
    else:
        print("No Flush")

    print()

    print(" ** Hand 2 ** ")
    print("----------")
    n2 = n_of_a_kind(hand2, community)

    if n2 == 5:
        print("4-of-a-kind")
    elif n2 == 4:
        print("Full House")
    elif n2 == 3:
        print("3-of-a-kind")
    elif n2 == 2:
        print("Two Pair")
    elif n2 == 1:
        print("Pair")
    elif n2 == 0:
        print("No Pair")

    s2 = detect_straight(hand2, community)
    if s2 > 0:
        face = s2
        faces = ['Jack', 'Queen', 'King', 'Ace']
        if s2 > 10:
            face = faces[s2 - 11]

        print("Straight with high", face)
    else:
        print("No Straight")
    if s2 == True:
        print("Flush")
    else:
        print("No Flush")


main()
