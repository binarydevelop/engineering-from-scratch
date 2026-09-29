function mergeTwoSortedList(list1, list2){
    let l1 = 0;
    let l2 = 0;
    let merged = [];
    while(l1 < list1.length && l2 < list2.length){
      if(list1[l1] < list2[l2]){
        merged.push(list1[l1]);
        l1++;
      } else {
        merged.push(list2[l2])
        l2++;
      }
    }
    
    while(l1 < list1.length){
      merged.push(list1[l1]);
      l1++;
    }
    while(l2 < list2.length){
      merged.concat(list2[l2]);
      l2++;
    }
    return merged;
  }
  
  
  const list1 = [1,2,4];
  const list2 = [1,3,4];
  
  console.log(mergeTwoSortedList(list1, list2));

  /* https://leetcode.com/problems/merge-two-sorted-lists/ */