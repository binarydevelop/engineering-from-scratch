Why does this work?

The right side after the pivot is decreasing.

Example:

1 3 5 4 2
    -----
    decreasing suffix

A decreasing suffix is already the biggest possible order for those elements.

So to get the next permutation, we must increase the number just before it.

That number is the pivot.

Then we increase it by the smallest possible amount.

Then we make the suffix as small as possible.

That gives the next immediate permutation.