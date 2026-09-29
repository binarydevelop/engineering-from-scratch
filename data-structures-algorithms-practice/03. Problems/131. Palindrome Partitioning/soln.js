/**
 * @param {string} s
 * @return {string[][]}
 */
var partition = function(s) {
    const result = [];
    const path = [];

    function isPalindrome(str) {
        let start = 0;
        let end = str.length - 1;

        while (start < end) {
            if (str[start] !== str[end]) {
                return false;
            }

            start++;
            end--;
        }

        return true;
    }

    function backTrack(idx) {
        if (idx === s.length) {
            result.push([...path]);
            return;
        }

        for (let i = idx; i < s.length; i++) {
            const piece = s.slice(idx, i + 1);

            if (!isPalindrome(piece)) {
                continue;
            }

            path.push(piece);
            backTrack(i + 1);
            path.pop();
        }
    }

    backTrack(0);

    return result;
};