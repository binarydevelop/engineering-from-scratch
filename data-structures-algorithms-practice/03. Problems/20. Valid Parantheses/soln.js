/**
 * @param {string} s
 * @return {boolean}
 */
var soln = function(s) {
    let bracketMap = {
        '(': ')',
        '[': ']',
        '{': '}'
    };

    let stack = [];

    for (let i = 0; i < s.length; i++) {
        let char = s[i];

        if (bracketMap[char]) {
            stack.push(bracketMap[char]);
        } else {
            let top = stack.pop();

            if (top !== char) {
                return false;
            }
        }
    }

    return stack.length === 0;
};

let s = "()";
console.log(soln(s)); // true