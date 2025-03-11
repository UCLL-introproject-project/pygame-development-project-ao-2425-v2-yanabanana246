import pygame
import random

# initialize pygame
pygame.init()
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption('Blackjack')
# game values
screen = pygame.display.set_mode([600, 900])
font = pygame.font.Font('freesansbold.ttf', 36)
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['C', 'D', 'H', 'S']
deck =
for i in range(4):
    for j in range(13):
        deck.append(cards[j] + '-' + suits[i])
pygame.init()
first_deal = True
my_hand =
dealer_hand =
split_hands = [for _ in range(2)]
hand_active = False
dealer_active = False
splithand_active = False
my_score = 0
dealer_score = 0
records = [0, 0, 0]
results = [0, 'Player bust!', 'Player Blackjack!', 'Dealer Blackjack!', 'Push!']
result = 0
add_score = True
aantal_games = 0
buttons =
money = 500
bet = 25


# draw cards on the screen
def draw_cards(player_hand, dealer_hand, reveal_dealer):
    for i in range(len(player_hand)):
        screen.blit(font.render(player_hand[i], True, 'white'), (75 + 70 * i, 535 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 530 + (5 * i), 120, 220], 5, 5)
        if i < len(dealer_hand):
            if reveal_dealer:
                screen.blit(font.render(dealer_hand[i], True, 'white'), (75 + 70 * i, 165 + 5 * i))
                pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
            else:
                if i == 0:
                    screen.blit(font.render(dealer_hand[i], True, 'white'), (75 + 70 * i, 165 + 5 * i))
                    pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
                else:
                    screen.blit(font.render('???', True, 'white'), (75 + 70 * i, 165 + 5 * i))
                    pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


def draw_split_cards(split_hands, dealer_hand, current_hand_index, reveal_dealer):
    for i in range(len(split_hands[0])):
        if i < len(split_hands[0]):
            screen.blit(font.render(split_hands[0][i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(split_hands[0][i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


def draw_split_scores(split_hands, dealer_score, current_hand_index, reveal_dealer):
    # Draw first hand score
    score1 = calculate_score(split_hands[0])
    screen.blit(font.render(f'Hand 1: {score1}', True, 'white'), (350, 460))
    # Draw second hand score
    score2 = calculate_score(split_hands[1])
    screen.blit(font.render(f'Hand 2: {score2}', True, 'white'), (350, 660))
    # Draw dealers score
    if reveal_dealer:
        screen.blit(font.render(f'Dealer: {dealer_score}', True, 'white'), (350, 100))


# will seaurch if there is a possibility to split.
def possiblility_split(my_hand):
    if len(my_hand) == 2 and my_hand[0] == my_hand[1]:
        may_split = True
    else:
        may_split = False
    return may_split


# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 23456789 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and cars, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score


# draw game conditions and buttons
def draw_game(act, records, result, aantal_games, money):
    button_list =
    # intitlaly on startuup ( not active )  only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (200, 50))
        button_list.append(deal)
        screen.blit(font.render(f' Money {money}', True, 'white'), (0, 0))
    # one game started, shot hit and stand , split ( if needed)buttons and  win/loss records
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygamepygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        score_text = font.render(f'Wins: {records[0]} Losses: {records[1]} Tie: {records[2]}', True, 'white')
        screen.blit(score_text, (15, 840))
        screen.blit(font.render(f' Money {money}', True, 'white'), (0, 0))
        aantal_games += 1
        # draws splitbutton if apllicable
        if possiblility_split(my_hand):
            split = pygame.draw.rect(screen, 'white', [300, 500, 300, 100], 0, 5)
            pygame.draw.rect(screen, 'green', [300, 500, 300, 100], 3, 5)
            split_text = font.render('Split ?', True, 'black')
            screen.blit(split_text, (400, 535))
            button_list.append(split)
    # if ther is an outcome for the hand tat was played, display a restart button an tell user what happend
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
    # check end game scenarios is player has stood, busted or blackjacked
    # result 1- player bust, 2- win, 3-loss,4-push
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


# need to add somthing so that it says i lost all my money!
def calculate_money(start_money, result, current_money, money_bet, want_split=False):
    if want_split:
        money_bet *= 2
    if current_money <= 0:
        return 'All your money is gone'
    else:
        if result in [1, 3]:  # Player busted or Dealer wins
            return current_money - money_bet
        elif result == 2:  # Player wins
            return current_money + money_bet
        elif result == 4:  # Tie game
            return current_money  # No money change
        return current_money  # Default case

def quit_game(money):
    if money == 'All your money is gone':
        return False
    return True

# main game  loop
run = True
while run:
    # run game at our framrate and fill sceen with bg color
    timer.tick(fps)
    screen.fill('black')
    # initial deal to player and dealer
    if first_deal:
        for i in range(2):
            card = random.randint(0, len(deck) - 1)
            my_hand.append(deck[card])
            deck.pop(card)
            card = random.randint(0, len(deck) - 1)
            dealer_hand.append(deck[card])
            deck.pop(card)
        first_deal = False
        hand_active = True
        dealer_active = True
        my_score = calculate_score(my_hand)
        dealer_score = calculate_score(dealer_hand)
    # once game is activated, and dealt, calculate scores and display cards
    if hand_active:
        draw_cards(my_hand, dealer_hand, not dealer_active)
        screen.blit(font.render(f'Player Score: {my_score}', True, 'white'), (10, 400))
        if dealer_active == False:
          screen.blit(font.render(f'Dealer Score: {dealer_score}', True, 'white'), (10, 100))
    buttons = draw_game(hand_active, records, result, aantal_games, money)
    # enent handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not hand_active:
                if buttons[0].collidepoint(event.pos):
                    first_deal = True
                    my_hand = []
                    dealer_hand = []
                    deck = []
                    for i in range(4):
                        for j in range(13):
                            deck.append(cards[j] + '-' + suits[i])
                    result = 0
                    add_score = True
                    hand_active = False
                    dealer_active = False
                    money = calculate_money(500, result, money, bet)
                    if money == 'All your money is gone':
                        run = quit_game(money)
            else:
                if buttons[0].collidepoint(event.pos) and hand_active: # hit
                    card = random.randint(0, len(deck) - 1)
                    my_hand.append(deck[card])
                    deck.pop(card)
                    my_score = calculate_score(my_hand)
                    if my_score > 21:
                        hand_active = False
                        dealer_active = False
                        result = 1
                elif buttons[1].collidepoint(event.pos) and hand_active: # stand
                    hand_active = False
                    dealer_active = False
                elif len(buttons) == 3 and buttons[2].collidepoint(event.pos): # split
                    if possiblility_split(my_hand):
                        split_hands[0].append(my_hand[0])
                        split_hands[1].append(my_hand[1])
                        my_hand = []
                        splithand_active = True
                        hand_active = False
    if not hand_active and not dealer_active:
        while dealer_score < 17:
            card = random.randint(0, len(deck) - 1)
            dealer_hand.append(deck[card])
            deck.pop(card)
            dealer_score = calculate_score(dealer_hand)
        result, records, add_score = check_endgame(hand_active, dealer_score, my_score, result, records, add_score)

    pygame.display.flip()
pygame.quit()