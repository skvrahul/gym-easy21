## Overview
This is a Gym environment for the game Easy21 as proposed in the assignment for David Silver's RL Course.
The assignment can be found [Here](http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching_files/Easy21-Johannes.pdf)

## Installation
The environment can be installed as a standalone python package dependent on *gym*   

`git clone https://github.com/skvrahul/gym-easy21.git`   
`cd gym-easy21`   
`pip install -e . `

## Details

* Name: env-easy21-v0
* [Environment Definition](http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching_files/Easy21-Johannes.pdf)

### Description
Play the blackjack like game Easy21 against a dealer who has the following policy:   
- Always stick on any sum greater than or equal to 17
- Hit otherwise



### Observation

Type: Tuple(Box(1), Box(1))

Num | Observation  | Min | Max  
----|--------------|-----|----   
0   | Dealers Card | 1   | 10
1   | Players Sum  | 1   | 21


### Actions

Type: Discrete(2)

Num | Action    
----|--------------   
0   | Hit  
1   | Stick 


### Reward
Reward is   
`-1` if the Dealer wins,   
`0` if it is a Draw and   
`1` if the player wins.    

### Starting State

Both player and dealer start with a random Black card [1, 10]   


### Episode Termination
The episode terminates when either dealer or player goes bust or when both players stick
