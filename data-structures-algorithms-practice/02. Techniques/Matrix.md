Yes — these are **matrix coordinate properties**, and they are very useful in DSA problems.

Think of every matrix cell as:

```js
matrix[i][j]
```

Where:

```txt
i = row
j = column
```

Once you understand how `i` and `j` behave, many matrix problems become pattern-based.

---

## 1. Same row

Cells in the same row have the same `i`.

```txt
[0,0] [0,1] [0,2] [0,3]
```

All have:

```js
i = 0
```

Useful for row traversal:

```js
for (let j = 0; j < cols; j++) {
    console.log(matrix[i][j]);
}
```

---

## 2. Same column

Cells in the same column have the same `j`.

```txt
[0,2]
[1,2]
[2,2]
[3,2]
```

All have:

```js
j = 2
```

Useful for column traversal:

```js
for (let i = 0; i < rows; i++) {
    console.log(matrix[i][j]);
}
```

---

## 3. Main diagonal

Top-left to bottom-right diagonal:

```txt
[0,0], [1,1], [2,2], [3,3]
```

Property:

```js
i === j
```

Example:

```js
matrix[0][0]
matrix[1][1]
matrix[2][2]
```

Useful in square matrix problems.

---

## 4. Anti-diagonal

Top-right to bottom-left diagonal:

```txt
[0,3], [1,2], [2,1], [3,0]
```

For an `n x n` matrix:

```js
i + j === n - 1
```

Example in a `4 x 4` matrix:

```js
0 + 3 = 3
1 + 2 = 3
2 + 1 = 3
3 + 0 = 3
```

So:

```js
i + j === n - 1
```

---

## 5. All top-left to bottom-right diagonals

These are the diagonals used in your `diagonalSort` problem.

Property:

```js
i - j
```

Same diagonal means same `i - j`.

```txt
[0,0], [1,1], [2,2] => i - j = 0

[0,1], [1,2], [2,3] => i - j = -1

[1,0], [2,1], [3,2] => i - j = 1
```

Useful for:

```js
let key = i - j;
```

---

## 6. All top-right to bottom-left diagonals

Property:

```js
i + j
```

Same diagonal means same `i + j`.

```txt
[0,2], [1,1], [2,0] => i + j = 2
```

Useful for anti-diagonal grouping:

```js
let key = i + j;
```

---

## 7. Moving in 4 directions

Very common in BFS/DFS matrix problems.

From cell:

```js
matrix[i][j]
```

You can move:

```txt
up    -> i - 1, j
down  -> i + 1, j
left  -> i, j - 1
right -> i, j + 1
```

Code pattern:

```js
let directions = [
    [-1, 0], // up
    [1, 0],  // down
    [0, -1], // left
    [0, 1]   // right
];

for (let [dr, dc] of directions) {
    let newRow = i + dr;
    let newCol = j + dc;
}
```

Useful in problems like:

```txt
Number of Islands
Flood Fill
Rotting Oranges
Shortest Path in Grid
Surrounded Regions
```

---

## 8. Moving in 8 directions

Includes diagonals too.

```js
let directions = [
    [-1, 0],
    [1, 0],
    [0, -1],
    [0, 1],
    [-1, -1],
    [-1, 1],
    [1, -1],
    [1, 1]
];
```

Useful for:

```txt
Word Search
Minesweeper
Knight-like grid variations
Island problems with diagonal connections
```

---

## 9. Boundary check

Any time you move in a matrix, always check whether the new cell is valid.

```js
if (
    newRow >= 0 &&
    newRow < rows &&
    newCol >= 0 &&
    newCol < cols
) {
    // valid cell
}
```

This is one of the most important matrix habits.

You can make a helper:

```js
function isValid(r, c, rows, cols) {
    return r >= 0 && r < rows && c >= 0 && c < cols;
}
```

---

## 10. Flattening 2D index to 1D

Sometimes a matrix is treated like a 1D array.

Formula:

```js
index = i * cols + j;
```

Example:

```txt
matrix:
[ [1, 2, 3],
  [4, 5, 6] ]
```

Positions:

```txt
[0][0] -> 0 * 3 + 0 = 0
[0][1] -> 0 * 3 + 1 = 1
[0][2] -> 0 * 3 + 2 = 2
[1][0] -> 1 * 3 + 0 = 3
[1][1] -> 1 * 3 + 1 = 4
[1][2] -> 1 * 3 + 2 = 5
```

Useful in binary search on matrix.

---

## 11. Convert 1D index back to 2D

Opposite of flattening:

```js
i = Math.floor(index / cols);
j = index % cols;
```

Example:

```js
let index = 4;
let cols = 3;

let i = Math.floor(index / cols); // 1
let j = index % cols;             // 1
```

So index `4` means:

```js
matrix[1][1]
```

Very useful for LeetCode:

```txt
Search a 2D Matrix
```

---

## 12. Transpose of matrix

Transpose means swap rows and columns.

Property:

```js
matrix[i][j] becomes matrix[j][i]
```

Example:

```txt
Original:
1 2 3
4 5 6

Transpose:
1 4
2 5
3 6
```

For square matrix:

```js
for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
        [matrix[i][j], matrix[j][i]] = [matrix[j][i], matrix[i][j]];
    }
}
```

---

## 13. Rotate matrix 90 degrees clockwise

Common trick:

```txt
Transpose + reverse each row
```

Example:

```txt
1 2 3
4 5 6
7 8 9
```

Transpose:

```txt
1 4 7
2 5 8
3 6 9
```

Reverse each row:

```txt
7 4 1
8 5 2
9 6 3
```

Code:

```js
function rotate(matrix) {
    let n = matrix.length;

    // transpose
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            [matrix[i][j], matrix[j][i]] = [matrix[j][i], matrix[i][j]];
        }
    }

    // reverse each row
    for (let row of matrix) {
        row.reverse();
    }
}
```

---

## 14. Spiral traversal

Use four boundaries:

```js
let top = 0;
let bottom = rows - 1;
let left = 0;
let right = cols - 1;
```

Then move:

```txt
left → right
top → bottom
right → left
bottom → top
```

After each direction, shrink one boundary.

Useful for:

```txt
Spiral Matrix
Spiral Matrix II
```

---

## 15. Layer/ring concept

A matrix can be seen as layers.

Example:

```txt
1  2  3  4
5  6  7  8
9 10 11 12
13 14 15 16
```

Outer layer:

```txt
1 2 3 4 8 12 16 15 14 13 9 5
```

Inner layer:

```txt
6 7 11 10
```

Useful for:

```txt
Rotate Image
Spiral Matrix
Matrix ring rotation
```

Layer number can be thought of as:

```js
layer = Math.min(i, j, rows - 1 - i, cols - 1 - j);
```

---

## 16. Prefix sum in matrix

Used when you need fast submatrix sum.

A 2D prefix sum stores sum from `[0][0]` to `[i][j]`.

Formula:

```js
prefix[i][j] =
    matrix[i][j]
    + prefix[i - 1][j]
    + prefix[i][j - 1]
    - prefix[i - 1][j - 1]
```

Why subtract?

Because the top-left area gets counted twice.

Useful for:

```txt
Range Sum Query 2D
Maximum sum rectangle
Submatrix sum problems
```

---

## 17. Sorted matrix trick

If matrix rows and columns are sorted:

```txt
1  4  7
2  5  8
3  6  9
```

Start from top-right:

```js
let i = 0;
let j = cols - 1;
```

Then:

```js
if (matrix[i][j] === target) found
else if (matrix[i][j] > target) j--
else i++
```

Why?

From top-right:

```txt
moving left  -> smaller
moving down  -> larger
```

Useful for:

```txt
Search a 2D Matrix II
```

---

## 18. Marking visited cells

For DFS/BFS, you often need:

```js
let visited = Array.from({ length: rows }, () =>
    Array(cols).fill(false)
);
```

Then:

```js
visited[i][j] = true;
```

Or mutate the matrix directly:

```js
matrix[i][j] = "#";
```

This is common in island/grid problems.

---

## 19. Row and column marking

In problems like:

```txt
Set Matrix Zeroes
```

If one cell is zero, mark its whole row and column.

Simple version:

```js
let zeroRows = new Set();
let zeroCols = new Set();

for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
        if (matrix[i][j] === 0) {
            zeroRows.add(i);
            zeroCols.add(j);
        }
    }
}
```

Then:

```js
if (zeroRows.has(i) || zeroCols.has(j)) {
    matrix[i][j] = 0;
}
```

---

## 20. Common coordinate formulas

Here is the cheat sheet:

```txt
Same row:                    i is same
Same column:                 j is same

Main diagonal:               i === j
Anti-diagonal:               i + j === n - 1

Top-left to bottom-right:    i - j is same
Top-right to bottom-left:    i + j is same

Move up:                     i - 1, j
Move down:                   i + 1, j
Move left:                   i, j - 1
Move right:                  i, j + 1

Flatten 2D to 1D:            i * cols + j
Convert 1D to 2D row:        Math.floor(index / cols)
Convert 1D to 2D col:        index % cols

Transpose:                   matrix[i][j] ↔ matrix[j][i]

Anti-diagonal in n x n:      i + j === n - 1
```

---

The best way to think in matrix questions is:

```txt
What does this problem care about?

Rows?        Use i
Columns?     Use j
Main diagonal? i === j
All diagonals one way? i - j
All diagonals other way? i + j
Neighbors?   Use direction arrays
Submatrix?   Use boundaries or prefix sum
Sorted matrix? Start from top-right or use binary search
```

Once you recognize which pattern the problem is asking for, the code becomes much easier.
