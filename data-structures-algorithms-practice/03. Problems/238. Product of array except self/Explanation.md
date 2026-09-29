## Optimized Approach: Use the answer array itself

We want:

```python
answer[i] = product of everything before i * product of everything after i
```

Instead of making two extra arrays:

```python
prefix = [...]
suffix = [...]
```

we store the **left product** directly inside `answer`.

Then we come back from the right side and multiply the **right product** into it.

---

# Code

```python
def productExceptSelf(nums):
    n = len(nums)
    answer = [1] * n

    left_product = 1

    for i in range(n):
        answer[i] = left_product
        left_product *= nums[i]

    right_product = 1

    for i in range(n - 1, -1, -1):
        answer[i] *= right_product
        right_product *= nums[i]

    return answer
```

---

# Think of it in two passes

Example:

```python
nums = [1, 2, 3, 4]
```

We need:

```python
answer = [24, 12, 8, 6]
```

---

# Pass 1: Store product of everything on the left

We start with:

```python
answer = [1, 1, 1, 1]
left_product = 1
```

Why is `left_product = 1`?

Because before the first element, there is nothing. Product of nothing is treated as `1`.

Now move left to right.

| index | nums[i] | left_product before | answer[i] becomes | left_product after |
| ----- | ------: | ------------------: | ----------------: | -----------------: |
| 0     |       1 |                   1 |                 1 |                  1 |
| 1     |       2 |                   1 |                 1 |                  2 |
| 2     |       3 |                   2 |                 2 |                  6 |
| 3     |       4 |                   6 |                 6 |                 24 |

After first pass:

```python
answer = [1, 1, 2, 6]
```

This means:

```text
answer[0] = product of numbers before index 0 = 1
answer[1] = product of numbers before index 1 = 1
answer[2] = product of numbers before index 2 = 1 * 2 = 2
answer[3] = product of numbers before index 3 = 1 * 2 * 3 = 6
```

So after pass 1, `answer` only knows the **left side product**.

It does not know the right side yet.

---

# Pass 2: Multiply product of everything on the right

Now we go from right to left.

Start:

```python
right_product = 1
```

Why `1`?

Because after the last element, there is nothing. Product of nothing is `1`.

Current answer:

```python
answer = [1, 1, 2, 6]
```

Now move right to left.

| index | nums[i] | answer[i] before | right_product before | answer[i] after | right_product after |
| ----- | ------: | ---------------: | -------------------: | --------------: | ------------------: |
| 3     |       4 |                6 |                    1 |               6 |                   4 |
| 2     |       3 |                2 |                    4 |               8 |                  12 |
| 1     |       2 |                1 |                   12 |              12 |                  24 |
| 0     |       1 |                1 |                   24 |              24 |                  24 |

Final:

```python
answer = [24, 12, 8, 6]
```

---

# What exactly is happening?

At every index:

```python
answer[i] already has product of everything on the left
```

Then in the second pass:

```python
right_product has product of everything on the right
```

So we do:

```python
answer[i] = answer[i] * right_product
```

Which means:

```python
answer[i] = left product * right product
```

That is exactly what we need.

---

# Look at index 2 carefully

```python
nums = [1, 2, 3, 4]
```

At index `2`, the number is `3`.

We want product of everything except `3`:

```python
1 * 2 * 4 = 8
```

After first pass:

```python
answer[2] = 2
```

That means product of everything before index `2`:

```python
1 * 2 = 2
```

During second pass, when we reach index `2`:

```python
right_product = 4
```

That means product of everything after index `2`:

```python
4
```

Now:

```python
answer[2] = 2 * 4 = 8
```

Done.

---

# Why do we update product after using it?

This part is very important:

```python
answer[i] = left_product
left_product *= nums[i]
```

We first put `left_product` into `answer[i]`, then update it.

Why?

Because `answer[i]` should not include `nums[i]`.

For example, at index `2`, number is `3`.

The left product should be:

```python
1 * 2
```

It should not be:

```python
1 * 2 * 3
```

So we use `left_product` first, then multiply by current number for the next index.

Same idea on the right side:

```python
answer[i] *= right_product
right_product *= nums[i]
```

We use `right_product` first because it should not include `nums[i]`.

Then we update it for the next index on the left.

---

# Pattern

This is the key pattern:

## Prefix from left + suffix from right

Use this when:

```text
Each index needs information from the left side and the right side.
```

Here:

```text
left side product * right side product
```

The optimization trick is:

```text
Use the output array to store prefix values,
then use one variable to track suffix values.
```

---

# Complexity

### Time Complexity

```text
O(n)
```

Because we only loop twice:

```text
one pass from left to right
one pass from right to left
```

### Space Complexity

```text
O(1) extra space
```

We only use:

```python
left_product
right_product
```

The `answer` array is not counted as extra space because we have to return it anyway.

---

# One-line memory trick

Think:

```text
First pass fills left products.
Second pass multiplies right products.
```

That is the whole optimized solution.
