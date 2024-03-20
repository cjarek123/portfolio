import random
import time

def quadHeapify(arr, length, root):
    largest = root
    first = 4 * root + 1
    second = 4 * root + 2
    third = 4 * root + 3
    fourth = 4 * root + 4
    
    if first < length and arr[largest] < arr[first]:
        largest = first
    if second < length and arr[largest] < arr[second]:
        largest = second    
    if third < length and arr[largest] < arr[third]:
        largest = third
    if fourth < length and arr[largest] < arr[fourth]:
        largest = fourth
        
    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        
        quadHeapify(arr, length, largest)
        

def quadHeapSort(arr):
    length = len(arr)
    
    for i in range(length//4 -1, -1, -1):
        quadHeapify(arr, length, i)
    
    for i in range(length-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        quadHeapify(arr, i, 0)
        
if __name__ == '__main__':
    n = 2**16
    arr = [random.randint(0, 99) for _ in range (n)]
    
    """
    print("original array is")
    for x in arr:
        print(x, end= " ")
    """
    timeStart = time.perf_counter()
    quadHeapSort(arr)
    timeEnd = time.perf_counter()
    """
    print("\nquadHeapSorted array is")
    for x in arr:
        print(x, end= " ")
    """
    timeDuration = timeEnd - timeStart
    print(f"\nTook {timeDuration:.3f} seconds")