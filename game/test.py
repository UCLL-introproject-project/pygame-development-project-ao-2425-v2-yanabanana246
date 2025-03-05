import copy
import random
import pygame

# game variables
pygame.init()
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4

WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()

font = pygame.font.SysFont('freesantbold.ttf', 44)
active = False
money_changed = False

# win , loss, draw/tie
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
test_money = 0
add_score = False
results = ['', 'Player busted o_0', 'Player wins! :)', 'Dealer wins:(', 'Tie game...']

# money
start_money = 100
money = start_money
money_bet = 20
money_updated = False
# split
may_split = False
split_hands = []
split_scores = []
split_active = False
split_reveal = []
split_finished = []
split_bets = []

# aantaal games
aantal_games = 0

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck) - 1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    return current_hand, current_deck

# show the amount of money you have and the amount you bet.
def draw_money(money, result):
    screen.blit(font.render(f' Money [{money}]', True, 'white'), (0, 0))

# draw scores for players and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))

# draw cards visually ont screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

# will act as all the split cards
def split_cards():
    pass

# will draw to seperate hands
def draw_split(split_hands, split_reveal, split_scores):
    for hand_idx, hand in enumerate(split_hands):
        for card_idx, card in enumerate(hand):
            x_offset = 70 + (140 * hand_idx) + (70 * card_idx)
            y_offset = 460
            pygame.draw.rect(screen, 'white', [x_offset, y_offset, 120, 220], 0, 5)
            screen.blit(font.render(card, True, 'black'), (x_offset + 5, y_offset + 5))
            screen.blit(font.render(card, True, 'black'), (x_offset + 5, y_offset + 175))
            pygame.draw.rect(screen, 'red', [x_offset, y_offset, 120, 220], 5, 5)
        screen.blit(font.render(f'Score: {split_scores[hand_idx]}', True, 'white'), (100 + (140 * hand_idx), 700))

# will seaurch if there is a possibility to split.
def possibility_split(my_hand):
    if len(my_hand) == 2 and my_hand[0] == my_hand[1]:
        return True
    else:
        return False

# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        elif hand[i] == 'A':
            hand_score += 11
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

# draw game conditions and buttons
def draw_game(act, records, result, aantal_games, money, may_split):
    button_list = []
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (200, 50))
        button_list.append(deal)
        screen.blit(font.render(f' Money {money}', True, 'white'), (0, 0))
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True,'blach')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        score_text = font.render(f'Wins: {records[0]} Losses: {records[1]} Tie: {records[2]}', True, 'white')
        screen.blit(score_text, (15, 840))
        screen.blit(font.render(f' Money {money}', True, 'white'), (0, 0))
        aantal_games += 1
        if may_split and len(my_hand) == 2:
            split = pygame.draw.rect(screen, 'white', [300, 500, 300, 100], 0, 5)
            pygame.draw.rect(screen, 'green', [300, 500, 300, 100], 3, 5)
            split_text = font.render('SPLIT', True, 'black')
            screen.blit(split_text, (400, 535))
            button_list.append(split)

    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = font.render('New HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list

# check endgam conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4

        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1

            add = False
    return result, totals, add

def calculate_money(start_money, result, current_money):
    if result == 1:
        return current_money - money_bet
    elif result == 2:
        return current_money + money_bet
    elif result == 3:
        return current_money - money_bet
    elif result == 4:
        return current_money
    return current_money

# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('black')

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        may_split = possibility_split(my_hand)
        initial_deal = False

    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)

        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            while dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
                dealer_score = calculate_score(dealer_hand)
        draw_scores(player_score, dealer_score)
        buttons = draw_game(active, records, outcome, aantal_games, money, may_split)

        if split_active:
            draw_split(split_hands, split_reveal, split_scores)
            for hand_idx, hand in enumerate(split_hands):
                if not split_finished[hand_idx]:
                    split_scores[hand_idx] = calculate_score(hand)
                    screen.blit(font.render(f'Score: {split_scores[hand_idx]}', True, 'white'),(100 + (140 * hand_idx), 700))
                    if split_scores[hand_idx] > 21:
                        split_finished[hand_idx]=True
            if all(split_finished):
                reveal_dealer=True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    add_score = True
                    money_updated = False
                    reveal_dealer=False
                    dealer_score=0
                    player_score=0
                    split_active=False
                    split_hands = []
                    split_scores = []
                    split_reveal = []
                    split_finished = []
                    split_bets = []

            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active and not split_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer and not split_active:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3 and buttons[2].collidepoint(event.pos) and not split_active and may_split:
                    split_active=True
                    split_hands.append([my_hand[0], deal_cards([], game_deck)[0][0]])
                    split_hands.append([my_hand[1], deal_cards([], game_deck)[0][0]])
                    split_scores.append(0)
                    split_scores.append(0)
                    split_reveal.append(False)
                    split_reveal.append(False)
                    split_finished.append(False)
                    split_finished.append(False)
                    split_bets.append(money_bet)
                    split_bets.append(money_bet)
                    my_hand = []
                    hand_active=False
                    may_split=False

                elif result != 0 and buttons[-1].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    add_score = True
                    money_updated = False
                    reveal_dealer=False
                    dealer_score=0
                    player_score=0
                    split_active=False
                    split_hands = []
                    split_scores = []
                    split_reveal = []
                    split_finished = []
                    split_bets = []

    if hand_active and player_score > 21 and not split_active:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    if outcome != 0 and not money_updated:
        money = calculate_money(start_money, outcome, money)
        money_updated = True

    pygame.display.flip()
pygame.quit()