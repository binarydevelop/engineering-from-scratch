
function isHappy(N,C,A){
    let candiesRequired = 0;
    for(let i =0 ; i < N; i++){
        candiesRequired += A[i]
    }
    if(candiesRequired > C){
        console.log('No')
    }else {
        console.log('Yes')
    }
}
isHappy(3,7, [4,2,2]);

/* https://www.codechef.com/problems/LECANDY?tab=submissions */