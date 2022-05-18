import random


# ---------- game setup ----------


class Card:
    # Card class defines a card
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def get_val(self):
        return self.value

    def get_suit(self):
        return self.suit


def create_deck():
    # creates the deck
    deck = []
    val = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suit = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    # initializes the deck
    for i in range(4):
        for j in range(13):
            deck.append(Card(val[j], suit[i]))
    return deck


def shuffle(deck):
    # shuffles the deck
    random.shuffle(deck)


def create_hand(deck):
    # creates a hand
    card1 = random.choice(deck)
    deck.remove(card1)
    card2 = random.choice(deck)
    deck.remove(card2)
    return [card1, card2]


def flop(deck, community_cards):
    # flop 3 cards
    for i in range(3):
        flop_card = random.choice(deck)
        community_cards.append(flop_card)
        deck.remove(flop_card)


def turn(deck, community_cards):
    # turn 1 card
    turn_card = random.choice(deck)
    community_cards.append(turn_card)
    deck.remove(turn_card)


def river(deck, community_cards):
    # river 1 card
    river_card = random.choice(deck)
    community_cards.append(river_card)
    deck.remove(river_card)


# ---------- helper functions ----------


def print_deck(deck):
    # prints the deck
    faces = ['Jack', 'Queen', 'King', 'Ace']
    for card in deck:
        val = card.get_val()
        if val > 10:
            face_val = faces[val - 11]
            print(face_val, "of", card.get_suit())
        else:
            print(card.get_val(), "of", card.get_suit())


def remove_value(l1, target):
    # removes a target value in a given list
    answer = []
    for i in l1:
        if i != target:
            answer.append(i)
    return answer


def high_card(hand):
    # returns the high card of a hand
    if hand[0].get_val() >= hand[1].get_val():
        return hand[0].get_val()
    else:
        return hand[1].get_val()


def low_card(hand):
    # returns the low card of a hand
    if hand[0].get_val() >= hand[1].get_val():
        return hand[1].get_val()
    else:
        return hand[0].get_val()


def combine_cards(hand, community):
    # combines the whole cards with the community cards
    all_cards = []
    for card in hand:
        all_cards.append(card)
    for card in community:
        all_cards.append(card)
    return all_cards


def print_players_hands(players):
    # prints the hands of players given a list of players
    for index, player in enumerate(players):
        print("Player", index + 1)
        print_deck(player)
        print()


def straight_helper(cards):
    # given 5 numbers in an array, well tell if they are in straight order
    # defined as (n+1 - n) = 1
    for i in range(4):
        diff = cards[i + 1] - cards[i]
        if diff != 1:
            return False
    return True


def append_ties(points_array, max_value):
    res = []
    for i in range(len(points_array)):
        if points_array[i] == max_value:
            res.append(i)
        else:
            res.append(-1)
    return res


# ---------- hand evaluation ----------

def two_of_a_kind(hand, community):
    # creates an array of card objects
    all_cards = combine_cards(hand, community)
    # creates an array of ONlY card values
    only_values = []
    for card in all_cards:
        only_values.append(card.get_val())
    # checks to see if a two-of-a-kind exists in the array
    for value in only_values:
        if only_values.count(value) == 2:
            # three kicker values(next highest cards) are used to determine the winner of two equal two-of-a-kinds
            only_values = remove_value(only_values, value)
            first_kicker = max(only_values)
            only_values = remove_value(only_values, first_kicker)
            second_kicker = max(only_values)
            if four_of_a_kind(hand, community)[0] is False or full_house(hand, community)[0] is False:
                only_values = remove_value(only_values, second_kicker)
                third_kicker = max(only_values)
            else:
                return [False]
            # returns the truth value of two_of_a_kind, the value, and three kickers
            return [True, value, first_kicker, second_kicker, third_kicker]
    return [False]


def two_pair(hand, community):
    values = []
    # if flag == 2, there is a two pair.
    flag = 0
    # creates an array of card objects
    all_cards = combine_cards(hand, community)
    # creates an array of only card values
    only_values = []
    for card in all_cards:
        only_values.append(card.get_val())
    # checks to see if 2 pair exists in the
    for value in only_values:
        if only_values.count(value) == 2:
            flag += 1
            values.append(value)
            only_values.remove(value)
        if flag == 2:
            # returns the truth value of two_pair and the values of pair one and two
            # also returns one kicker value to determine who wins tie breaks
            only_values = remove_value(only_values, values[0])
            only_values = remove_value(only_values, values[1])
            kicker = max(only_values)
            high_pair = 0
            low_pair = 0
            if values[0] >= values[1]:
                high_pair = values[0]
                low_pair = values[1]
            elif values[0] < values[1]:
                high_pair = values[1]
                low_pair = values[0]
            return [True, high_pair, low_pair, kicker]
    return [False]


def three_of_a_kind(hand, community):
    # creates an array of card objects
    all_cards = combine_cards(hand, community)
    # creates an array of only card values
    only_values = []
    for card in all_cards:
        only_values.append(card.get_val())
    # checks to see if 3 pair exists in the
    for value in only_values:
        if only_values.count(value) == 3:
            # returns the truth value of three_of_a_kind and the value of the triplet
            # additionally, it must return 2 kicker cards which are the next 2 highest cards in the set
            only_values = remove_value(only_values, value)
            first_kicker = max(only_values)
            only_values = remove_value(only_values, first_kicker)
            second_kicker = max(only_values)
            return [True, value, first_kicker, second_kicker]
    return [False]


def detect_straight(hand, community):
    all_cards = combine_cards(hand, community)
    only_values = []
    for card in all_cards:
        only_values.append(card.get_val())
    only_values = list(set(only_values))
    only_values.sort()
    length = len(only_values)
    if length < 5:
        return [False]
    elif length == 5:
        if straight_helper(only_values) is True:
            return [True, only_values[-1]]
    elif length == 6:
        low = only_values[0:5]
        high = only_values[1:6]
        if straight_helper(high) is True:
            return [True, high[-1]]
        elif straight_helper(low) is True:
            return [True, low[-1]]
    elif length == 7:
        low = only_values[0:5]
        mid = only_values[1:6]
        high = only_values[2:7]

        if straight_helper(high) is True:
            return [True, high[-1]]
        elif straight_helper(mid) is True:
            return [True, mid[-1]]
        elif straight_helper(low) is True:
            return [True, low[-1]]
    return [False]


def detect_flush(hand, community):
    flag = False
    # the suit of the flush if there is one
    suit = ""
    # creates an array of card objects
    all_cards = combine_cards(hand, community)
    # creates an array of only card suits
    only_suits = []
    for card in all_cards:
        only_suits.append(card.get_suit())
    for i in range(len(only_suits)):
        if only_suits.count(only_suits[i]) >= 5:
            flag = True  # True if flush is detected
            suit = only_suits[i]  # detects what suit the flush is
            break
    only_suit_cards = []
    for card in all_cards:
        if card.get_suit() == suit:
            only_suit_cards.append(card)  # creates array with all cards that are of the flushes suit
    # sort this array by value
    only_suit_cards.sort(key=lambda x: x.value)
    # list of suits in highest to the lowest value.
    only_suits_cards = reversed(only_suit_cards)

    if flag:
        return [True, list(only_suits_cards)]
    else:
        return [False]


def full_house(hand, community):
    three = three_of_a_kind(hand, community)
    two = two_of_a_kind(hand, community)
    # if either of these return False, there is no Full House
    if three[0] is True and two[0] is True:
        # returns the truth value of full house, the triplet value, and the double value within the full house.
        return [True, three[1], two[1]]
    else:
        return [False]


def four_of_a_kind(hand, community):
    # creates an array of card objects
    all_cards = combine_cards(hand, community)
    # creates an array of only card values
    only_values = []
    for card in all_cards:
        only_values.append(card.get_val())
    # checks to see if 3 pair exists in the
    for value in only_values:
        if only_values.count(value) == 4:
            # returns the truth value of four_of_a_kind and the value of the quadruplet
            # also returns the one kicker value which is the next highest value in the set of cards
            only_values = remove_value(only_values, value)
            return [True, value, max(only_values)]
    else:
        return [False]


def detect_straight_flush(hand, community):
    straight = detect_straight(hand, community)
    flush = detect_flush(hand, community)
    # no need to do rest if base case false
    if straight[0] is True and flush[0] is True:
        flush_high_card = ((flush[1])[0]).get_val()
        if straight[1] == flush_high_card:
            return True
        else:
            return False
    else:
        return False


def detect_royal_flush(hand, community):
    straight = detect_straight(hand, community)
    # no need to do rest if base case false
    if straight[0] is True:
        straight_high_card = straight[1]
        if detect_straight_flush(hand, community) is True and straight_high_card == 14:
            return True
        else:
            return False
    else:
        return False


# ---------- Who Wins? ----------

def who_wins(player_array, community):
    length = len(player_array)
    points_array = [0] * length

    # going from a top-down approach
    # as soon as array filled with value, use "continue" to start next player

    for i in range(length):
        two = two_of_a_kind(player_array[i], community)
        two_p = two_pair(player_array[i], community)
        three = three_of_a_kind(player_array[i], community)
        straight = detect_straight(player_array[i], community)
        flush = detect_flush(player_array[i], community)
        f_house = full_house(player_array[i], community)
        four = four_of_a_kind(player_array[i], community)

        # ----------- Royal Flush -----------
        if detect_royal_flush(player_array[i], community) is True:
            points_array[i] = 9
            continue
        # ----------- Straight Flush -----------
        elif detect_straight_flush(player_array[i], community) is True:
            points_array[i] = 8
            continue
        # ----------- Four-Of-A-Kind -----------
        elif four[0] is True:
            points_array[i] = 7
            continue
        # ----------- Full House -----------
        elif f_house[0] is True:
            points_array[i] = 6
            continue
        # ----------- Flush -----------
        elif flush[0] is True:
            points_array[i] = 5
            continue
        # ----------- Straight -----------
        elif straight[0] is True:
            points_array[i] = 4
            continue
        # ----------- Three-Of-A-Kind -----------
        elif three[0] is True:
            points_array[i] = 3
            continue
        # ----------- Two Pair -----------
        elif two_p[0] is True:
            points_array[i] = 2
            continue
        # ----------- Two-Of-A-Kind -----------
        elif two[0] is True:
            points_array[i] = 1
            continue

    # print()
    # print("Points Table:", points_array)
    # print()

    # the max values of this array is the top scoring individuals
    max_value = max(points_array)
    # this count is the total number of top scoring individuals
    max_counts = points_array.count(max_value)
    # array for winners

    if max_counts == 1:
        return [points_array.index(max_value), max_value]
    else:
        # ------------------High-Card-------------------------- NOT COMPLETED
        if max_value == 0:

            # NOTE - High Card (determining the best high card out of multiple) code has not been completed. Work in
            # progress

            res = append_ties(points_array, max_value)
            # print("Res", res)
            pass
        # ------------------Two-of-a-Kind-------------------------- COMPLETED
        elif max_value == 1:
            res = append_ties(points_array, max_value)
            # print("Players 1", res)
            pair_values = []  # array of values
            for i in range(len(res)):
                if res[i] >= 0:
                    pair_values.append(two_of_a_kind(player_array[i], community)[1])
                else:
                    pair_values.append(-1)
            # print("Pair Values: ", pair_values)
            pv_max = max(pair_values)
            if pair_values.count(pv_max) == 1:
                return [pair_values.index(pv_max), max_value]
            else:
                res2 = append_ties(pair_values, pv_max)
                # print("Players 2", res2)
                first_kickers = []
                for i in range(len(res2)):
                    if res2[i] >= 0:
                        first_kickers.append(two_of_a_kind(player_array[i], community)[2])
                    else:
                        first_kickers.append(-1)
                # print("First Kickers: ", first_kickers)
                fk_max = max(first_kickers)
                if first_kickers.count(fk_max) == 1:
                    return [first_kickers.index(fk_max), max_value]
                else:
                    res2 = append_ties(first_kickers, fk_max)
                    # print("Players 3", res2)
                    seconds_kickers = []
                    for i in range(len(res2)):
                        if res2[i] >= 0:
                            seconds_kickers.append(two_of_a_kind(player_array[i], community)[3])
                        else:
                            seconds_kickers.append(-1)
                    # print("Second Kickers: ", seconds_kickers)
                    sk_max = max(seconds_kickers)
                    if seconds_kickers.count(sk_max) == 1:
                        return [seconds_kickers.index(sk_max), max_value]
                    else:
                        res3 = append_ties(seconds_kickers, sk_max)
                        # print("Players 4", res3)
                        third_kickers = []
                        for i in range(len(res3)):
                            if res3[i] >= 0:
                                third_kickers.append(two_of_a_kind(player_array[i], community)[4])
                            else:
                                third_kickers.append(-1)
                        # print("Third Kickers: ", third_kickers)
                        tk_max = max(third_kickers)
                        if third_kickers.count(tk_max) == 1:
                            return [third_kickers.index(tk_max), max_value]
                        else:
                            res5 = []
                            for i in range(len(res3)):
                                if third_kickers[i] > 0:
                                    res5.append(i)
                            # print("Players 5", res5)
                            res5.append(max_value)
                            return res5
        # ------------------Two-Pair-------------------------- COMPLETED
        elif max_value == 2:
            res = append_ties(points_array, max_value)
            # print("Players 1", res)
            pair_one_values = []
            for i in range(len(res)):
                if res[i] >= 0:
                    pair_one_values.append(two_pair(player_array[i], community)[1])
                else:
                    pair_one_values.append(-1)
            # print("Pair One Values: ", pair_one_values)
            pov_max = max(pair_one_values)
            if pair_one_values.count(pov_max) == 1:
                return [pair_one_values.index(pov_max), max_value]
            else:
                res2 = append_ties(pair_one_values, pov_max)
                # print("Players 2", res2)
                pair_two_values = []
                for i in range(len(res2)):
                    if res2[i] >= 0:
                        pair_two_values.append(two_pair(player_array[i], community)[2])
                    else:
                        pair_two_values.append(-1)
                # print("Pair Two Values: ", pair_two_values)
                ptv_max = max(pair_two_values)
                if pair_two_values.count(ptv_max) == 1:
                    return [pair_two_values.index(ptv_max), max_value]
                else:
                    res2 = append_ties(pair_two_values, ptv_max)
                    # print("Players 3", res2)
                    first_kickers = []
                    for i in range(len(res2)):
                        if res2[i] >= 0:
                            first_kickers.append(two_pair(player_array[i], community)[3])
                        else:
                            first_kickers.append(-1)
                    # print("Kicker Cards: ", first_kickers)
                    k_max = max(first_kickers)
                    if first_kickers.count(k_max) == 1:
                        return [first_kickers.index(k_max), max_value]
                    else:
                        res3 = []
                        for i in range(len(res2)):
                            if first_kickers[i] > 0:
                                res3.append(i)
                        # print("Players 4", res3)
                        res3.append(max_value)
                        return res3
        # ------------------Three-of-a-Kind-------------------------- COMPLETED
        elif max_value == 3:
            res = append_ties(points_array, max_value)
            # print("Players 1", res)
            triplet_values = []
            for i in range(len(res)):
                if res[i] >= 0:
                    triplet_values.append(three_of_a_kind(player_array[i], community)[1])
                else:
                    triplet_values.append(-1)
            # print("Pair One Values: ", triplet_values)
            t_max = max(triplet_values)
            if triplet_values.count(t_max) == 1:
                return [triplet_values.index(t_max), max_value]
            else:
                res2 = append_ties(triplet_values, t_max)
                # print("Players 2", res2)
                first_kickers = []
                for i in range(len(res2)):
                    if res2[i] >= 0:
                        first_kickers.append(three_of_a_kind(player_array[i], community)[2])
                    else:
                        first_kickers.append(-1)
                # print("First Kickers: ", first_kickers)
                fk_max = max(first_kickers)
                if first_kickers.count(fk_max) == 1:
                    return [first_kickers.index(fk_max), max_value]
                else:
                    res2 = append_ties(first_kickers, fk_max)
                    # print("Players 3", res2)
                    second_kickers = []
                    for i in range(len(res2)):
                        if res2[i] >= 0:
                            second_kickers.append(three_of_a_kind(player_array[i], community)[3])
                        else:
                            second_kickers.append(-1)
                    # print("Seconds Kickers: ", second_kickers)
                    sk_max = max(second_kickers)
                    if second_kickers.count(sk_max) == 1:
                        return [first_kickers.index(sk_max), max_value]
                    else:
                        res3 = []
                        for i in range(len(res2)):
                            if second_kickers[i] > 0:
                                res3.append(i)
                        # print("Players 4", res3)
                        res3.append(max_value)
                        return res3
        # ------------------Straight and Straight Flush-------------------------- COMPLETED
        elif max_value == 4 or max_value == 8:
            res = append_ties(points_array, max_value)
            # print("Players 1", res)
            high_vals = []
            for i in range(len(res)):
                if res[i] >= 0:
                    high_vals.append(detect_straight(player_array[i], community)[1])
                else:
                    high_vals.append(-1)
            hv_max = max(high_vals)
            if high_vals.count(hv_max) == 1:
                return [high_vals.index(hv_max), max_value]
            else:
                res2 = []
                for i in range(len(res)):
                    if high_vals[i] > 0:
                        res2.append(i)
                # print("Players 2", res2)
                res2.append(max_value)
                return res2
        # ------------------Flush-------------------------- NOT COMPLETED
        elif max_value == 5:
            # NOTE - Flush code (determining the better flush out of multiple) has not been completed. Work in progress
            pass
        # ------------------Full House-------------------------- COMPLETED
        elif max_value == 6:
            res = append_ties(points_array, max_value)
            # print("Players 1", res)
            triplet_values = []
            for i in range(len(res)):
                if res[i] >= 0:
                    triplet_values.append(full_house(player_array[i], community)[1])
                else:
                    triplet_values.append(-1)
            tv_max = max(triplet_values)
            if triplet_values.count(tv_max) == 1:
                return [triplet_values.index(tv_max), max_value]
            else:
                res2 = append_ties(triplet_values, tv_max)
                # print("Players 2", res2)
                pair_values = []
                for i in range(len(res)):
                    if res[i] >= 0:
                        pair_values.append(full_house(player_array[i], community)[2])
                    else:
                        pair_values.append(-1)
                pv_max = max(triplet_values)
                if pair_values.count(pv_max) == 1:
                    return [pair_values.index(pv_max), max_value]
                else:
                    res3 = []
                    for i in range(len(res2)):
                        if pair_values[i] > 0:
                            res3.append(i)
                    # print("Players 3", res3)
                    res3.append(max_value)
                    return res3
        # ------------------Four-of-a-Kind--------------------------  COMPLETED
        elif max_value == 7:
            res = append_ties(points_array, max_value)
            # print("Players 1", res)
            high_vals = []
            for i in range(len(res)):
                if res[i] >= 0:
                    high_vals.append(four_of_a_kind(player_array[i], community)[1])
                else:
                    high_vals.append(-1)
            # print("Pair One Values: ", high_vals)
            hv_max = max(high_vals)
            if high_vals.count(hv_max) == 1:
                return [high_vals.index(hv_max), max_value]
            else:
                res2 = append_ties(high_vals, hv_max)
                # print("Players 2", res2)
                first_kickers = []
                for i in range(len(res2)):
                    if res2[i] >= 0:
                        first_kickers.append(four_of_a_kind(player_array[i], community)[2])
                    else:
                        first_kickers.append(-1)
                # print("Kicker Cards: ", first_kickers)
                k_max = max(first_kickers)
                if first_kickers.count(k_max) == 1:
                    return [first_kickers.index(k_max), max_value]
                else:
                    res3 = []
                    for i in range(len(res2)):
                        if first_kickers[i] > 0:
                            res3.append(i)
                    # print("Players 3", res3)
                    res3.append(max_value)
                    return res3
        # ------------------Royal Flush--------------------------  COMPLETED
        elif max_value == 9:
            res = []
            for i in range(len(points_array)):
                if points_array[i] == max_value:
                    res.append(i)
            res.append(max_value)
            return res


# ---------- main method ----------
def main():
    # create the deck
    deck = create_deck()
    # shuffle the deck
    shuffle(deck)

    # print the banner
    print("----------------------------")
    print("  Welcome to Texas Hold'em")
    print("----------------------------")

    # collect input for the number of players
    num_of_players = int(input("How many players are at the table?: "))
    # create 'num_of_players' amount of players and put them into array.
    player_array = []
    for i in range(num_of_players):
        player_array.append(create_hand(deck))
    # returns the array of players back to the main function
    community = []
    flop(deck, community)
    turn(deck, community)
    river(deck, community)

    print()
    print("Community Cards")
    print_deck(community)
    print()

    print_players_hands(player_array)
    winning_hands = who_wins(player_array, community)
    number_to_word = ["pass", "Two-of-a-Kind", "Two-Pair", "Three-of-a-Kind", "Straight", "Flush", "Full House",
                      "Four-of-a-Kind", "Straight Flush", "Royal Flush"]
    if len(winning_hands) == 2:
        print("**************************************")
        print("Player", winning_hands[0] + 1, "won the round with a", number_to_word[winning_hands[1]])
        print("**************************************")
    else:
        print("************************************************")
        print("The following players drew the hand with a", number_to_word[winning_hands[-1]])
        for i in range(len(winning_hands) - 1):
            print("  -Player", winning_hands[i] + 1)
        print("************************************************")


main()
