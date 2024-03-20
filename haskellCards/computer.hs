module Computer (doTurn) where

import Types

isSingleElement :: [a] -> Bool
isSingleElement [_] = True
isSingleElement _ = False

getSuit :: Card -> Suit
getSuit (Card _ suit _) = suit

hasBriscola :: Player -> Briscola -> Bool
hasBriscola (Player hand _ _) briscola = any ((== briscola). getSuit) hand

hasGreaterCard :: [Card] -> [Card] -> Bool
hasGreaterCard hand [] = False
hasGreaterCard hand table = any (\card -> all (< card) table) hand

sortAsc :: [Card] -> [Card]
sortAsc [] = []
sortAsc [x] = [x]
sortAsc (x:y:xs)
    | x <= y = x : sortAsc (y:xs)
    | otherwise = y : sortAsc (x:xs)

sortDec :: [Card] -> [Card]
sortDec [] = []
sortDec [x] = [x]
sortDec (x:y:xs)
    | x >= y = x : sortDec (y:xs)
    | otherwise = y : sortDec (x:xs)

playLowest :: Player -> Table -> IO (Player, Table)
playLowest player@(Player hand deck human) table =
    case hand of
        [] -> return (Player [] deck False, table)
        _ -> return (Player (tail hand') deck False, table ++ [head hand'])
    where
        hand' = sortAsc hand

playHighest :: Player -> Table -> IO (Player, Table)
playHighest player@(Player hand deck human) table =
    case hand of
        [] -> return (Player [] deck False, table)
        _ -> return (Player (tail hand') deck False, table ++ [head hand'])
    where
        hand' = sortDec hand

playBriscola :: Player -> Table -> Briscola -> IO (Player, Table)
playBriscola player@(Player hand deck human) table briscola
  = if hasBriscola player briscola
        then 
            let findBriscola [] _ = error "No briscola in hand"
                findBriscola (Card n s p : xs) briscola
                    | s == briscola = Card n s p
                    | otherwise = findBriscola xs briscola
            in do
                let hand' = findBriscola hand briscola : dropWhile ((/= briscola) . getSuit) (tail hand)
                return (Player (tail hand') deck False, table ++ [head hand'])
        else playHighest player table

playBriscola player@(Player hand deck human) table briscola
    = if hasBriscola player briscola
        then 
            let findBriscola [] _ = error "No briscola in hand"
                findBriscola (Card n s p : xs) briscola
                    | s == briscola = Card n s p
                    | otherwise = findBriscola xs briscola
            in do
                let hand' = findBriscola hand briscola : foldr (\x acc -> if x `elem` acc then acc else x : acc) [] (dropWhile ((/= briscola) . getSuit) (tail hand))
                return (Player (tail hand') deck False, table ++ [head hand'])
        else playHighest player table




doTurn :: Player -> Table -> Briscola -> IO (Player, Table)
doTurn player@(Player hand deck human) table briscola =
    case hand of
        [] -> return (Player [] deck False, table)
        _ -> if isSingleElement hand
            then return (Player [] deck False, table ++ [head hand])
            else if hasGreaterCard hand table
                then playBriscola player table briscola
                else playLowest player table