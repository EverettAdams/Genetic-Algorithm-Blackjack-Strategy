#Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

#Defining Blackjack Simulation Components
class Shoe:
    #Method: Initialize instance variables for an object of class Shoe
    def __init__(self,deck_num):
        #.deck_num: Integer number of decks (of 52 cards) used by the casino in the shoe
        self.deck_num = deck_num
        #.cards: NumPy array of integers representing the values of each card the shoe in Blackjack
        #(represents the shoe itself)
        self.cards = np.array(deck_num * [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,
            8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11])

    #Method: Shuffles the order of each card in the shoe(each integer in the array)
    def shuffle(self):
        np.random.shuffle(self.cards)

    #Method: Deals a card
    def deal_card(self):
        #Returns card value at the top of the shoe (index = 0) and then deletes the card from shoe
        card = self.cards[0]
        self.cards = np.delete(self.cards,0)
        return card

class Player:
    #Method: Initialize instance variables for class Player
    def __init__(self, cash, strategy):
        #.cash: Float representing the amount of money the Player has available to bet ($)
        self.cash = cash
        #.strategy: List of 2 entries containing Hard and Soft strategy DataFrames
        self.strategy = strategy
        #.bet: Integer representing the amount of money the Player places in betting area ($)
        self.bet = 0
        #.hand: NumPy array of integers representing the values of the cards in the Player's hand
        self.hand = np.array([], dtype = int)
        #.count: Integer representing the sum of the values of the cards in the Player's hand
        self.count = 0

    #Method:
    def call_strategy(self,dealer_hand):
        if 11 in self.hand:
            return self.strategy[1].at[self.count, dealer_hand[0]]
        else:
            return self.strategy[0].at[self.count, dealer_hand[0]]

    #Method: Make a bet of value bet_amount $
    def make_bet(self,bet_amount):
        self.bet += bet_amount
        self.cash -= bet_amount

    #Method: Allow Player to get hit (accept another card to their hand) from a specified Shoe.cards object
    def hit(self, Shoe):
        self.hand = np.append(self.hand,Shoe.deal_card())
        self.count = np.sum(self.hand)

class Dealer:
    #Method: Initialize instance variables for an object of class Dealer
    def __init__(self):
        #.hand: NumPy array of integers representing the values of the cards for the Dealer's hand
        self.hand = np.array([], dtype = int)
        #.count: Integer representing the sum of the values of the cards in the Dealer's hand
        self.count = 0

    #Method: Allow Dealer to get hit (accept another card to their hand) from a specified Shoe.cards object
    def hit(self, Shoe):
        self.hand = np.append(self.hand,Shoe.deal_card())
        self.count = np.sum(self.hand)
