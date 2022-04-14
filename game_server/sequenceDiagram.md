sequenceDiagram
participant Player
participant PlayerOffTurn
participant Game
participant Board
participant Cardset

Note over Player: Create Game 
alt Player creates game
    Player->>+Game: createGame()
    Game->>-Player: gameID
end

Note over Player: Join Game 
    Player->>+Game: createPlayer(gameID)
    Game->>+Cardset: getAvailableCharacters(gameID)
    Cardset->>-Game: characterName
    Game->>-Player: playerID, characterName

Note over Player: Start Game 
alt Game does not have enough players 
loop Until minimum 3 players
    Player->>+Game: createGame()
    Game->>-Player: Error: not enough players
end
else Game has enough players
    Player->>+Game: startGame(gameID)
    Game->>+Cardset: pickCaseFile(gameID)
    Cardset->>-Game: caseFile
    Game->>+Cardset: dealRemainingCards(gameID)
    Cardset->>-Game: playerCards, visibleCards
    Game->>+Board: createBoard(gameID)
    Board->>-Game: gameBoard
    Game->>Game: changeGameState(gameID)
    Game->>-Player: gameBoard, cardSet, visibleCards
end

Note over Player: Player's turn
loop for each player
    Game->>+Player: notifyTurn

    alt player makes move
        Player->>+Game: move(newPosition)
        Game->>+Board: checkMove(newPosition)
        Board->>-Game: gameBoard
        Game->>-Player: gameBoard
        Game->>PlayerOffTurn: gameBoard

    else player makes suggestion
        Player->>+Game: suggestion(cardSet)
        Game->>+Cardset: checkCardset(cardSet)
        loop for each player off turn, until rebuttal
            Game->>Cardset: checkPlayerCards(playerID)
            alt player off turn cannot refute
                Cardset->>Game: None

            else player off turn can refute with one card
                Cardset->>Game: rebuttalCard
                Game->>Player: rebuttalCard

            else player off turn can refute with multiple cards
                Cardset->>Game: rebuttalCards
                Game->>+PlayerOffTurn: rebuttalCards
                PlayerOffTurn->>-Game: rebuttalCard
            end
        end
        Game->>-Player: rebuttalCard

    else player makes accusation
        alt accusation is correct
            Player->>+Game: accusation(cardSet)
            Game->>+Cardset: checkCardset(cardSet)
            Cardset->>-Game: true
            Game->>Game: updatePlayerStatus(winner)
            Game->>-Player: true
            Game->>PlayerOffTurn: gameOver
        else accusation is incorrect
            Player->>+Game: accusation(cardSet)
            Game->>+Cardset: checkCardset(cardSet)
            Cardset->>-Game: false
            Game->>Game: updatePlayerStatus(loser)
            Game->>-Player: false
        end
    end
    
    Player->>-Game: notifyTurnEnd
end
Note over Player: Game end




