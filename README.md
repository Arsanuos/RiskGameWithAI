# Risk Game with AI
## Introduction
Computers playing games like humans, has been always a very hard problem, as it requires too much computations and memory to simulate the way that human use to think. Here AI field shows up, as it tries to solve the problems it faces rationally, according to some heuristics and search algorithms to reach the best solution.

## Overview
In this repo, we tried to solve one of the famous search problem in the field of AI, RISK game. we solved simplified and abstract version of it, you can check the [rules](http://web.mit.edu/sp.268/www/risk.pdf) of full version of the game.

## Board Overview
In this version, the board is just an undirected graph, where each country is represented by node, and the roads between each two nodes are represented as edge, we call group of nodes (countries) as partition (continent) which has to be told to the application to assign bonus troops according to it, as we will discuss later.

## Assumed Rules
This version of the game is more general, but not necessarily more complicated. The following is list of assumptions:

1. RISK is a multi-player game, but we will assume that only 2 players are in the game in the simplified version.

2. RISK has cards that can be cached in for armies - we will have no cards in our version. Instead  of  cards,  a  player  which  conquers  at  least  one  node  (territory),  receives  an additional bonus of 2 armies at the next turn.

3. Player gets extra bonus, each turn once it capture a partition (continent) on the board, unless it loses it during the game. but it can get it back once it got the partition again.

4. Amount of bonus of each partition is defined while defining each partition.

5. The partition is defined as: bonus value, list of indexes of each node. i.e. when defining partition like this (5 0 1 2), we mean that the player will get bonus value = 5, when it capture the nodes with indexes = 0, 1, and 2. Note that each node on the board must belong to only one partition.

6. The battles are deterministic.  Denote A(v) the number of armies
in node v.  node v can attack node u only if there is an edge between these vertices, and A(v)−A(u)> 1.  As a result of the battle, each opposing player loses A(u) armies, and the attacking player must move at least 1 army to u, but must leave at least 1 army in v.

7. Initial placement of armies is determined as part of the defining the board environment.

8. When getting the armies at the beginning of a turn, they must all be placed on the same node.

9. Initially, a turn will consist of: placing the bonus armies at the beginning of the turn, moving armies from one node to the other, and doing at most one attack (including moving armies into the captured territory). There will be no fortifying step, for simplicity.

10. The bonus completely placed into one node, at the beginning of each turn for each player.   

11. Each player has at most one move, he can do with his troops, moving troops should be from one node to the other that belongs to the current player making the movement.

12. Each player has at most one attack, from one of his node to another node belongs to the enemy. the attack is successful, if it satisfied the above attack rules.

13. Each agent would make his attack according to heuristic, except for the human agent, as it would attack as he wants according to his heuristic.

## Objective
The goal of the game is to conquer the world in the smallest number of turns.

## Agents

### Simple Agents

#### Passive Agent
- Agent never attacks, and always places all its additional armies on the node that has the fewest armies, breaking ties by favoring the lowest-numbered vertex.

#### Pacifist Agent
- Agent that places its bonus army troops, as the Passive agent, then conquers only one node (if it can), such that it loses as few armies as possible.

#### Aggressive Agent
- Agent that places its bonus armies on the node with the most armies, and greedily attempts to attack so as to cause the most damage, i.e. to prevent the enemy getting a continent bonus.

In the above simple agents, ties are broken by selecting the smallest numbered node among all that are equally good.  At this stage, you can try running agents against each other, or play human against agent.  As we allow user to select one of which agents will be in a game run.

### Intelligent Agents

We also implemented intelligent agents that plays against a completely passive agent, and attempts to win in as few turns as possible. There will be three types of agents, each one employs a different search algorithm, defined below. All agents will use a heuristic function will be discussed down.

#### Greedy Agent
- A greedy agent, that picks the move with the best immediate heuristic value.

#### A\* Agent
- An agent using A* search, with the same heuristic.

#### Real-time A\* (RTA\*) Agent
- An agent using real-time A* search.  

## Design of the Project

### UML Diagram
//TODO add picture to that has the UML diagram.

### Project Structure
- **Agent**: Contains the implementation of the agents.
- **Parser**: Contains the implementation of the intermediate layer between the HTML page and the back-end.
- **Heuristic**: Contains the heuristics of placing bonus, and the attacks that is used by the simple agents.
- **Evaluation**: Contains the heuristic Evaluation function.
- **State**: Contains the implementation of the game state and the other classes, that used to describe the current state of the game.
- **frontend**: Contains the HTML, CSS, and the JS. which is the implementation of the front-end page.
- **graph**: Contains the Django files for back-end.

## How to run it.

### Prerequisite installed software

1. Python 3.

2. Django package compatible with Python 3.  

### Run steps

1. Clone the project `git clone https://github.com/Arsanuos/RiskGameWithAI.git`.

2. Run this command `python manage.py runserver` from the terminal while you are inside the project directory, which will portal the project on port `8000`.

3. Enjoy the game :smile: .


## Screen Shots

//TODO put the screen shot.

## Authors


* **Amr Hendy** [AmrHendy](https://github.com/AmrHendy)

* **Arsanous Eissa** [Arsanous](https://github.com/Arsanuos)

* **Muhammed Ibrahim** [MuhammedKhamis](https://github.com/MuhammedKhamis)


## Contribute


Contributions are always welcome!

Please read the [contribution guidelines](contributing.md) first.


## License


This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

##
Made with love &nbsp; :heart: .
