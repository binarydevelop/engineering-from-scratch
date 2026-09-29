function hasCycle(head) {
  const visited = new Set();

  let current = head;

  while (current !== null) {
    if (visited.has(current)) {
      return true;
    }

    visited.add(current);

    current = current.next;
  }

  return false;
}