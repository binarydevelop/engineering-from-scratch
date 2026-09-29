Let’s trace **Word Search** with a very small board:

```javascript
board = [
  ["A", "B"],
  ["C", "D"]
];

word = "ABD";
```

The word exists:

```text
A -> B -> D
```

Coordinates:

```text
A = (0,0)
B = (0,1)
D = (1,1)
```

---

# Code With Line Numbers

Focus on this version:

```javascript
function exist(board, word) {
  const rows = board.length;
  const cols = board[0].length;

  function dfs(row, col, index) {
    // Line 1
    if (index === word.length) {
      return true;
    }

    // Line 2
    if (
      row < 0 ||
      row >= rows ||
      col < 0 ||
      col >= cols
    ) {
      return false;
    }

    // Line 3
    if (board[row][col] !== word[index]) {
      return false;
    }

    // Line 4
    const temp = board[row][col];

    // Line 5
    board[row][col] = "#";

    // Line 6
    const found =
      dfs(row + 1, col, index + 1) || // down
      dfs(row - 1, col, index + 1) || // up
      dfs(row, col + 1, index + 1) || // right
      dfs(row, col - 1, index + 1);   // left

    // Line 7
    board[row][col] = temp;

    // Line 8
    return found;
  }

  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      if (dfs(row, col, 0)) {
        return true;
      }
    }
  }

  return false;
}
```

Important: this line is the center of the recursion:

```javascript
const found =
  dfs(row + 1, col, index + 1) ||
  dfs(row - 1, col, index + 1) ||
  dfs(row, col + 1, index + 1) ||
  dfs(row, col - 1, index + 1);
```

JavaScript evaluates `||` from left to right.

So it tries:

```text
down -> up -> right -> left
```

And if one call returns `true`, JavaScript stops checking the rest.

This is called **short-circuiting**.

Does this make sense so far?

---

# Starting Point

We call:

```javascript
exist(board, "ABD")
```

The outer loop starts at `(0,0)`.

```text
board:
A B
C D
```

`board[0][0] = "A"`.

So we call:

```javascript
dfs(0, 0, 0)
```

Meaning:

```text
Can I match word[0] starting at cell (0,0)?
```

`word[0] = "A"`.

---

# Call Stack Trace

## Call 1: `dfs(0, 0, 0)`

Current call stack:

```text
dfs(0, 0, 0)
exist(...)
```

We are trying to match:

```text
word[0] = "A"
board[0][0] = "A"
```

Line 1:

```javascript
if (index === word.length)
```

`0 === 3` is false.

Line 2: bounds are okay.

Line 3:

```javascript
board[0][0] !== word[0]
```

`"A" !== "A"` is false, so we continue.

Line 4:

```javascript
const temp = board[0][0];
```

So:

```text
temp = "A"
```

Line 5:

```javascript
board[0][0] = "#";
```

Board becomes:

```text
# B
C D
```

Now Line 6 starts.

We need to match the next character:

```text
index + 1 = 1
word[1] = "B"
```

Line 6 first tries **down**:

```javascript
dfs(1, 0, 1)
```

Now `dfs(0,0,0)` pauses at Line 6 and waits for this call to return.

---

## Call 2: `dfs(1, 0, 1)`

Current call stack:

```text
dfs(1, 0, 1)
dfs(0, 0, 0)  paused at Line 6
exist(...)
```

We are trying to match:

```text
word[1] = "B"
board[1][0] = "C"
```

Line 1:

```text
1 === 3? false
```

Line 2: bounds okay.

Line 3:

```javascript
if (board[row][col] !== word[index])
```

Here:

```text
"C" !== "B"
```

That is true.

So this call returns:

```javascript
false
```

Call 2 is removed from the call stack.

Now we go back to Call 1.

---

## Back to Call 1: `dfs(0, 0, 0)`

We were here:

```javascript
const found =
  dfs(1, 0, 1) ||     // returned false
  dfs(-1, 0, 1) ||
  dfs(0, 1, 1) ||
  dfs(0, -1, 1);
```

Down returned `false`.

So JavaScript continues to the next direction: **up**.

It calls:

```javascript
dfs(-1, 0, 1)
```

---

## Call 3: `dfs(-1, 0, 1)`

Current call stack:

```text
dfs(-1, 0, 1)
dfs(0, 0, 0)  paused at Line 6
exist(...)
```

Line 1:

```text
1 === 3? false
```

Line 2 checks bounds:

```javascript
row < 0
```

Here:

```text
row = -1
```

So this is out of bounds.

Return:

```javascript
false
```

Call 3 is removed from the stack.

---

## Back to Call 1 Again

Now Line 6 has:

```javascript
const found =
  false ||      // down
  false ||      // up
  dfs(0, 1, 1) ||
  dfs(0, -1, 1);
```

Now JavaScript tries **right**:

```javascript
dfs(0, 1, 1)
```

---

## Call 4: `dfs(0, 1, 1)`

Current call stack:

```text
dfs(0, 1, 1)
dfs(0, 0, 0)  paused at Line 6
exist(...)
```

We are trying to match:

```text
word[1] = "B"
board[0][1] = "B"
```

Line 1:

```text
1 === 3? false
```

Line 2: bounds okay.

Line 3:

```text
"B" !== "B"? false
```

So match is good.

Line 4:

```javascript
const temp = board[0][1];
```

```text
temp = "B"
```

Line 5:

```javascript
board[0][1] = "#";
```

Board becomes:

```text
# #
C D
```

Now Line 6 starts.

We need to match:

```text
index + 1 = 2
word[2] = "D"
```

Try down first:

```javascript
dfs(1, 1, 2)
```

---

## Call 5: `dfs(1, 1, 2)`

Current call stack:

```text
dfs(1, 1, 2)
dfs(0, 1, 1)  paused at Line 6
dfs(0, 0, 0)  paused at Line 6
exist(...)
```

We are trying to match:

```text
word[2] = "D"
board[1][1] = "D"
```

Line 1:

```text
2 === 3? false
```

Line 2: bounds okay.

Line 3:

```text
"D" !== "D"? false
```

Good match.

Line 4:

```javascript
const temp = board[1][1];
```

```text
temp = "D"
```

Line 5:

```javascript
board[1][1] = "#";
```

Board becomes:

```text
# #
C #
```

Now Line 6 starts.

We need the next index:

```text
index + 1 = 3
```

Since `word.length = 3`, index `3` means:

```text
We already matched A, B, and D.
```

Line 6 first tries down:

```javascript
dfs(2, 1, 3)
```

---

## Call 6: `dfs(2, 1, 3)`

Current call stack:

```text
dfs(2, 1, 3)
dfs(1, 1, 2)  paused at Line 6
dfs(0, 1, 1)  paused at Line 6
dfs(0, 0, 0)  paused at Line 6
exist(...)
```

Line 1:

```javascript
if (index === word.length) {
  return true;
}
```

Here:

```text
index = 3
word.length = 3
```

So:

```javascript
return true;
```

Very important:

Even though `(2,1)` is out of bounds, Line 1 runs **before** bounds checking.

That is okay because reaching `index === word.length` means:

```text
The whole word has already been matched.
```

Call 6 returns:

```javascript
true
```

Now it is removed from the stack.

---

# Returning Back Up

Now we go back to Call 5.

## Back to Call 5: `dfs(1, 1, 2)`

It was waiting at Line 6:

```javascript
const found =
  dfs(2, 1, 3) ||   // returned true
  dfs(0, 1, 3) ||
  dfs(1, 2, 3) ||
  dfs(1, 0, 3);
```

Since the first call returned `true`, JavaScript does not call the other three directions.

So:

```javascript
found = true;
```

Now Line 7 executes:

```javascript
board[1][1] = temp;
```

It restores `"D"`.

Board becomes:

```text
# #
C D
```

Line 8:

```javascript
return found;
```

So Call 5 returns:

```javascript
true
```

Call 5 is removed from the stack.

---

## Back to Call 4: `dfs(0, 1, 1)`

Call 4 was waiting at Line 6:

```javascript
const found =
  dfs(1, 1, 2) ||   // returned true
  dfs(-1, 1, 2) ||
  dfs(0, 2, 2) ||
  dfs(0, 0, 2);
```

First direction returned `true`.

So:

```javascript
found = true;
```

The other directions are skipped.

Line 7 restores `"B"`:

```javascript
board[0][1] = temp;
```

Board becomes:

```text
# B
C D
```

Line 8:

```javascript
return found;
```

So Call 4 returns:

```javascript
true
```

Call 4 is removed from the stack.

---

## Back to Call 1: `dfs(0, 0, 0)`

Call 1 was waiting at Line 6:

```javascript
const found =
  dfs(1, 0, 1) ||   // false
  dfs(-1, 0, 1) ||  // false
  dfs(0, 1, 1) ||   // true
  dfs(0, -1, 1);
```

Since right returned `true`:

```javascript
found = true;
```

The left call is skipped.

Line 7 restores `"A"`:

```javascript
board[0][0] = temp;
```

Board becomes normal again:

```text
A B
C D
```

Line 8:

```javascript
return found;
```

So Call 1 returns:

```javascript
true
```

Call 1 is removed from the stack.

---

## Back to `exist`

We were inside:

```javascript
if (dfs(row, col, 0)) {
  return true;
}
```

`dfs(0,0,0)` returned `true`.

So:

```javascript
return true;
```

The whole function ends.

Final answer:

```javascript
true
```

---

# Full Clean Call Stack Summary

Here is the whole story in one clean trace:

```text
exist(board, "ABD")
  calls dfs(0,0,0)  // looking for "A"
  
    dfs(0,0,0)
      matches "A"
      marks A as "#"
      tries down: dfs(1,0,1)  // looking for "B"
      
        dfs(1,0,1)
          board[1][0] = "C", needed "B"
          returns false
      
      tries up: dfs(-1,0,1)
      
        dfs(-1,0,1)
          out of bounds
          returns false
      
      tries right: dfs(0,1,1)  // looking for "B"
      
        dfs(0,1,1)
          matches "B"
          marks B as "#"
          tries down: dfs(1,1,2)  // looking for "D"
          
            dfs(1,1,2)
              matches "D"
              marks D as "#"
              tries down: dfs(2,1,3)
              
                dfs(2,1,3)
                  index === word.length
                  returns true
              
              found = true
              restores D
              returns true
          
          found = true
          restores B
          returns true
      
      found = true
      restores A
      returns true
  
  dfs returned true
  exist returns true
```

---

# The Most Important Execution Rule

When JavaScript hits this:

```javascript
const found =
  dfs(row + 1, col, index + 1) ||
  dfs(row - 1, col, index + 1) ||
  dfs(row, col + 1, index + 1) ||
  dfs(row, col - 1, index + 1);
```

It does **not** run all four at once.

It runs them one by one.

Like this:

```text
1. Call down.
2. If down returns true, stop.
3. If down returns false, call up.
4. If up returns false, call right.
5. If right returns true, stop.
6. If right returns false, call left.
```

So a parent `dfs` call is basically asking:

```text
Can any of my neighbors complete the rest of the word?
```

If any neighbor says `true`, parent says `true`.

If all neighbors say `false`, parent says `false`.

---

# Why Restore Happens Even When We Found the Word

This is subtle but important.

In our code, we do:

```javascript
const found = dfs(...) || dfs(...) || dfs(...) || dfs(...);

board[row][col] = temp;

return found;
```

So even if `found` is `true`, we still restore the board before returning.

That is good practice because it leaves the board unchanged.

Example:

```text
A was changed to "#"
B was changed to "#"
D was changed to "#"
```

As returns happen:

```text
D restores itself
B restores itself
A restores itself
```

Then the board is back to normal.

---

# Tiny Mental Model

Every `dfs(row, col, index)` means:

```text
Can I match word[index...] starting from this cell?
```

It returns:

```text
true  -> yes, this path can complete the word
false -> no, this path fails
```

Parent calls wait for child calls.

When a child returns, the parent continues exactly where it paused.

That is how everything works together.

---

Does this call-stack flow make sense now?
