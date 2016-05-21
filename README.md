# CS229_Project
This is the repo for CS 229 (Machine learning), spring 2016, Stanford
Team: 
Hubert Teo\n
Yuetong Wang\n
Jiren Zhu

We are writing a hearthstone AI as our final class project.

The game system we are operating on is forked from the hearthbreaker platform by danielyule and others. We appreciate the great infrastructure that they constructed which would allow us to build on easily.

Notes:

For the hearthbreaker simulator
Before running the program, resize the terminal to be bigger, else there would be an error.

How the engine works: 
The object Game manages all the game states. It has two player objects which stand for the entire states of each player. Each player holds attributes like deck, hand and minions. Yet the player is mostly an attribute holder. An agent is a decision maker for player. It decides which cards to play and which targets to point to. We should be writing a new agent class and modifying some of the game/player engine to allow our AI to have all the information.

First step of the work. 
In the first part of the project we will generate some games by the existing AI on a specific deck and then record the winning/losing situation of respective game states. We will run some supervised learning algorithms to teach the AI how to evaluate the board.

Extracting feature:
For each player:
Hand number:
Deck depth:
Mana:
Hero Health:
Minion vectors * 7: Attack, Health, Can_attack