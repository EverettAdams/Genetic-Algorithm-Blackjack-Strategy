#Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import blackjack as bj

#Defining Genetic Algorithm Components
class Individual:
    def __init__(self,strategy):
        self.strategy = strategy
        self.fitness = 0

#Create randomized strategy
def create_strategy():
     hard = pd.DataFrame(np.random.randint(0,2,size=(18,10)),index = [i for i in range(4,22)], columns = [n for n in range(2,12)])
     soft = pd.DataFrame(np.random.randint(0,2,size=(10,10)), index = [i for i in range(12,22)], columns = [n for n in range(2,12)])
     return [hard,soft]

#Create population of N individuals with randomized strategies
def create_population(N):
    population_df = pd.DataFrame(columns = ['individual','fitness'])
    population_df['individual'] = [Individual(create_strategy()) for i in range(N)]
    return population_df

#Evaluate and record fitness of population
def fitness(population_df, simulation_turns):

    # Adjustable Simulation Parameters
    N = simulation_turns #Number of turns
    BA = 1 #Amount of cash bet each round ($)
    Initial_Cash = 100000 #Starting amout of cash for the player ($)

    for individual in population_df['individual']:
        #Instantiate Game Objects
        game_shoe = bj.Shoe(8) #Instantiate object of class Shoe (shoe of cards)
        game_shoe.shuffle() #Shuffle order of array game_shoe.cards
        player = bj.Player(Initial_Cash, individual.strategy) #Instantiate object of class Player with a cash amount of 100$
        dealer = bj.Dealer() #Instantiate object of class Dealer
        entity_list = np.array([player,dealer]) #List of entities(objects of Player and Dealer class)

        #Game Logic
        for turn in range(N):

            #Refill Shoe when number of cards in shoe is low (below 50)
            if len(game_shoe.cards) < 50:
                shoe_add = bj.Shoe(8)
                shoe_add.shuffle()
                game_shoe.cards = np.append(game_shoe.cards,shoe_add.cards)

            #Clear hand and count of each entity in the game
            for entity in entity_list:
                entity.hand = np.array([], dtype = int)
                entity.count = 0

            #Placing of Bets
            player.make_bet(BA)

            #Dealing of Opening Hand + Update Count
            for cards in range(2):
                player.hit(game_shoe)
                dealer.hit(game_shoe)


            #Player's Turn
            while True:
                #Check for Blackjack in Opening Hand
                if len(player.hand) == 2 and player.count == 21:
                    player.count = -2
                    break
                #Soft Ace --> Hard Ace
                if 11 in player.hand and player.count>21:
                    index = np.where(player.hand == 11)[0][0]
                    player.hand[index] = player.hand[index] - 10
                    player.count = np.sum(player.hand)
                #Player Decision (Hit/Stand)
                move = player.call_strategy(dealer.hand)
                #Player move: Hit
                if move == 1:
                    #Deal the player a card & update count
                    player.hit(game_shoe)
                    #Check if player has a soft ace and if count has gone over 21
                    if 11 in player.hand and player.count>21:
                        index = np.where(player.hand == 11)[0][0]
                        player.hand[index] = player.hand[index] - 10
                        player.count = np.sum(player.hand)
                    #Bust if count is over 21
                    if player.count > 21:
                        player.count = -1
                        break
                #Player move: Stand
                elif move == 0:
                    break

            #Dealer's Turn
            while True:
                #Soft ace --> Hard ace
                if 11 in dealer.hand and dealer.count>21:
                    index = np.where(dealer.hand == 11)[0][0]
                    dealer.hand[index] = dealer.hand[index] - 10
                    dealer.count = np.sum(dealer.hand)
                #Dealer Decision (Stand on soft 17)
                #Dealer move: Hit
                if dealer.count < 17:
                    dealer.hit(game_shoe)
                    #Check if dealer has a soft ace and if count has gone over 21
                    if 11 in dealer.hand and dealer.count>21:
                        index = np.where(dealer.hand == 11)[0][0]
                        dealer.hand[index] = dealer.hand[index] - 10
                        dealer.count = np.sum(dealer.hand)
                    #Bust if count is over 21
                    if dealer.count > 21:
                        dealer.count = -1
                        break
                #Dealer move: Stand
                elif dealer.count >= 17:
                    break


            #Payout
            if player.count == -2 and dealer.count != 21: #The player gets a Blackjack and the dealer does not: Win
                player.cash += 2.5 * player.bet
                player.bet = 0
            elif player.count == -1: #The player busts before the dealer: Loss
                player.bet = 0
            elif dealer.count == -1: #The dealer busts & the player does not: Win
                player.cash += 2 * player.bet
                player.bet = 0
            elif player.count == dealer.count: #The player and the dealer have the same count: Tie
                player.cash += player.bet
                player.bet = 0
            elif player.count > dealer.count: #The player has a higher count than the dealer: Win
                player.cash += 2 * player.bet
                player.bet = 0
            else: #The dealer has a higher count than the player: Loss
                player.bet = 0

        #Record Temporary Fitness of Individual
        population_df['fitness'].loc[population_df['individual'] == individual] = player.cash - Initial_Cash
        population_df['fitness'] = pd.to_numeric(population_df['fitness'])

#Select individuals approriate for reproduction (Tourney 4)
def selection(population_df):
    selected_individuals = []

    for i in range(population_df.shape[0]//4):
        tourney_set = population_df[4*i:4*i+4]
        selected_individuals.append(tourney_set['individual'][tourney_set['fitness'].idxmax()])

    return selected_individuals

#Input two individuals and output two children Individuals
def crossover(parent_1,parent_2):
    x_slice = random.randint(2,10)
    y_slice_hard = random.randint(4,20)
    y_slice_soft = random.randint(12,20)

    #Placeholder Variables for Offspring Strategies
    offspring_strategy_1 = [0,0]
    offspring_strategy_2 = [0,0]

    #Hard Stratgies of Offspring
    offspring_strategy_1[0] = pd.concat([parent_1.strategy[0].loc[:, 2:x_slice].loc[4:y_slice_hard].join(parent_2.strategy[0].loc[:, x_slice+1:11].loc[4:y_slice_hard]), parent_2.strategy[0].loc[:, 2:x_slice].loc[y_slice_hard+1:21].join(parent_1.strategy[0].loc[:, x_slice+1:11].loc[y_slice_hard+1:21])])
    offspring_strategy_2[0] = pd.concat([parent_2.strategy[0].loc[:, 2:x_slice].loc[4:y_slice_hard].join(parent_1.strategy[0].loc[:, x_slice+1:11].loc[4:y_slice_hard]), parent_1.strategy[0].loc[:, 2:x_slice].loc[y_slice_hard+1:21].join(parent_2.strategy[0].loc[:, x_slice+1:11].loc[y_slice_hard+1:21])])
    #Soft Strategies of Offsrping
    offspring_strategy_1[1] = pd.concat([parent_1.strategy[1].loc[:, 2:x_slice].loc[12:y_slice_soft].join(parent_2.strategy[1].loc[:, x_slice+1:11].loc[12:y_slice_soft]), parent_2.strategy[1].loc[:, 2:x_slice].loc[y_slice_soft+1:21].join(parent_1.strategy[1].loc[:, x_slice+1:11].loc[y_slice_soft+1:21])])
    offspring_strategy_2[1] = pd.concat([parent_2.strategy[1].loc[:, 2:x_slice].loc[12:y_slice_soft].join(parent_1.strategy[1].loc[:, x_slice+1:11].loc[12:y_slice_soft]), parent_1.strategy[1].loc[:, 2:x_slice].loc[y_slice_soft+1:21].join(parent_2.strategy[1].loc[:, x_slice+1:11].loc[y_slice_soft+1:21])])

    return [Individual(offspring_strategy_1), Individual(offspring_strategy_2)]

# Produce population of reproduced individuals from selected individuals of previous population
def reproduction(selected_individuals,population_size):
    next_generation = []
    for i in range(population_size//8):
        parent_1 = selected_individuals[2*i]
        parent_2 = selected_individuals[2*i+1]

        for n in range(4):
            next_generation.extend(crossover(parent_1, parent_2))
    random.shuffle(next_generation)
    return next_generation
