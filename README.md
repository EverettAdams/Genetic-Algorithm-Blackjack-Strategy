# Genetic-Algorith-Blackjack-Strategy

## Context
This project was submitted as a term project for the Introduction to Computer Programming in Engineering and Science course at Dawson College for the winter 2020 term. The scope of the project was to apply the Python programming knowledge and scientific computing principles that were taught throughout the course in an applied setting of the students choice.

# Task
The objective of the project was to develop a genetic algorithm that optimizes a player betting strategy for a simplified version of Blackjack. The algorithmically generated strategy is compared against other betting strategies to gauge its performance. Notably, the output of the genetic algorithm was compared against the mathematically optimal  methodology, basic strategy, and a randomized betting strategy. Ultimately, it was found that the optimized strategy only performed 1.3% worse than basic strategy indicating that the genetic algorithm is a good framework for developing a Blackjack betting strategy.

Despite the interesting results, there are many improvements that can be made. It would be valuable to expand the genetic algorithm to the complete version of Blackjack including additional player actions (e.g. split, doubling, splitting). Next, it would be valuable to increase the number of Blackjack hands that were simulated in the fitness evaluation process. This would allow the algorithm to distinguish between strategies with small differences as the effect of these small discrepencies have a more pronounced effect the more hands of Blackjack that are played given the random nature of the game. This would require in more time-efficient code as the current number of hands of Blackjack was chosen due to time constraints.
