function soln(head){
    let prev = null
    let current = head

    while(current!=null){
        let next = current.next
        current.next = prev

        prev = current
        current = head
    }

    return prev
}

// O(n) Time and O(1) space