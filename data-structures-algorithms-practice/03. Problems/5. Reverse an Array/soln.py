def soln(arr):
  n = len(arr)-1
  for i in range(len(arr)//2):
    temp = arr[i]
    arr[i] = arr[n-i] 
    arr[n-i] = temp
  return arr

arr = [1, 4, 3, 2, 6, 5]
print(soln(arr))

#another solution 
def _reverse(a, i, j):
    """Reverse subarray a[i..j] in-place."""
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1
    return arr

print(_reverse(arr))