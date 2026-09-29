// https://www.geeksforgeeks.org/problems/check-if-an-array-is-sorted0701/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card


function arraySortedOrNot(arr) {
    for(let i = 0; i < arr.length; i++){
        if(arr[i] > arr[i+1]) return false
    }
    return true;
}