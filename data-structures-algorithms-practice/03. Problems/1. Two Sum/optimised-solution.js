/* 

Here is a step-by-step breakdown of the solution:

Create a new empty hash table using the Map constructor: let map = new Map();
Iterate through the input array using a for loop: for (let i = 0; i < arr.length; i++) { ... }
For each element of the array, calculate its complement with respect to the target value: let compliment = target - arr[i];
Check if the complement is already in the hash table using the has method of the Map object: if (map.has(compliment)) { ... }
If the complement is in the hash table, return an array containing the indices of the two elements that add up to the target value: return [map.get(compliment), i];
If the complement is not in the hash table, add the current element and its index to the hash table using the set method of the Map object: map.set(arr[i], i);
If no two elements are found that add up to the target value, return an empty array: return [];
Overall, the time complexity of this algorithm is O(n), where n is the length of the input array, because each element of the array is processed only once, and the lookup and insertion operations on the hash table take constant time on average.
*/

var twoSum = function(arr, target) {
    let map = new Map();
    for(let i = 0; i< arr.length; i++){
      let compliment = target - arr[i];
      
      if(map.has(compliment)){
        return [map.get(compliment), i]
      } else {
        map.set(arr[i], i)
      }
    }
    return [];
  };
  
  