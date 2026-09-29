def soln(arr):
  largest = -1
  res = []
  for i in range(len(arr)-1, -1, -1):
    if arr[i] >= largest:
      res.append(arr[i])
      largest = arr[i]
    
  return res[::-1]
    
arr = []

print(soln(arr))

## Second solution
def soln(arr):
  leaders = []
  leaders.append(arr[len(arr)-1])
  for i in range(len(arr)-1, 0, -1):
    if arr[i] > arr[i-1]:
      leaders.append(arr[i])
    
  return list(reversed(leaders))


arr = [16, 17, 4, 3, 5, 2]
print(soln(arr))