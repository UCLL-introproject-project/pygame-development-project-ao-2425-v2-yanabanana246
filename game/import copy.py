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
start_money = 100  # or whatever starting amount you want
money = start_money  # This ensures money starts as an integer
money_bet = 20
money_updated = False
# split
may_split = False
amount_splits = 0
want_split = False
current_hand_index = 0  # Track which hand is active during split

# double down
double_down = False
#stand for double down collor change
stand=False

# aantaal games 
aantal_games = 0

# deal cards by selecting randomly from deck, and make function for one card at a time

def deal_cards(current_hand, current_deck, want_split=False, hand_index=0):
    if want_split and isinstance(current_hand[0], list) and len(current_hand) == 2:
        card = random.randint(0, len(current_deck) - 1)
        current_hand[hand_index].append(current_deck[card])
        current_deck.pop(card)
    else:
        card = random.randint(0, len(current_deck) - 1)
        current_hand.append(current_deck[card])
        current_deck.pop(card)
    return current_hand, current_deck

# show the amount of money you have and the amount you bet.
def draw_money(money, result):
    
    screen.blit(font.render(f' Money [{money}]', True, 'white'), (0, 0))
    if money == 'All your money is gone':
        print('quiet')
    
# draw scores for players and dealer on screen 
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))

# draw cards visually ont screen 
def draw_cards(player, dealer, reveal):
    if not isinstance(player[0], list):
        for i in range(len(player)):
            pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
            screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
            screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
            pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
    # cards has been split
    else:
        for hands in player:
            for i in range(len(hands)):
                pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
                screen.blit(font.render(hands[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
                screen.blit(font.render(hands[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
                pygame.draw.rect(screen, 'purple', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
     # if player hasn't finished turn, dealer will hide one card
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

def split_cards(want_split, my_hand):
    if want_split:
        first_hand = my_hand[:1]
        second_hand = my_hand[1:]
        my_hand = [first_hand, second_hand]
    return my_hand
# will draw to seperate hands

def draw_split_hands(split_hands, dealer_hand, reveal_dealer, current_hand_index):
    for i in range(len(split_hands[0])):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460, 120, 220], 0, 5)
        screen.blit(font.render(split_hands[0][i], True, 'black'), (75 + 70 * i, 465))
        screen.blit(font.render(split_hands[0][i], True, 'black'), (75 + 70 * i, 635))
        # Highlight current active hand
        color = 'yellow' if current_hand_index == 0 else 'green'
        pygame.draw.rect(screen, color, [70 + (70 * i), 460, 120, 220], 5, 5)
        # Draw second hand (bottom)

    for i in range(len(split_hands[1])):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 660, 120, 220], 0, 5)
        screen.blit(font.render(split_hands[1][i], True, 'black'), (75 + 70 * i, 665))
        screen.blit(font.render(split_hands[1][i], True, 'black'), (75 + 70 * i, 835))
        # Highlight current active hand

        color = 'yellow' if current_hand_index == 1 else 'green'
        pygame.draw.rect(screen, color, [70 + (70 * i), 660, 120, 220], 5, 5)
    # Draw dealer's hand

    for i in range(len(dealer_hand)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal_dealer:
            screen.blit(font.render(dealer_hand[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer_hand[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else: 
            screen.blit(font.render('???', True, 'black'), (75+ 70 * i, 165 + 5 * i))
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
    #calculate hand score fresh every time, check how many aces we have

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
    button_list = []
    # intitlaly on startuup ( not active )  only option is to deal new hand

    if not act: 
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (200, 50))
        button_list.append(deal)
        screen.blit(font.render(f' Money {money}', True, 'white'), (0, 0))
    # one game started, shot hit and stand , split ( if needed), Double down buttons and  win/loss records

    else:
        # 00
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        # 01
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        #02
        double_down = pygame.draw.rect(screen, 'white', [300, 0, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'gold', [300, 0, 300, 100], 3, 5)
        double_down_text = font.render('Double Down', True, 'black')
        screen.blit(double_down_text, (355, 35))
        button_list.append(double_down)

        score_text = font.render(f'Wins: {records[0]} Losses: {records[1]} Tie: {records[2]}', True, 'white')
        screen.blit(score_text, (15, 840))
        screen.blit(font.render(f' Money {money}', True, 'white'), (0, 0))
        aantal_games += 1

        
        # draws splitbutton if apllicable 
        #03
        if possiblility_split(my_hand):
            split = pygame.draw.rect(screen, 'white', [300, 500, 300, 100], 0, 5)
            pygame.draw.rect(screen, 'green', [300, 500, 300, 100], 3, 5)
            split_text = font.render('Split ?', True, 'black')
            screen.blit(split_text, (400, 535))
            button_list.append(split)
    #if ther is an outcome for the hand tat was played, display a restart button an tell user what happend

    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = font.render('New HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
  #  print(button_list)
    return button_list
# check endgam conditions function 
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # First check if my_hand exists and has elements
    if my_hand and len(my_hand) > 0:
        # For split hands
        if isinstance(my_hand[0], list) and len(my_hand) == 2:
            hand1_score = calculate_score(my_hand[0])
            hand2_score = calculate_score(my_hand[1])
            
            if not hand_act and deal_score >= 17:
                # Check if either hand is a winner
                hand1_wins = (hand1_score <= 21 and (hand1_score > deal_score or deal_score > 21))
                hand2_wins = (hand2_score <= 21 and (hand2_score > deal_score or deal_score > 21))
                
                if hand1_wins or hand2_wins:
                    result = 2  # Player wins
                # Check for tie - both hands must tie or one ties while other busts
                elif ((hand1_score == deal_score and hand1_score <= 21) and 
                      (hand2_score == deal_score and hand2_score <= 21)):
                    result = 4  # Tie game
                else:
                    result = 3  # Dealer wins
                    
                if add:
                    if result == 2:
                        totals[0] += 1
                    elif result == 3:
                        totals[1] += 1
                    else:
                        totals[2] += 1
                    add = False
        else:
            # Original logic for non-split hands
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
def calculate_money(start_money, result, current_money, money_bet, want_split,double_down):
    # Convert current_money to int if it's a string
    if isinstance(current_money, str):
        try:
            current_money = int(current_money)
        except ValueError:
            return 0  # Return 0 if conversion fails
    if want_split and double_down: 
        money_bet *= 2
        money_bet *= 2
    elif want_split or double_down:
        money_bet *= 2
        

        
    if result in [1, 3]:  # Player busted or Dealer wins
        return current_money - money_bet
    elif result == 2:  # Player wins
        return current_money + money_bet
    elif result == 4:  # Tie game
        return current_money  # No money change
    return current_money  # Default case
def change_color_double_down(double_down, stand):
    if double_down and not stand:
        pygame.draw.rect(screen, 'purple', [300, 0, 300, 100], 3, 5)
    

def quit_game(money):
    if isinstance(money, str):
        try:
            money = int(money)
        except ValueError:
            money = 0
            
    if money <= 0:
        # Initialize pygame clock
        clock = pygame.time.Clock()
        countdown_duration = 20  # seconds
        start_time = pygame.time.get_ticks()

        while True:
            clock.tick(60)  # Limit to 60 FPS for smooth display
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) // 1000
            time_remaining = countdown_duration - elapsed_time

            if time_remaining <= 0:
                break

            # Clear screen
            screen.fill('black')
            
            # Draw Game Over text
            game_over_text = font.render('Game Over - Out of Money!', True, 'red')
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
            
            # Draw Statistics
            stats_text = font.render('Final Statistics:', True, 'white')
            screen.blit(stats_text, (WIDTH//2 - stats_text.get_width()//2, HEIGHT//2 - 20))
            
            wins_text = font.render(f'Wins: {records[0]}', True, 'green')
            losses_text = font.render(f'Losses: {records[1]}', True, 'red')
            ties_text = font.render(f'Ties: {records[2]}', True, 'yellow')
            
            screen.blit(wins_text, (WIDTH//2 - wins_text.get_width()//2, HEIGHT//2 + 20))
            screen.blit(losses_text, (WIDTH//2 - losses_text.get_width()//2, HEIGHT//2 + 60))
            screen.blit(ties_text, (WIDTH//2 - ties_text.get_width()//2, HEIGHT//2 + 100))
            
            # Calculate and display win percentage
            total_games = sum(records)
            if total_games > 0:
                win_percentage = (records[0] / total_games) * 100
                percentage_text = font.render(f'Win Rate: {win_percentage:.1f}%', True, 'white')
                screen.blit(percentage_text, (WIDTH//2 - percentage_text.get_width()//2, HEIGHT//2 + 140))

            # Draw countdown timer
            minutes = time_remaining // 60
            seconds = time_remaining % 60
            timer_text = font.render(f'Game closing in: {minutes:02d}:{seconds:02d}', True, 'white')
            screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, HEIGHT - 100))

            # Update display
            pygame.display.flip()

            # Handle only the quit event (X button)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            # Small delay to prevent CPU overuse
            pygame.time.delay(16)  # approximately 60 FPS

        return False
    return True

# main game  loop 
run = True
while run:
    # run game at our framrate and fill sceen with bg color
    timer.tick(fps)
    screen.fill('black')
    # initial deal to player and dealer

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        may_split = possiblility_split(my_hand)
        initial_deal = False


    # once game is activated, and dealt, calculate scores and display cards
    if active:
        if want_split and isinstance(my_hand[0], list) and len(my_hand) == 2:
            draw_split_hands(my_hand, dealer_hand, reveal_dealer, current_hand_index)
            if reveal_dealer:
                dealer_score = calculate_score(dealer_hand)
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            draw_split_scores(my_hand, dealer_score, current_hand_index, reveal_dealer)
        else:
            player_score = calculate_score(my_hand)
            draw_cards(my_hand, dealer_hand, reveal_dealer)
            if reveal_dealer:
                dealer_score = calculate_score(dealer_hand)
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome, aantal_games, money)
    change_color_double_down(double_down, stand)

    # enent handling, if quit pressed, then exit game
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
                    current_hand_index = 0
            else:

                # if player can hit, allo them to draw a card 
                if buttons[0].collidepoint(event.pos) and hand_active:
                    # if the cards are split let the hit until they reach higher then 21
                    if want_split and isinstance(my_hand[0], list) and len(my_hand) == 2:
                        my_hand, game_deck = deal_cards(my_hand, game_deck, want_split, current_hand_index)
                        if calculate_score(my_hand[current_hand_index]) > 21:
                            if current_hand_index == 0:
                                current_hand_index = 1
                                if calculate_score(my_hand[1]) > 21 :
                                    hand_active = False
                                    reveal_dealer = True

                            else:
                                hand_active = False
                                reveal_dealer = True
                                stand=True
                    else:
                        # this is not split 
                        my_hand, game_deck = deal_cards(my_hand, game_deck)
                        if calculate_score(my_hand) > 21:
                            hand_active = False
                            reveal_dealer = True
                # let player end turn( stand)
                elif buttons[1].collidepoint(event.pos) and hand_active:
                    # if cards are split just let the end 1  part at a time
                    if want_split and isinstance(my_hand[0], list) and len(my_hand) == 2:
                        if current_hand_index == 0:
                            current_hand_index = 1
                            if calculate_score(my_hand[1]) > 21 :
                                hand_active = False
                                reveal_dealer = True
                        else:
                            hand_active = False
                            reveal_dealer = True
                            stand=True
                    # allow player to end turn without split
                    else:
                        hand_active = False
                        reveal_dealer = True
                        stand=True

                elif len(buttons) == 4:
                    #start game
                    if buttons[3].collidepoint(event.pos) and '<rect(150, 220, 300, 100)>' in str(buttons):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0
                        money_updated = False
                        current_hand_index = 0
                        double_down=False
                        want_split=False
                        stand=False


                        

                        # makes the split option 
                    elif buttons[3].collidepoint(event.pos) and '<rect(300, 500, 300, 100)>' in str(buttons):
                        want_split = True
                        my_hand = split_cards(want_split, my_hand)
                        split_cards(want_split, my_hand)
                    # try double down 
                    elif buttons[3].collidepoint(event.pos) and '<rect(300, 0, 300, 100)>' in str(buttons):
                        print('works')
                        double_down = True
                        change_color_double_down(double_down,stand)


                elif len(buttons) == 3:
                    #start game
                    if buttons[2].collidepoint(event.pos) and '<rect(150, 220, 300, 100)>' in str(buttons):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0
                        money_updated = False
                        current_hand_index = 0
                        stand=False
                        

                        # makes the split option 
                    elif buttons[2].collidepoint(event.pos) and '<rect(300, 500, 300, 100)>' in str(buttons):
                        want_split = True
                        my_hand = split_cards(want_split, my_hand)
                        split_cards(want_split, my_hand)
                    # try double down 
                    elif buttons[2].collidepoint(event.pos) and '<rect(300, 0, 300, 100)>' in str(buttons):
                        print('works')
                        double_down = True
                        change_color_double_down(double_down,stand)



    # if player busts, autmaticlly end turn - treat like a stand
    if hand_active and not want_split and calculate_score(my_hand) > 21:
        hand_active = False
        reveal_dealer = True
    
    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    if outcome != 0 and not money_updated:
        money = calculate_money(start_money, outcome, money,money_bet,want_split,double_down)
        money_updated = True
        run = quit_game(money)
    pygame.display.flip()
pygame.quit()