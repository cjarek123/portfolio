import Data.Ord (comparing)
import Data.List ( delete, elemIndex)
import System.Random ( randomRIO )

data Number = Two | Four | Five | Six | Seven | Jack | Queen | King | Three | Ace
  deriving (Read, Enum, Eq, Show, Ord)

data Suit = Clubs | Diamonds | Hearts | Spades
  deriving (Read, Enum, Eq, Show, Ord)

data Card = Card Number Suit
  deriving (Eq, Show)

data Player = Player { hand :: [Card], deck :: [Card], player :: Bool}
  deriving (Show)

type Briscola = Suit
type Deck = [Card]
type Table = [Card]


-- Game initialisation

newDeck :: Deck
newDeck = [Card x y |  y <- [Clubs .. Spades], x <- [Two .. Ace]]

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
pickBriscola (briscola@(Card _ suit):rest) = (rest ++ [briscola], suit)

removeCard :: Deck -> Deck
removeCard = tail


--Mechanisms--

-- Print the player hand
displayHand :: Player -> IO ()
displayHand (Player [card1, card2, card3] _ _) = do
  print $ "1 " ++ show card1
  print $ "2 " ++ show card2
  print $ "3 " ++ show card3
displayHand (Player [card1, card2] _ _) = do
  print $ "1 " ++ show card1
  print $ "2 " ++ show card2
displayHand (Player [card1] _ _) = do
  print $ "1 " ++ show card1

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
checkTable table@(card1:card2:card3:_) briscola player1@(Player hand1 deck1 human1) player2@(Player hand2 deck2 human2) player3@(Player hand3 deck3 human3)
  | player == Just 0 = ([], Player hand1 (table ++ deck1) human1, player2, player3)
  | player == Just 1 = ([], Player hand2 (table ++ deck2) human2, player3, player1)
  | otherwise        = ([], Player hand3 (table ++ deck3) human3, player1, player2)
  where player = elemIndex (compareCards briscola (compareCards briscola card1 card2) card3) table

-- Compare two cards to find the highest one
compareCards :: Briscola -> Card -> Card -> Card
compareCards briscola card1@(Card number1 suit1) card2@(Card number2 suit2)
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
  


-- Game --

playGame :: Deck -> Player -> Player -> Player -> Table -> Briscola -> IO ()
playGame deck player1@(Player hand _ _) player2 player3 table briscola
  | null hand = do print "implement points" -- implement points
  | null deck = do
    (player1', table') <- playTurn player1 table
    (player2', table'') <- playTurn player2 table'
    (player3', table''') <-  playTurn player3 table''

    playGame [] player1' player2' player3' table''' briscola
  | otherwise = do
      print player1
      print player2
      print player3

      (player1', table') <- playTurn player1 table
      (player2', table'') <- playTurn player2 table'
      (player3', table''') <-  playTurn player3 table''

      let (table'''', player1'', player2'', player3'') = checkTable table''' briscola player1' player2' player3'

      let (deck', player1''') = draw deck player1''
      let (deck'', player2''') = draw deck' player2''
      let (deck''', player3''') = draw deck'' player3''

      print player1'''
      print player2'''
      print player3'''

      print table''''

      playGame deck''' player1''' player2''' player3''' table'''' briscola

playTurn :: Player -> Table -> IO (Player, Table)
playTurn player@(Player hand deck human) table
  | human    = do
      displayHand player
      playCard player table
  | otherwise = return (Player (tail hand) deck False, table ++ [head hand])



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
