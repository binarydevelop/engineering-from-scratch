Without the checks, you can accidentally visit the same row or column twice after the boundaries move inward.

Example: **single row**

```js
let matrix = [[1, 2, 3]];
```

Initial boundaries:

```js
top = 0
bottom = 0
left = 0
right = 2
```

First loop: traverse top row:

```js
[1, 2, 3]
```

Then:

```js
top++
top = 1
```

Now `top > bottom`, so there is no bottom row left.

Without this check:

```js
if (top <= bottom) {
    for (let col = right; col >= left; col--) {
        results.push(matrix[bottom][col]);
    }
    bottom--;
}
```

You would traverse the same row again backward:

```js
[1, 2, 3, 2, 1]
```

That is wrong.

So the check prevents duplicate traversal:

```js
if (top <= bottom) {
    for (let col = right; col >= left; col--) {
        results.push(matrix[bottom][col]);
    }
    bottom--;
}
```

---

Example: **single column**

```js
let matrix = [
  [1],
  [2],
  [3]
];
```

Correct spiral output should be:

```js
[1, 2, 3]
```

After traversing the top row and right column, the column boundaries may cross:

```js
right--
```

Now there may be no left column left to traverse.

So we use:

```js
if (left <= right) {
    for (let row = bottom; row >= top; row--) {
        results.push(matrix[row][left]);
    }
    left++;
}
```

Without this check, you might revisit the same column and get duplicates like:

```js
[1, 2, 3, 2]
```

The checks make sure each remaining row or column still exists before visiting it.
