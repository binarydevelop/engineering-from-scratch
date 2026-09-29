/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
var maxFrequency = function(nums, k) {
        nums.sort((a,b) => a - b)

    let left = 0;
    let currentSum = 0;
    let maxFrequency = 0; 

    for(let right = 0; right < nums.length; right++){
        currentSum += nums[right];

        while(((right - left + 1) * nums[right] - currentSum) > k){
            currentSum -= nums[left];
            left++; 
        }

        let frequency = right - left + 1
        maxFrequency = Math.max(frequency, maxFrequency)
    }

    return maxFrequency
};



/*
The maximum possible frequency of the most frequent element after performing at most $k$ operations is found using a Sorting + Sliding Window (Two Pointer) approach.
## 1. Problem Overview
To maximize the frequency of an element, you must increase smaller elements to match a target element. By sorting the array, the elements you change will always be contiguous and directly to the left of your target element. [1, 2] 
## 2. Formulating the Condition
Let the current sliding window range from index $L$ to $R$. The target value we want to change all elements in the window to is $nums[R]$.

* 
* The total sum of the window after changing all elements would be: $\text{window\_length} \times nums[R]$
* The current actual sum of elements in the window is: $\text{current\_sum}$
* The operations needed to achieve this is: $(\text{window\_length} \times nums[R]) - \text{current\_sum}$
* 

The window is valid as long as the operations needed do not exceed $k$:
$$(R - L + 1) \times nums[R] - \text{current\_sum} \le k$$ 
## 3. Step-by-Step Algorithm

   1. Sort the Array: Arrange the elements in ascending order.
   2. Initialize Pointers: Set the left pointer $L = 0$ and the tracking variable $\text{current\_sum} = 0$.
   3. Expand the Window: Loop through the array with a right pointer $R$ from $0$ to $n-1$.
   4. Add Current Element: Add $nums[R]$ to $\text{current\_sum}$.
   5. Shrink if Invalid: If the operations condition is violated, subtract $nums[L]$ from $\text{current\_sum}$ and increment $L$.
   6. Track Maximum: The maximum window size achieved during the iteration is your final answer.

## 4. Code Implementation (Python)

def maxFrequency(nums: list[int], k: int) -> int:
    # Step 1: Sort the array
    nums.sort()
    
    L = 0
    current_sum = 0
    max_freq = 0
    
    # Step 3: Expand the window using right pointer R
    for R in range(len(nums)):
        current_sum += nums[R]
        
        # Step 5: Shrink window from the left if it requires more than k operations
        while (R - L + 1) * nums[R] - current_sum > k:
            current_sum -= nums[L]
            L += 1
            
        # Step 6: Update the maximum frequency found
        max_freq = max(max_freq, R - L + 1)
        
    return max_freq

## 5. Complexity Analysis

* 
* Time Complexity: $\mathcal{O}(n \log n)$ due to the initial sorting step. The sliding window phase takes $\mathcal{O}(n)$ time because both $L$ and $R$ traverse the array at most once.
* Space Complexity: $\mathcal{O}(1)$ or $\mathcal{O}(n)$ depending on the space required by the sorting algorithm implementation in the chosen programming language.
* 

If you want, I can:

* 
* Provide the solution in Java, C++, or JavaScript
* Explain the optimized space-optimized prefix sum variant
* Walk through a dry run with a specific example array
* 

Let me know how you would like to proceed.

[1] [https://algo.monster](https://algo.monster/liteproblems/1838)
[2] [https://neetcode.io](https://neetcode.io/solutions/frequency-of-the-most-frequent-element)

*/