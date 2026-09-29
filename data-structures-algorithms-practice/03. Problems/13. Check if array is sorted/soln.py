def soln(arr):
  # why only till 0 because at index 1 we will check if the element at 0 is greater than the one at index 1 
  for i in range(len(arr)-1, 0, -1): 
    if not arr[i] > arr[i-1]:
      return False
    
  return True
    
    
arr = [2,3,5,8, 17, 18, -1]

print(soln(arr))
