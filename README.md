# Gamma

Least Unique Positive Integer implementation

It is a fun game and now that people are stuck in home office it can be a great way to have to start the day with a common activity. The game has been studied a lot and has some maths behind how people behave and what really is optimal in some respect.

The rules of the Game
- It is a Multiplayer game
- Each player picks a positive integer. The lowest unique integer wins.


## Features

- Single Global Playground 
- Trusted players (no registration)
- Explicit start of a round
- Within an active round:
  - A user can add their number with a name as part of the game. The name is unique and cannot be reused in the round.
- All users vote is collected.
- Compete the Round, return roundID
- Round Results: winner, and the number
- Listing all rounds with IDs and start date, end date, number of participants
- Querying the results of any rounds including the most recent one: Winner and winning number
- Querying the statistics of any round: distribution of votes from 1 to the max number voted for in that round.
- Auto Round Close
- More advanced GUI 

## General resource and the individual endpoints

- GET /: initial page
- POST /: you can enter or not the game, create new round
- GET /sorry: page if you do not want to play
- GET /thanks: thanks page after playing
- GET /submit: initial submit page
- POST /submit: submit your name and you number
- GET /close: close the active game round
- GET /current_round: get the current acite game stands
- GET /get_all_rounds: list all finished game rounds (all data)
- GET /list_all_rounds: list all finished game rounds (id: start, end, participant numbers)
- GET /round/{round_id}: get winner and winner number by id
- GET /round2: get winner and winner number by round id
- GET /statistics/{round_id}: get game votes distribution by round is
- GET /statistics2: get game votes distribution by round is
