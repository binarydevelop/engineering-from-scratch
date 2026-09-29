def soln(arr):
  largest = -1
  second_largest = -1
  for elem in arr:
    if elem > largest:
      second_largest = largest
      largest = elem
    elif elem < largest and elem > second_largest:
      second_largest = elem
  return second_largest
    
arr = [12, 35, 1, 10, 34, 1]

print(soln(arr))

