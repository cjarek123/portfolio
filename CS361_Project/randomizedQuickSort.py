import time
import random

def randomPartition(array, low, high):
    pivot = random.randint(low, high)
    i = low - 1
    
    for j in range(low, high):
        if array[j] <= array[high]:
            i = i + 1
            array[i], array[j] = array[j], array[i]
    
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1


def randomizedQuicksort(array, low, high):
    if low < high:
        p = randomPartition(array, low, high)
        randomizedQuicksort(array, low, p - 1)
        randomizedQuicksort(array, p + 1, high)
        
if __name__ == '__main__':
    n = 2**16
    arr = [random.randint(0, 99) for _ in range (n)]

    """
    print("original array is")
    for x in arr:
        print(x, end= " ")
    """
    
    timeStart = time.perf_counter()
    randomizedQuicksort(arr, 0, len(arr) - 1)
    timeEnd = time.perf_counter()
    
    """
    print("\nrandomizedQuickSorted array is ")
    for x in arr:
        print(x, end = " ")
    """
    timeDuration = timeEnd - timeStart
    print(f"\nTook {timeDuration:.3f} seconds") 