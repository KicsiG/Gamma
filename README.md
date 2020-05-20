# Gamma
Gamma


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
