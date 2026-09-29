This technique is usually called **negative marking** or **index marking**.

It is also part of a broader idea called **using the array itself as a hash table**.

The key idea is:

```js id="9ksjbf"
value -> index
```

For an array containing numbers from `1` to `n`, each number can point to an index:

```js id="g1xmk3"
number 1 -> index 0
number 2 -> index 1
number 3 -> index 2
...
number n -> index n - 1
```

So when you see a number, you mark its corresponding index as visited by making it negative.

Example:

```js id="7k7v4i"
nums = [1, 2, 2, 4]
```

When you see `1`, mark index `0` negative:

```js id="czzm95"
[-1, 2, 2, 4]
```

When you see `2`, mark index `1` negative:

```js id="v4nq1e"
[-1, -2, 2, 4]
```

When you see `2` again, index `1` is already negative, so `2` is the duplicate.

At the end:

```js id="kfb5em"
[-1, -2, 2, -4]
```

Index `2` is still positive, so number `3` was missing.

So the answer is:

```js id="xnsw7g"
[2, 3]
```

This technique is generally used when:

```js id="ffki2f"
1. Array values are in a fixed range, usually 1 to n
2. You need to detect missing numbers, duplicates, or visited values
3. You want O(1) extra space
4. You are allowed to modify the input array
```

Common problems where this appears:

```js id="h2fh0o"
Find All Numbers Disappeared in an Array
Find All Duplicates in an Array
Set Mismatch
First Missing Positive
Find the Duplicate Number
```

The pattern looks like this:

```js id="5z2zgd"
for (let i = 0; i < nums.length; i++) {
    let index = Math.abs(nums[i]) - 1;

    if (nums[index] < 0) {
        // already seen this number
    } else {
        nums[index] *= -1;
    }
}
```

Important warning: use `Math.abs(nums[i])` because the number may already have been made negative earlier.

Use this when the problem says something like:

```js id="syzobt"
nums contains numbers from 1 to n
```

or:

```js id="078gl2"
nums has length n and values are in the range [1, n]
```

That is your signal that values can be mapped directly to indices.
