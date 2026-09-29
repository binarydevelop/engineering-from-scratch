def _reverse(a, i, j):
    """Reverse subarray a[i..j] in-place."""
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1

def left_rotate(a, d):
    """
    Left-rotate list a by d positions in-place.
    Example: [1,2,3,4,5], d=2 -> [3,4,5,1,2]
    """
    n = len(a)
    if n <= 1:
        return
    d %= n
    if d == 0:
        return
    _reverse(a, 0, d - 1)
    _reverse(a, d, n - 1)
    _reverse(a, 0, n - 1)

def right_rotate(a, d):
    """
    Right-rotate list a by d positions in-place.
    Example: [1,2,3,4,5], d=2 -> [4,5,1,2,3]
    """
    n = len(a)
    if n <= 1:
        return
    d %= n
    if d == 0:
        return
    # right rotate by d == left rotate by n-d
    left_rotate(a, n - d)

# Quick tests
if __name__ == "__main__":
    arr = [1,2,3,4,5,6,7]
    left_rotate(arr, 2)
    print("left by 2:", arr)        # [3,4,5,6,7,1,2]

    arr = [1,2,3,4,5,6,7]
    right_rotate(arr, 2)
    print("right by 2:", arr)       # [6,7,1,2,3,4,5]

    # edge cases
    a = []
    left_rotate(a, 3); print("empty:", a)
    a = [1]
    left_rotate(a, 10); print("single:", a)
    a = [1,2,3]
    left_rotate(a, -1)  # negative => rotate right by 1
    print("neg d (left -1):", a)     # [3,1,2]
