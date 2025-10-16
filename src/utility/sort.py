def quicksort(arr, key):
    if len(arr) <= 1:
        return arr
    else:
        pivot = getattr(arr[len(arr) // 2], key)
        left = [x for x in arr if getattr(x, key) < pivot]
        middle = [x for x in arr if getattr(x, key) == pivot]
        right = [x for x in arr if getattr(x, key) > pivot]
        return quicksort(left, key) + middle + quicksort(right, key)