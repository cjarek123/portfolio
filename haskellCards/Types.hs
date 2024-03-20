module Types where

data Number = Two | Four | Five | Six | Seven | Jack | Queen | King | Three | Ace
    deriving (Read, Enum, Eq, Show, Ord)

data Suit = Clubs | Diamonds | Hearts | Spades
    deriving (Read, Enum, Eq, Show, Ord)

data Card = Card Number Suit Points
    deriving (Eq, Show, Ord)

data Player = Player { hand :: [Card], deck :: [Card], human :: Bool}
    deriving (Show)

type Briscola = Suit
type Points = Int
type Deck = [Card]
type Table = [Card]