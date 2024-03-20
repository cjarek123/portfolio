import Data.List ( delete, elemIndex)
import System.Random ( randomRIO )

import Types
import Computer


-- Game initialisation

newDeck :: Deck
newDeck = [Card x y pts |  y <- [Clubs .. Spades], x <- [Two .. Ace],
          pts <- [case x of
            Jack -> 2
            Queen -> 3
            King -> 4
            Three -> 10
            Ace -> 11
            _ -> 0]]

-- Generate a random number and pick the card in that position from the deck
shuffleDeck :: Deck -> IO Deck
shuffleDeck deck
  | null deck = return deck
  | otherwise = do
    let deckLen = length deck -1
    n <- randomRIO(0, deckLen)
    let randomCard = deck !! n
    tailShuffle <- shuffleDeck $ delete randomCard deck
    return $ randomCard : tailShuffle

-- Give three cards to each player
dealCards :: Deck -> (Deck, Player, Player, Player)
dealCards deck =
  let
    player1 = take 3 deck
    player2 = take 3 $ drop 3 deck
    player3 = take 3 $ drop 6 deck
    updatedDeck = drop 9 deck
  in
    (updatedDeck, Player player1 [] True, Player player2 [] False, Player player3 [] False)

-- Take the first card of the deck as briscola and put it at the end of the deck
pickBriscola :: Deck -> (Deck, Briscola)
pickBriscola (briscola@(Card _ suit _):rest) = (rest ++ [briscola], suit)

removeCard :: Deck -> Deck
removeCard = tail


--Mechanisms--

-- Print the player hand
displayHand :: Player -> IO ()
displayHand (Player handCards _ _) = do
  putStrLn "\nPlayer's Hand:"
  mapM_ (\(i, card) -> putStrLn $ show i ++ " " ++ show card) indexedCards
  where
    indexedCards = zip [1..] handCards

displayTable :: Table -> IO ()
displayTable table = mapM_ printCard table

printCard :: Card -> IO ()
printCard (Card number suit _) = putStr $ show number ++ " of " ++ show suit ++ "   "

-- Make the player choose a card to play
playCard :: Player -> Table -> IO (Player, Table)
playCard (Player [card1, card2, card3] deck _) table = do
  c <- getChar
  case c of
    '1' -> return (Player [card2, card3] deck True, table ++ [card1])
    '2' -> return (Player [card1, card3] deck True, table ++ [card2])
    '3' -> return (Player [card1, card2] deck True, table ++ [card3])
    _   -> playCard (Player [card1, card2, card3] deck True) table
playCard (Player [card1, card2] deck _) table = do
  c <- getChar
  case c of
    '1' -> return (Player [card2] deck True, table ++ [card1])
    '2' -> return (Player [card1] deck True, table ++ [card2])
    _   -> playCard (Player [card1, card2] deck True) table
playCard (Player [card1] deck _) table = do
  c <- getChar
  case c of
    '1' -> return (Player [] deck True, table ++ [card1])
    _   -> playCard (Player [card1] deck True) table

-- Find the highest card and give the table to the right player
checkTable :: Table -> Briscola -> Player -> Player -> Player -> (Table, Player, Player, Player)
checkTable table@[card1, card2, card3] briscola player1@(Player hand1 deck1 human1) player2@(Player hand2 deck2 human2) player3@(Player hand3 deck3 human3)
  | player == Just 0 = ([], Player hand1 (table ++ deck1) human1, player2, player3)
  | player == Just 1 = ([], Player hand2 (table ++ deck2) human2, player3, player1)
  | otherwise        = ([], Player hand3 (table ++ deck3) human3, player1, player2)
  where player = elemIndex (compareCards briscola (compareCards briscola card1 card2) card3) table

-- Compare two cards to find the highest one
compareCards :: Briscola -> Card -> Card -> Card
compareCards briscola card1@(Card number1 suit1 _) card2@(Card number2 suit2 _)
  | suit1 == suit2 && number1 > number2 = card1
  | suit1 == suit2 && number1 < number2 = card2
  | suit2 == briscola = card2
  | otherwise = card1

-- Give a new card to the player
draw :: Deck -> Player -> (Deck, Player)
draw deck (Player hand deck' human) = (tail deck, Player (head deck : hand) deck' human)

-- finishRound :: Table -> [Card]
-- finishRound (card1:card2:card3:_)
--   | compareCards card1 card2 == GT = if compareCards card1 card3 == GT then [] else

-- Tally up the points from a single deck
tally :: Player -> Int
tally player@(Player _ deck _) =
  foldr (\(Card _ _ pts) rec -> pts + rec) 0 deck

-- Create a list of all players' scores
scoreList :: [Player] -> [Int]
scoreList = map tally

-- Print out the scores of each player
printScores :: [Int] -> Int -> IO ()
printScores (score:scores) index = do
  putStrLn $ "Player " ++ show index ++ ": " ++ show score
  printScores scores (index + 1)

-- From a list of scores, determine the index of the winner; -1 if there's a draw
indexWinner :: [Int] -> Int -> Int -> Int
indexWinner [] currTop index = index
indexWinner (score:scores) currTop index
  | score > currTop = indexWinner scores score (index + 1)
  | score < currTop = indexWinner scores currTop (index + 1)
  | score == currTop = -1


-- Game --

playGame :: Deck -> Player -> Player -> Player -> Table -> Briscola -> IO ()
playGame deck player1@(Player hand _ _) player2 player3 table briscola
  | null hand = do print "implement points" -- implement points
  | null deck = do
    (player1', table') <- playTurn player1 table briscola
    (player2', table'') <- playTurn player2 table' briscola
    (player3', table''') <-  playTurn player3 table'' briscola

    playGame [] player1' player2' player3' [] briscola
  | otherwise = do

      print player1
      print player2
      print player3

      (player1', table') <- playTurn player1 table briscola
      (player2', table'') <- playTurn player2 table' briscola
      (player3', table''') <-  playTurn player3 table'' briscola

      let (table'''', player1'', player2'', player3'') = checkTable table''' briscola player1' player2' player3'

      let (deck', player1''') = draw deck player1''
      let (deck'', player2''') = draw deck' player2''
      let (deck''', player3''') = draw deck'' player3''

      print player1'''
      print player2'''
      print player3'''

      playGame deck''' player1''' player2''' player3''' [] briscola

playTurn :: Player -> Table -> Briscola -> IO (Player, Table)
playTurn player@(Player hand deck human) table briscola
  | human    = do
    putStrLn "\nTable:"
    displayTable table
    displayHand player
    playCard player table
  | otherwise = doTurn player table briscola

-- MAIN --
main :: IO ()
main = do
  deck <- shuffleDeck newDeck
  let deck' = removeCard deck
  let (updatedDeck, player1, player2, player3) = dealCards deck'
  let (updatedDeck', briscola) = pickBriscola updatedDeck
  print briscola
  print $ length updatedDeck'
  playGame updatedDeck' player1 player2 player3 [] briscola
  print $ length updatedDeck'
