/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} head
 * @param {number} n
 * @return {ListNode}
 */
var removeNthFromEnd = function(head, n) {
    let dummy = new ListNode(0, head);

    let current = head;
    let index = 1;
    let map = new Map();

    map.set(0, dummy);

    while (current !== null) {
        map.set(index, current);
        current = current.next;
        index++;
    }

    let length = index - 1;
    let toRemove = length - n + 1;

    let prevNode = map.get(toRemove - 1);
    let removalNode = map.get(toRemove);

    prevNode.next = removalNode.next;
    removalNode.next = null;

    return dummy.next;
};

//TIME O(N) SPACE O(N)