/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} head
 * @return {void} Do not return anything, modify head in-place instead.
 */
var reorderList = function(head) {
    let fast = head
    let slow = head

    while(fast && fast.next!= null){
        slow = slow.next
        fast = fast.next.next
    }

    let current = slow.next
    let prev = null
    slow.next = null

    while(current != null){
        let nextNode = current.next
        current.next = prev

        prev = current
        current = nextNode
    }

    let first = head;
    let second = prev

    while(second!= null){
        let temp1 = first.next
        let temp2 = second.next

        first.next = second
        second.next = temp1 

        first = temp1
        second = temp2
    }
};