/**
 * @param {number} x
 * @return {number}
 */
var reverse = function(n) {
    let isNegative = false;

    if(n < 0){
        isNegative = true
        n *= -1;
    } 
    let reversed = 0;
    while(n > 0){
        remainder = n % 10
        reversed = reversed * 10 + remainder
        n = Math.floor(n/10);
    }
    if (reversed > 2 ** 31 - 1 || reversed < -(2 ** 31)) return 0;

    return isNegative == true ? reversed * -1 : reversed ; 
};
