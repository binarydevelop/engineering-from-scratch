## Backtracking

Backtracking is a problem-solving technique where we:

```txt
try one choice
explore it
undo the choice
try another choice
```

It is mostly used when we need to generate **all possible answers**.

---

# 1. Basic concept

Backtracking is like exploring a decision tree.

Example: generate all strings of length `2` using `"a"` and `"b"`.

Choices at each position:

```txt
position 1: choose a or b
position 2: choose a or b
```

Decision tree:

```txt
          ""
        /    \
      "a"    "b"
     /  \    /  \
   "aa" "ab" "ba" "bb"
```

Output:

```js
["aa", "ab", "ba", "bb"]
```

Backtracking means:

```txt
choose "a"
  choose "a" → "aa"
  undo "a"
  choose "b" → "ab"
undo "a"

choose "b"
  choose "a" → "ba"
  undo "a"
  choose "b" → "bb"
```

---

# 2. Real-life intuition

Imagine you are inside a maze.

At every point, you have choices:

```txt
go left
go right
go straight
```

You choose one path.

If it works, good.

If it does not work, you come back and try another path.

That is backtracking.

```txt
Try → Explore → Undo → Try next
```

---

# 3. Pattern recognition

Use backtracking when the problem says something like:

```txt
generate all
find all combinations
find all permutations
find all subsets
all valid ways
all possible paths
```

Common LeetCode patterns:

```txt
Generate Parentheses
Subsets
Permutations
Combination Sum
Word Search
N-Queens
Palindrome Partitioning
Sudoku Solver
```

The big clue is:

```txt
I need to try many possibilities and collect valid ones.
```

That usually means:

```txt
Backtracking
```

---

# 4. Backtracking template

This is the general pattern:

```js
function backtrack(path, choices) {
  // Base case:
  // If path is complete, save it.
  if (isComplete(path)) {
    result.push([...path]);
    return;
  }

  // Try every possible choice.
  for (const choice of choices) {
    // Skip invalid choices.
    if (!isValid(choice)) {
      continue;
    }

    // 1. Choose
    path.push(choice);

    // 2. Explore
    backtrack(path, choices);

    // 3. Undo the choice
    path.pop();
  }
}
```

The most important part is:

```js
path.push(choice);  // choose
backtrack(...);     // explore
path.pop();         // undo
```

That `pop()` is what makes it “backtracking.”

---

# 5. Why do we undo?

Suppose we are generating subsets from:

```js
[1, 2, 3]
```

If we choose `1`, then choose `2`, we get:

```js
[1, 2]
```

After exploring `[1, 2]`, we need to remove `2` so we can try:

```js
[1, 3]
```

If we do not undo, our path keeps old choices and becomes wrong.

So:

```js
path.pop();
```

means:

```txt
I am done exploring this choice.
Go back to the previous state.
```

---

# 6. Example 1: Subsets

Problem:

```js
nums = [1, 2, 3]
```

Generate all subsets:

```js
[
  [],
  [1],
  [1, 2],
  [1, 2, 3],
  [1, 3],
  [2],
  [2, 3],
  [3]
]
```

---

## Intuition

For each number, we have two choices:

```txt
include it
or
skip it
```

For `1`:

```txt
take 1
or skip 1
```

For `2`:

```txt
take 2
or skip 2
```

For `3`:

```txt
take 3
or skip 3
```

That is a decision tree.

---

## Code with comments

```js
function subsets(nums) {
  // This stores all final subsets.
  const result = [];

  // This stores the current subset we are building.
  const path = [];

  function backtrack(index) {
    // Every current path is a valid subset.
    // We copy it because path changes later.
    result.push([...path]);

    // Try adding every number starting from index.
    for (let i = index; i < nums.length; i++) {
      // Choose nums[i]
      path.push(nums[i]);

      // Explore further choices after i.
      backtrack(i + 1);

      // Undo the choice.
      // Remove nums[i] so we can try another option.
      path.pop();
    }
  }

  // Start from index 0.
  backtrack(0);

  return result;
}
```

---

## Dry run

Input:

```js
nums = [1, 2, 3]
```

Start:

```txt
path = []
result = [[]]
```

Choose `1`:

```txt
path = [1]
result includes [1]
```

Choose `2`:

```txt
path = [1, 2]
result includes [1, 2]
```

Choose `3`:

```txt
path = [1, 2, 3]
result includes [1, 2, 3]
```

Undo `3`:

```txt
path = [1, 2]
```

Undo `2`:

```txt
path = [1]
```

Choose `3`:

```txt
path = [1, 3]
result includes [1, 3]
```

Undo `3`, undo `1`, then try starting with `2`.

Final result contains all subsets.

---

# 7. Example 2: Generate Parentheses

This is LeetCode 22.

For:

```js
n = 3
```

We need all valid strings with:

```txt
3 opening brackets
3 closing brackets
```

---

## Pattern recognition

Problem says:

```txt
generate all valid combinations
```

That means:

```txt
Backtracking
```

Because we are building possible strings step by step.

---

## Intuition

At each step, we can add:

```txt
"("
or
")"
```

But we have rules:

```txt
Add "(" if open < n
Add ")" if close < open
```

Why?

```txt
open < n
```

means we still have opening brackets left.

```txt
close < open
```

means we only close if there is an unmatched opening bracket.

---

## Code with comments

```js
function generateParenthesis(n) {
  // Stores all valid answers.
  const result = [];

  function backtrack(current, open, close) {
    // Base case:
    // If the string has length 2 * n,
    // we used all parentheses.
    if (current.length === 2 * n) {
      result.push(current);
      return;
    }

    // Choice 1: Add "("
    // We can add "(" only if we still have some left.
    if (open < n) {
      backtrack(current + "(", open + 1, close);
    }

    // Choice 2: Add ")"
    // We can add ")" only if there is an unmatched "(".
    if (close < open) {
      backtrack(current + ")", open, close + 1);
    }
  }

  // Start with empty string and no brackets used.
  backtrack("", 0, 0);

  return result;
}
```

---

# 8. Example 3: Permutations

Problem:

```js
nums = [1, 2, 3]
```

Generate all orderings:

```js
[
  [1, 2, 3],
  [1, 3, 2],
  [2, 1, 3],
  [2, 3, 1],
  [3, 1, 2],
  [3, 2, 1]
]
```

---

## Pattern recognition

When you see:

```txt
all possible orderings
```

Think:

```txt
Permutations → Backtracking
```

---

## Intuition

At each position, choose a number that has not been used yet.

Example:

```txt
First position: choose 1, 2, or 3
Second position: choose from remaining numbers
Third position: choose last remaining number
```

---

## Code with comments

```js
function permute(nums) {
  // Stores all permutations.
  const result = [];

  // Current permutation being built.
  const path = [];

  // Tracks which numbers are already used.
  const used = new Set();

  function backtrack() {
    // Base case:
    // If path length equals nums length,
    // we built one full permutation.
    if (path.length === nums.length) {
      result.push([...path]);
      return;
    }

    // Try every number.
    for (const num of nums) {
      // If num is already used in current path, skip it.
      if (used.has(num)) {
        continue;
      }

      // Choose num.
      path.push(num);
      used.add(num);

      // Explore with this choice.
      backtrack();

      // Undo the choice.
      path.pop();
      used.delete(num);
    }
  }

  backtrack();

  return result;
}
```

---

# 9. The three key actions

Every backtracking problem has these three actions:

```js
// Choose
path.push(choice);

// Explore
backtrack(...);

// Undo
path.pop();
```

For permutations, because we also use a `Set`, we undo both:

```js
path.pop();
used.delete(num);
```

For board problems, undo means changing the board back.

Example:

```js
board[row][col] = "#";   // choose
backtrack(...);          // explore
board[row][col] = old;   // undo
```

---

# 10. Backtracking vs recursion

Backtracking uses recursion, but not all recursion is backtracking.

## Normal recursion

Usually solves one path.

Example:

```txt
reverse linked list recursively
```

## Backtracking

Explores many paths.

Example:

```txt
generate all subsets
generate all parentheses
generate all permutations
```

So:

```txt
Backtracking = recursion + choices + undo
```

---

# 11. How to identify the base case

Ask:

```txt
When is one answer complete?
```

Examples:

## Generate Parentheses

One answer is complete when:

```js
current.length === 2 * n
```

## Permutations

One answer is complete when:

```js
path.length === nums.length
```

## Combination Sum

One answer is complete when:

```js
sum === target
```

## Word Search

One answer is complete when:

```js
index === word.length
```

The base case is where we stop exploring and save/return.

---

# 12. How to identify choices

Ask:

```txt
What options can I try from this state?
```

Examples:

## Generate Parentheses

Choices:

```txt
add "("
add ")"
```

## Subsets

Choices:

```txt
include current number
skip current number
```

## Permutations

Choices:

```txt
choose any unused number
```

## Word Search

Choices:

```txt
move up
move down
move left
move right
```

---

# 13. How to identify constraints

Ask:

```txt
What choices are invalid?
```

Examples:

## Generate Parentheses

Invalid if:

```txt
close > open
open > n
```

## Permutations

Invalid if:

```txt
number already used
```

## Word Search

Invalid if:

```txt
out of bounds
already visited cell
wrong character
```

## Combination Sum

Invalid if:

```txt
sum > target
```

Constraints help us prune bad paths early.

---

# 14. Backtracking mental checklist

When solving a backtracking problem, ask:

```txt
1. What is my current path?
2. When is one answer complete?
3. What choices can I make?
4. Which choices are invalid?
5. How do I undo a choice?
```

For Generate Parentheses:

```txt
Path:
current string

Complete:
current.length === 2 * n

Choices:
add "(" or ")"

Invalid:
open > n
close > open

Undo:
not needed explicitly because strings are immutable
```

For Subsets:

```txt
Path:
current subset

Complete:
every path is valid

Choices:
choose next numbers

Invalid:
none, as long as we move index forward

Undo:
path.pop()
```

For Permutations:

```txt
Path:
current ordering

Complete:
path.length === nums.length

Choices:
any unused number

Invalid:
already used number

Undo:
path.pop()
used.delete(num)
```

---

# 15. Why sometimes we use `path.push/pop`, but sometimes `current + "("`

In JavaScript strings are immutable.

So this:

```js
backtrack(current + "(", open + 1, close);
```

creates a new string.

The old `current` is unchanged.

That means we do not need to manually undo.

But arrays are mutable.

So when we do:

```js
path.push(num);
```

we changed the same array.

Therefore we must undo:

```js
path.pop();
```

Important:

```txt
Strings: usually no explicit undo
Arrays/boards/Sets: usually need explicit undo
```

---

# 16. Time complexity

Backtracking time depends on how many possibilities we generate.

Examples:

## Subsets

For `n` numbers:

```txt
2^n subsets
```

Time:

```txt
O(n * 2^n)
```

because there are `2^n` subsets and copying each subset can take up to `n`.

## Permutations

For `n` numbers:

```txt
n! permutations
```

Time:

```txt
O(n * n!)
```

## Generate Parentheses

Number of valid answers is Catalan number.

You can say:

```txt
Time: O(Cn * n)
```

Where `Cn` is the nth Catalan number.

For interviews, saying:

```txt
We generate all valid combinations, so time depends on the number of valid outputs.
```

is often acceptable.

---

# Final memory trick

Backtracking means:

```txt
Try a choice.
Explore deeper.
Undo the choice.
Try another choice.
```

Core template:

```js
function backtrack(path) {
  if (done) {
    result.push(copyOfPath);
    return;
  }

  for (const choice of choices) {
    if (invalid(choice)) continue;

    makeChoice(choice);
    backtrack(path);
    undoChoice(choice);
  }
}
```

The most important phrase:

```txt
Backtracking = DFS over choices
```

You are walking through a decision tree, collecting valid answers.
