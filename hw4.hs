-- Problem 1 

data Tree a = LeafT a | NodeT (Tree a) (Tree a) deriving (Show, Eq)

balance :: [a] -> Tree a
balance [] = error "empty list"
balance [x] = LeafT x
balance ls@(x:xs) = NodeT (balance left) (balance right)
    where
        half = length ls `div` 2
        left = take half ls
        right = drop half ls



-- Problem 2

data T = Leaf | Node T T deriving (Eq, Show)

data P = GoLeft P | GoRight P | This deriving (Eq, Show)

allpaths :: T -> [P]
allpaths Leaf = [This]
allpaths (Node left right) = [This] ++ (map GoLeft (allpaths left)) ++ (map GoRight (allpaths right))


example2 :: T
example2 = Node Leaf (Node Leaf Leaf)

example3 :: T
example3 = Node (Node Leaf Leaf) (Node Leaf (Node Leaf Leaf))

-- Problem 3

data Expr = Val Int | Add Expr Expr
    deriving (Eq, Show)

folde :: (Int -> a) -> (a -> a -> a) -> Expr -> a
folde f g (Val x) = f x
folde f g (Add e1 e2) = g (folde f g e1) (folde f g e2)

eval :: Expr -> Int
eval = folde id (+)

exprExample1 :: Expr
exprExample1 = Add (Val 1) (Val 2)

exprExample2 :: Expr
exprExample2 = Add (Add (Val 1) (Val 2)) (Val 3)

-- Problem 4

myTakeWhile :: (a -> Bool) -> [a] -> [a]
myTakeWhile _ [] = []
myTakeWhile pred (x:xs)
    | pred x = x : myTakeWhile pred xs
    | otherwise = []

-- Problem 5

myDropWhile :: (a -> Bool) -> [a] -> [a]
myDropWhile _ [] = []
myDropWhile pred (x:xs)
    | pred x = myDropWhile pred xs
    | otherwise = x:xs

mySpan :: (a -> Bool) -> [a] -> ([a], [a])
mySpan _ [] = ([], [])
mySpan pred ls = (myTakeWhile pred ls, myDropWhile pred ls)

-- Problem 6

combinations3 :: Ord a => [a] -> [[a]]
combinations3 [] = []
combinations3 (x:xs) = [x:y:z:[] | y <- xs, z <- xs, y/=z] ++ combinations3 xs

-- Problem 7

increasing :: Ord a => [a] -> Bool
increasing xs = and [x <= y | (x,y) <- zip xs (tail xs)]

-- Problem 8

combinations :: (Ord a, Integral b) => b -> [a] -> [[a]]
combinations 0 _ = [[]]
combinations _ [] = []
combinations n (x:xs) = [x:y | y <- combinations (n-1) xs] ++ combinations n xs

-- Problem 9

data Complex = Complex { real :: Integer, imaginary :: Integer }

instance Eq Complex where
    (Complex x xi) == (Complex y yi) = x == y && xi == yi

instance Show Complex where
    show (Complex x xi) = show x ++ "+" ++ show xi ++ "i"

instance Num Complex where
    (Complex x xi) + (Complex y yi) = Complex (x+y) (xi+yi)
    (Complex x xi) - (Complex y yi) = Complex (x-y) (xi-yi)
    (Complex x xi) * (Complex y yi) = Complex (x*y - xi*yi) (x*yi + xi*y)
    abs (Complex x xi) = Complex (abs x) (abs xi)
    signum (Complex x xi) = Complex (signum x) (signum xi)
    fromInteger x = Complex (fromInteger x) (0)