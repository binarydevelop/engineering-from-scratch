/**
 * @param {string[]} tokens
 * @return {number}
 */
var evalRPN = function(tokens) {
    const ops = new Set(['+','-','*','/'])
 
    
    let stack = []
    let results = 1
    for(const token of tokens){
        if(!ops.has(token)){
             stack.push(Number(token))
        } else {
                let b = stack.pop()
                let a = stack.pop() 
            if (token === '+') stack.push(a + b);
            if (token === '-') stack.push(a - b);
            if (token === '*') stack.push(a * b);
            if (token === '/') stack.push(Math.trunc(a / b));
        }
    }
    
    return stack[0]

};