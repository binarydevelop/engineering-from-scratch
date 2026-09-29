var reverseList = function(head) {
    if (head === null) return null;

    let stack = [];
    let current = head;

    while (current !== null) {
        stack.push(current);
        current = current.next;
    }

    let newHead = stack.pop();
    current = newHead;

    while (stack.length > 0) {
        current.next = stack.pop();
        current = current.next;
    }

    current.next = null;

    return newHead;
};