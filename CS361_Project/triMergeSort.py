import time
import random

def triMergeSort(arr):
    length = (len(arr))
    if length > 1:
        
        leftDivision = length//3
        rightDivision = (2*length)//3
        
        left = arr[:leftDivision]
        center = arr[leftDivision:rightDivision]
        right = arr[rightDivision:]
        
        triMergeSort(left)
        triMergeSort(center)
        triMergeSort(right)
        
        L = C = R = n = 0
        while L < len(left) and C < len(center) and R < len(right):
            if left[L] <= right[R] and left[L] <= center[C]:
                arr[n] = left[L]
                L += 1
            elif center[C] <= left[L] and center[C] <= right[R]:
                arr[n] = center[C]
                C += 1
            else:
                arr[n] = right[R]
                R += 1
            n += 1
        
        while L < len(left) and C < len(center):
            if left[L] <= center[C]:
                arr[n] = left[L]
                L += 1
            else:
                arr[n] = center[C]
                C += 1
            n += 1
            
        while L < len(left) and R < len(right):
            if left[L] <= right[R]:
                arr[n] = left[L]
                L += 1
            else:
                arr[n] = right[R]
                R += 1
            n += 1
            
        while C < len(center) and R < len(right):
            if center[C] <= right[R]:
                arr[n] = center[C]
                C += 1
            else:
                arr[n] = right[R]
                R += 1
            n += 1
        
        while L < len(left):
            arr[n] = left[L]
            L += 1
            n += 1
        
        while C < len(center):
            arr[n] = center[C]
            C += 1
            n += 1
        
        while R < len(right):
            arr[n] = right[R]
            R += 1
            n += 1
            
if __name__ == '__main__':
    n = 2**16
    arr = [random.randint(0, 99) for _ in range (n)]
    
    """
    print("original array is")
    for x in arr:
        print(x, end= " ")
    """
    
    timeStart = time.perf_counter()
    triMergeSort(arr)
    timeEnd = time.perf_counter()
    
    """
    print("\ntriMergeSorted array is ")
    for x in arr:
        print(x, end = " ")
    """
    
    timeDuration = timeEnd - timeStart
    print(f"\nTook {timeDuration:.3f} seconds")