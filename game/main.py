import copy
import random
import pygame

# This is the button coordinates 
LEFT_SPLIT_BUTTON         = 300
TOP_SPLIT_BUTTON          = 500
WIDTH_SPLIT_BUTTON        = 300
HEIGHT_SPLIT_BUTTON       = 100

LEFT_DEAL_BUTTON          = 150
TOP_DEAL_BUTTON           = 220
WIDTH_DEAL_BUTTON         = 300
HEIGHT_DEAL_BUTTON        = 100

LEFT_HIT_BUTTON           = 0
TOP_HIT_BUTTON            = 700
WIDTH_HIT_BUTTON          = 195
HEIGHT_HIT_BUTTON         = 100

LEFT_STAND_BUTTON         = 195
TOP_STAND_BUTTON          = 700
WIDTH_STAND_BUTTON        = 195
HEIGHT_STAND_BUTTON       = 100

LEFT_SURRENDER_BUTTON     = 390
TOP_SURRENDER_BUTTON      = 700
WIDTH_SURRENDER_BUTTON    = 210
HEIGHT_SURRENDER_BUTTON   = 100

LEFT_DOUBLE_DOWN_BUTTON   = 300
TOP_DOUBLE_DOWN_BUTTON    = 0
WIDTH_DOUBLE_DOWN_BUTTON  = 300
HEIGHT_DOUBLE_DOWN_BUTTON = 100



# game variables
pygame.init()
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4

game_deck_original = decks * one_deck  # Bewaar de originele deck-configuratie
game_deck = copy.deepcopy(game_deck_original)  # Maak een kopie voor gebruik in het spel


WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack Super Fun 21')
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
#money_bet = int(input('Imput a amount in numbers please'))
money_bet=20
money_updated = False
# split
may_split = False
amount_splits = 0
want_split = False
current_hand_index = 0  # Track which hand is active during split

# double down for double down collor change
double_down = False
#stand 
stand=False

# aantal games 
aantal_games = 0



# makes a bet input sceen where you can make a amount you want to bet for every game
def get_bet_input(screen, available_funds):
    # variables to track input state and user input
    input_active = True# keeps the input loop running unit a valid bet is intered
    user_input = ""
    font = pygame.font.Font(None, 50) # the font
    input_box = pygame.Rect(200, 400, 200, 50)  # Define the input box rectangle
    color_active = pygame.Color('lightskyblue3')# when active color
    color_inactive = pygame.Color('gray15')# wen inactive color
    input_color = color_inactive # start with inactive

    while input_active:
        screen.fill('black')  # Clear the screen
        
        instructions = font.render("Enter your bet:", True, 'white')
        screen.blit(instructions, (200, 300))  # Display instructions

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN: # Handle key presses

                if event.key == pygame.K_RETURN:  # Confirm input when 'Enter' is pressed
                    try:
                        bet = int(user_input) # convert anser into a integer
                        if bet <= 0:
                            print("Bet must be a positive number.")
                        elif bet > available_funds:
                            print(f"Bet exceeds available funds: {available_funds}")
                        else:
                            return bet  # Valid bet, return it
                    except ValueError:
                        # Handle non-numeric input
                        print("Invalid input. Please enter a number.")
                elif event.key == pygame.K_BACKSPACE:  # Remove last character
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode  # Add typed character to input

        # Draw input box and user input text
        input_color = color_active # change the color when active
        pygame.draw.rect(screen, input_color, input_box, 2)
        # Render the user's current input inside the input box

        text_surface = font.render(user_input, True, 'white')
        # Display the text slightly offset within the input box for readability
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        # Update the screen to reflect all changes

        pygame.display.flip()







# show the amount of money you have.
def draw_money(money, result):
    
    screen.blit(font.render(f' Money [{money}]', True, 'white'), (0, 0))
    #this is not applicable anymore because the screen will get overriten by the new screen ( the quit sreen)
    if money == 'All your money is gone':
        print('quiet')

def calculate_money(start_money, result, current_money, money_bet, want_split,double_down):
    # Convert current_money to int if it's a string
    if isinstance(current_money, str):
        try:
            current_money = int(current_money)
        except ValueError:
            return 0  # Return 0 if conversion fails
    # this makes sure you bothe get the money for split and double_down 
    if want_split and double_down: 
        money_bet *= 2
        money_bet *= 2
    # if one of them is clickt it double you mony bet
    elif want_split or double_down:
        money_bet *= 2
        
    if result in [1, 3]:  # Player busted or Dealer wins
        return current_money - money_bet
    elif result == 2:  # Player wins
        return current_money + money_bet
    elif result == 5:
        return current_money - round(money_bet/2) # lets you keep half of you bet
    elif result == 4:  # Tie game
        return current_money  # No money change
    return current_money  # Default case



# draw scores for players and dealer on screen 
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))



# this gifs the cards to the players hand and removes the card form the decks so it can't be used anymore.
def deal_cards(current_hand, current_deck, want_split=False, hand_index=0):
    #if i want to split and i can split it will make me abel to split but in this case want plit is set on false. 
    if want_split and isinstance(current_hand[0], list) and len(current_hand) == 2:
        card = random.randint(0, len(current_deck) - 1)
        current_hand[hand_index].append(current_deck[card])
        current_deck.pop(card)
    else:
        #gets a card out of the deck
        card = random.randint(0, len(current_deck) - 1)
        #gets card in to hand
        current_hand.append(current_deck[card])
        #removes card form deck.
        current_deck.pop(card)
    # updated hand and deck
    return current_hand, current_deck





# draw cards visually on the screen 
def draw_cards(player, dealer, reveal):
    # for one hand
    if not isinstance(player[0], list):
        for i in range(len(player)):
            # draws the squere
            pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
            #draws the numbers 
            screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
            screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
            #draws the red border
            pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
    # cards has been split # this gets overritten by draw_split_hands
    else:
        for hands in player:
            for i in range(len(hands)):
                #same princeple
                pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
                screen.blit(font.render(hands[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
                screen.blit(font.render(hands[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
     # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        #shows to cards of the dealer whene the player stands
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        #just show one card
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
# will act as all the split cards


# will seaurch if there is a possibility to split.

def split_cards(want_split, my_hand):
    #this and not means that if my hand already has been split it will not split again.
    if want_split and not isinstance(my_hand[0], list):
        first_hand = my_hand[:1]
        second_hand = my_hand[1:]
        my_hand = [first_hand, second_hand]
    return my_hand
# will draw to seperate hands

def draw_split_hands(split_hands, dealer_hand, reveal_dealer, current_hand_index):
    #the first hand
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


def draw_button(rectangle, background_color, border_color, text_color, text_position, text):
    #gets the coorderendtce from a specifiek button 
    left, top, width, height = rectangle
    #draws the rectantangel
    main_rectangle = pygame.draw.rect(screen, background_color, [left, top, width, height], 0, 5)

    #draws border
    pygame.draw.rect(screen, border_color, [left, top, width, height], 3, 5)
    #dras text
    deal_text = font.render(text, True, text_color)

    text_left, text_top = text_position
    screen.blit(deal_text, (text_left, text_top))

    return main_rectangle

def draw_button_with_double_border(rectangle, background_color, border_one_color, border_two_color, text_color, text_position, text):
    #same princeple as before on draw_button but just with the double border
    left, top, width, height = rectangle

    main_rectangle = draw_button(rectangle, background_color, border_one_color, text_color, text_position, text)

    pygame.draw.rect(screen, border_two_color, [left + 3, top + 3, width - 6, height - 6], 3, 5)

    return main_rectangle


#makes known witch butten is clickt
def derive_button_type_from_position(button):
    left     = button.left
    top      = button.top
    height   = button.height
    width    = button.width

    if width == WIDTH_HIT_BUTTON and height == HEIGHT_HIT_BUTTON and left == LEFT_HIT_BUTTON and top == TOP_HIT_BUTTON:
        return "HIT"
    elif width == WIDTH_STAND_BUTTON and height == HEIGHT_STAND_BUTTON and left == LEFT_STAND_BUTTON and top == TOP_STAND_BUTTON:
        return "STAND"
    elif width == WIDTH_DOUBLE_DOWN_BUTTON and height == HEIGHT_DOUBLE_DOWN_BUTTON and left == LEFT_DOUBLE_DOWN_BUTTON and top == TOP_DOUBLE_DOWN_BUTTON:
        return "DOUBLE_DOWN"
    elif width == WIDTH_SPLIT_BUTTON and height == HEIGHT_SPLIT_BUTTON and left == LEFT_SPLIT_BUTTON and top == TOP_SPLIT_BUTTON:
        return "SPLIT"
    elif width == WIDTH_DEAL_BUTTON and height == HEIGHT_DEAL_BUTTON and left == LEFT_DEAL_BUTTON and top == TOP_DEAL_BUTTON:
        return "DEAL"
    elif width == WIDTH_SURRENDER_BUTTON and height == HEIGHT_SURRENDER_BUTTON and left == LEFT_SURRENDER_BUTTON and top == TOP_SURRENDER_BUTTON:
        return "SURRENDER"
    else:
        return "UNKNOWN"


def draw_game(act, records, result, aantal_games, money):
    button_list = []
    # intitlaly on startuup ( not active )  only option is to deal new hand

    if not act: 
        deal_rectangle = (LEFT_DEAL_BUTTON, TOP_DEAL_BUTTON, WIDTH_DEAL_BUTTON, HEIGHT_DEAL_BUTTON)
        text_position  = (LEFT_DEAL_BUTTON + 55, TOP_DEAL_BUTTON + 35)
        button_list.append(draw_button(deal_rectangle, 'white', 'green', 'black', text_position, 'DEAL HAND'))
        screen.blit(font.render(f' Money {money}', True, 'white'), (0, 0))
    # one game started, shot hit and stand , split ( if needed), Double down buttons and  win/loss records

    else:
        # 00 this is the hit button
        hit_rectangle = (LEFT_HIT_BUTTON, TOP_HIT_BUTTON, WIDTH_HIT_BUTTON, HEIGHT_HIT_BUTTON)
        hit_text_position = (LEFT_HIT_BUTTON + 50, TOP_HIT_BUTTON + 35)
        button_list.append(draw_button(hit_rectangle, 'white', 'green', 'black', hit_text_position, 'HIT ME'))
        # 01 this is the stand button 
        stand_rectangle = (LEFT_STAND_BUTTON, TOP_STAND_BUTTON, WIDTH_STAND_BUTTON, HEIGHT_STAND_BUTTON)
        stand_text_position = (LEFT_STAND_BUTTON + 55, TOP_STAND_BUTTON + 35)
        button_list.append(draw_button(stand_rectangle, 'white', 'green', 'black', stand_text_position, 'STAND'))
        #02 this is the surrender button
        surrender_rectangle = (LEFT_SURRENDER_BUTTON, TOP_SURRENDER_BUTTON, WIDTH_SURRENDER_BUTTON, HEIGHT_SURRENDER_BUTTON)
        surrender_text_position = (LEFT_SURRENDER_BUTTON + 10, TOP_SURRENDER_BUTTON + 35)
        button_list.append(draw_button(surrender_rectangle, 'white', 'red', 'black', surrender_text_position, 'SURRENDER'))
        #03 this is the double down button 
        double_down_rectangle = (LEFT_DOUBLE_DOWN_BUTTON, TOP_DOUBLE_DOWN_BUTTON, WIDTH_DOUBLE_DOWN_BUTTON, HEIGHT_DOUBLE_DOWN_BUTTON)
        double_down_text_position = (LEFT_DOUBLE_DOWN_BUTTON + 35, TOP_DOUBLE_DOWN_BUTTON + 35)
        button_list.append(draw_button(double_down_rectangle, 'white', 'gold', 'black', double_down_text_position, 'DOUBLE DOWN'))
        # shows the soce text
        score_text = font.render(f'Wins: {records[0]} Losses: {records[1]} Tie: {records[2]}', True, 'white')
        screen.blit(score_text, (15, 840))
        screen.blit(font.render(f' Money {money}', True, 'white'), (0, 0))
        #count the amount of games played. 
        aantal_games += 1

        
        # draws splitbutton if apllicable 
        #03
        if possiblility_split(my_hand):
            split_rectangle = (LEFT_SPLIT_BUTTON, TOP_SPLIT_BUTTON, WIDTH_SPLIT_BUTTON, HEIGHT_SPLIT_BUTTON)
            split_text_position = (LEFT_SPLIT_BUTTON + 55, TOP_SPLIT_BUTTON + 35)
            button_list.append(draw_button(split_rectangle, 'white', 'green', 'black', split_text_position, 'SPLIT'))

    #if ther is an outcome for the hand that was played, display a restart button an tell user what happend
    if result != 0:
        new_hand_rectangle = (LEFT_DEAL_BUTTON, TOP_DEAL_BUTTON, WIDTH_DEAL_BUTTON, HEIGHT_DEAL_BUTTON)
        new_hand_text_position = (LEFT_DEAL_BUTTON + 55, TOP_DEAL_BUTTON + 35)
        button_list.append(draw_button_with_double_border(new_hand_rectangle, 'white', 'green', 'black', 'black', new_hand_text_position, 'NEW HAND'))
  #  print(button_list)
    return button_list


# check endgame conditions function 
def check_endgame(hand_act, deal_score, play_score, result, totals, surrender, add):
    # First check if my_hand exists and has elements
    if surrender:
        totals[1] += 1
        add = False
        return 5, totals, add # five is to to calcute the money in surrender

    if my_hand and len(my_hand) > 0:
        # For split hands
        if isinstance(my_hand[0], list) and len(my_hand) == 2:
            hand1_score = calculate_score(my_hand[0])
            hand2_score = calculate_score(my_hand[1])
            
            if not hand_act and deal_score >= 17:
                # Check winning conditions for each hand
                hand1_wins = (hand1_score <= 21 and (hand1_score > deal_score or deal_score > 21))
                hand2_wins = (hand2_score <= 21 and (hand2_score > deal_score or deal_score > 21))
                hand1_ties = (hand1_score == deal_score and hand1_score <= 21)
                hand2_ties = (hand2_score == deal_score and hand2_score <= 21)
                
                # If either hand wins, player wins
                if hand1_wins or hand2_wins:
                    result = 2  # Player wins
                # If no winning hand but at least one hand ties, it's a tie
                elif hand1_ties or hand2_ties:
                    result = 4  # Tie game
                # If no wins and no ties, dealer wins
                else:
                    result = 3  # Dealer wins
                
                #saves the wins,loses and ties in a list for later
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
                #saves the wins,loses and ties in a list for later
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

# makes the bouder of the double down buttn change coller if clikt.
def change_color_double_down(double_down, stand):
    if double_down and not stand:
        pygame.draw.rect(screen, 'purple', [LEFT_DOUBLE_DOWN_BUTTON, TOP_DOUBLE_DOWN_BUTTON, WIDTH_DOUBLE_DOWN_BUTTON, HEIGHT_DOUBLE_DOWN_BUTTON], 3, 5)
    
#if money is the string al you money is gone ore somthing it makes a new screen with some specs
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

            #quit if the time runs out (20 seconds)
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
            
            #makes everthing in the middle 
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
            # if split just show the split hands 
            draw_split_hands(my_hand, dealer_hand, reveal_dealer, current_hand_index)
            #calculate the score if player stands
            if reveal_dealer:
                dealer_score = calculate_score(dealer_hand)
                #dealer needs to get more the 17
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            draw_split_scores(my_hand, dealer_score, current_hand_index, reveal_dealer)
        else:
            # don't want to split
            player_score = calculate_score(my_hand)
            draw_cards(my_hand, dealer_hand, reveal_dealer)
            if reveal_dealer:
                dealer_score = calculate_score(dealer_hand)
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            draw_scores(player_score, dealer_score)
    # draw the nesserery buttons
    buttons = draw_game(active, records, outcome, aantal_games, money)
    change_color_double_down(double_down, stand)
    #put surrender back to false
    surrender = False

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # start the game
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(game_deck_original) #reset de deck
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    add_score = True
                    money_updated = False
                    current_hand_index = 0
                    # Ask the player to place their bet 
                    money_bet = get_bet_input(screen,money)  # Pass the player's available funds
                    print(f'player bet {money_bet}')
            else:
                
                #check whether any of the currently active buttons were clicked
                event_position = event.pos

                clicked_button = None

                for button in buttons:
                    if button.collidepoint(event_position):
                        clicked_button = button
                        break

                #if no button was clicked, skip to the next iteration of the loop
                if clicked_button is None:
                    continue

                # else look witch button got head and take the nesserery steps
                button_type = derive_button_type_from_position(clicked_button)

                # takeing the nesserery steps
                if button_type == "HIT":
                    if hand_active:
                        if want_split and isinstance(my_hand[0], list) and len(my_hand) == 2:
                            # if the cards are split let the hit until they reach higher then 2
                            my_hand, game_deck = deal_cards(my_hand, game_deck, want_split, current_hand_index)
                            if calculate_score(my_hand[current_hand_index]) > 21:
                                if current_hand_index == 0:
                                    current_hand_index = 1
                                    if calculate_score(my_hand[1]) > 21:
                                        hand_active = False
                                        reveal_dealer = True
                                # if score is highe the 21 (game over for that hand)
                                else:
                                    hand_active = False
                                    reveal_dealer = True
                                    stand = True
                        else:
                            # this is not split 
                            my_hand, game_deck = deal_cards(my_hand, game_deck)
                            if calculate_score(my_hand) > 21:
                                hand_active = False
                                reveal_dealer = True
                # let player end turn( stand)
                elif button_type == "STAND":
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
                #givis you cards
                elif button_type == "DEAL":
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
                elif button_type == "SPLIT":
                    want_split = True
                    my_hand = split_cards(want_split, my_hand)
                    split_cards(want_split, my_hand)
                # try double down 
                elif button_type == "DOUBLE_DOWN":
                    #print('works')
                    double_down = True
                    change_color_double_down(double_down,stand)
                #makes you surrend (end game) and does the nessery steps like calculating
                elif button_type == "SURRENDER":
                    reveal_dealer = True
                    surrender = True
                    hand_active = False


    # if player busts, autmaticlly end turn - treat like a stand
    if hand_active and not want_split and calculate_score(my_hand) > 21:
        hand_active = False
        reveal_dealer = True
    
    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, surrender, add_score)

    if surrender:
        surrender  = False

    if outcome != 0 and not money_updated:
        money = calculate_money(start_money, outcome, money,money_bet,want_split,double_down)
        money_updated = True
        run = quit_game(money)
    pygame.display.flip()
pygame.quit()