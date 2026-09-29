function reverseList(head) {
  if (head === null || head.next === null) {
    return head;
  }

  const newHead = reverseList(head.next);

  head.next.next = head;
  head.next = null;

  return newHead;
}

// O(N) Time and O(N) space