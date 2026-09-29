def soln(arr):
  largest = -1
  for i in range(len(arr)):
    if arr[i] > largest:
      largest = arr[i]
      
  return largest
  


arr = [1,45,2,5,23,2,5233,3,3456]
print(soln(arr))