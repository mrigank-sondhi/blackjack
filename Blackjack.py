#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
from IPython.display import clear_output
from time import sleep

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Ace','Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
play_game = True
blackjack = 0

class Card:
    
    def __init__(self,suit='null',rank=0):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'
    
class Deck:
    
    def __init__(self):
        self.deck = []
        self.cardcount = 51
        for suit in suits:
            for rank in ranks:
                card = Card(suit,rank)
                self.deck.append(card)
    
    def display(self):
         for card in self.deck:
                print(card)
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        i = random.randint(0,self.cardcount)
        card = self.deck[i]
        print(card)
        self.deck.remove(card)
        self.cardcount -= 1
        return card
    
class Hand:
    
    def __init__(self):
        self.cards = []
        self.value = 0   
        self.aces = 0    
    
    def add_card(self,card):
        self.cards.append(card)
        if card.rank == 'Ace':
            self.aces += 1
        self.value += values[card.rank]
        if self.aces > 0:
            self.adjust_for_ace()    
    
    def adjust_for_ace(self):
        if self.value > 21:
            self.value -= 10
            self.aces -= 1
            
class Chips:
    
    def __init__(self):
        self.total = 2500  
        self.bet = 0
        
    def win_bet(self):
        if blackjack == 1:
            print(f'You win {int(1.5*self.bet)}!')
            self.total += 1.5*self.bet
            print(f'You now have : {int(self.total)}')
        else:
            print(f'You win {self.bet}!')
            self.total += self.bet
            print(f'You now have : {int(self.total)}')
    
    def lose_bet(self):
        print(f'You lost {self.bet}!')
        self.total -= self.bet
        print(f'Remaining : {int(self.total)}')
        
def take_bet(chips):
    print(f'You have {int(chips.total)} chips.')
    while(True):
        try:
            chips.bet = int(input('Place your bet:'))
            if (chips.bet>chips.total):
                print(f'Please enter a value less than or equal to {chips.total}!')
            else:
                break
        except:
            print('Please enter an integer value!')        
            
def hit(deck,hand):
    card = Card()
    card = deck.deal()
    hand.add_card(card)
    
def hit_or_stand(deck,hand):
    global play_game
    if hand.value == 21:
        play_game = False
        sleep(2)
        return
    choice = input('Press H to hit\t\tPress S to stand')
    if choice == 'H' or choice == 'h':
        hit(deck,hand)
    else:
        play_game = False
        sleep(2)
        
def push(player,dealer):
    
    if player.value>21 and dealer.value>21:
        print('Push!')
        play_game = 1
        sleep(2)
        return True
    elif player.value == dealer.value:
        print('Push!')
        play_game = 1
        sleep(2)
        return True
    else:
        return False

def player_busts(player):
    if player.value>21:
        print('\n\nPlayer busts!')
        print('Dealer wins!')
        return True
    else:
        return False
        
def dealer_busts(dealer):
    if dealer.value>21:
        print('\n\nDealer busts!')
        print('Player wins!')
        return True
    else:
        return False

def win_or_lose(player,dealer):
    if player.value > dealer.value:
        print('\n\nPlayer wins!')
        return True
    else:
        print('\n\nDealer wins!')
        return False
    
def board(player,dealer):
    clear_output()
    if play_game:
        print(f'DEALER\t\t\t\t Value:{values[dealer.cards[0].rank]}\n\n') 
        print(dealer.cards[0])
        print(f'-hidden-\n\n\n\n\nPLAYER\t\t\t\t Value:{player.value}\n\n') 
        for card in player.cards:
            print(card)
    else:
        print(f'DEALER\t\t\t\t Value:{dealer.value}\n\n') 
        for card in dealer.cards:
            print(card)
        print(f'\n\n\n\nPLAYER\t\t\t\t Value:{player.value}\n\n') 
        for card in player.cards:
            print(card)
            
chips = Chips()
while True:
    clear_output()
    play_game = True
    blackjack = 0
    if chips.total == 0:
        chips.total = 2500
    print('Welcome to Blackjack!')
    sleep(1)
    take_bet(chips)
    deck = Deck()
    dealer = Hand()
    player = Hand()
    for i in dealer,player:
        for j in range(0,2):
            i.add_card(deck.deal())
    if player.value == 21:
        blackjack = 1
        board(player,dealer)
        print('\nB-L-A-C-K-J-A-C-K')
        play_game = False
        sleep(2)
    
    while play_game:
        board(player,dealer)
        if player.value>21:
            print('You busted!')
            play_game = False
            sleep(2)
            break
        hit_or_stand(deck,player)
        
    while dealer.value<17:
        hit(deck,dealer)
        board(player,dealer)
        
    else:
        board(player,dealer)
    
    if push(player,dealer):
        sleep(1)
        continue
    elif player_busts(player):
        chips.lose_bet()
    elif dealer_busts(dealer):
        chips.win_bet()
    elif win_or_lose(player,dealer):
        chips.win_bet()
    else:    
        chips.lose_bet()
        
    for _ in dir():
            if _ == 'deck' or _ == 'dealer' or _ == 'player' or _ == 'choice':
                del globals()[_]
    if chips.total == 0:
        print('You are out of chips!')
    choice = input('Do you want to play again(Y/N)?')
    if choice == 'y' or choice == 'Y':
        continue
    else:
        break        

