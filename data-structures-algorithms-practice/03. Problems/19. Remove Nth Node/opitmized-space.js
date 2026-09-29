var removeNthFromEnd = function(head, n) {
    let dummy = new ListNode(0, null)
    let fast = dummy 
    let slow = dummy 
    dummy.next = head

    for(let i = 0; i<n; i++){
        fast=fast.next
    }
    while(fast.next != null){
        slow = slow.next
        fast = fast.next 
    }

    slow.next = slow.next.next

    return dummy.next;
};