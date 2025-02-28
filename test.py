import copy
import random
import pygame


# game variables
pygame.init()
cards = ['2', '3','4','5','6','7','8','9','10','J','Q','K','A']
one_deck= 4 * cards
decks = 4

WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()

font = pygame.font.SysFont('freesantbold.ttf',44)
active = False

# win , loss, draw/tie
records = [0,0,0]
player_score= 0
dealer_score = 0
initial_deal = False
my_hand= []
dealer_hand= []
outcome = 0
reveal_dealer=False
# deal cards by selecting randomly from deck, and make function for one card at a time

def deal_cards( current_hand,current_deck):
    card= random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    print(current_hand,current_deck)
    return current_hand,current_deck

# draw cards visually ont screen 
def draw_cards(player,dealer,reveal):
    for i in range (len (player)):
        pygame.draw.rect(screen,'white',[70+(70 * i), 460 + (5*i),120,220],0,5)
        screen.blit(font.render(player[i],True,'black'), (75 + 70*i,435+5*i))
        screen.blit(font.render(player[i],True,'black'), (75 + 70*i,635+5*i))
        pygame.draw.rect(screen,'red',[70+(70 * i), 460 + (5*i),120,220],5,5)
        
        




# draw game conditions and buttons
def draw_game(act,records):
    button_list = []
    # intitlaly on startuup ( not active )  only option is to deal new hand
    if not act: 
        deal = pygame.draw.rect(screen,'white',[150,20,300,100],0,5)
        pygame.draw.rect(screen,'green',[150,20,300,100],3,5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text,(200,50))
        button_list.append(deal)
    # one game started, shot hit and stand buttons and  win/loss records
    else:
        
        hit = pygame.draw.rect(screen,'white',[0,700,300,100],0,5)
        pygame.draw.rect(screen,'green',[0,700,300,100],3,5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text,(55,735))
        button_list.append(hit)

        stand = pygame.draw.rect(screen,'white',[300,700,300,100],0,5)
        pygame.draw.rect(screen,'green',[300,700,300,100],3,5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text,(355,735))
        button_list.append(stand)
        score_text = font.render (f'Wins: {records[0]} Losses: {records[1]} Tie: {records[2]}', True,'white')
        screen.blit(score_text, (15, 840))
    return button_list




# main game  loop 

run = True
while run:
    # run game at our framrate and fill sceen with bg color
    timer.tick(fps)
    screen.fill('black')

    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand,game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand,game_deck)
        print (my_hand,dealer_hand)
        initial_deal= False
            



    # once game is activated, and dealt, calculate scores and display cards
    if active: 
        draw_cards(my_hand, dealer_hand, reveal_dealer)
    buttons=draw_game(active,records)

    # enent hhandling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active =True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand= []
                    outcome = 0
        
    pygame.display.flip()
pygame.quit()
