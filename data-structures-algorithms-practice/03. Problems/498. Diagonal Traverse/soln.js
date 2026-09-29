/**
 * @param {number[][]} mat
 * @return {number[]}
 */
var findDiagonalOrder = function(matrix) {
    let map = new Map();
    let rows = matrix.length;
    let cols = matrix[0].length;
    let dir = true
    let results = []
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            let key = i + j;

            if (!map.has(key)) {
                map.set(key, []);
            }

            map.get(key).push(matrix[i][j]);
        }
    }

    for(let key = 0; key <= rows + cols -2; key++){
        let values = map.get(key)
        if(key % 2 == 0 ){
            results.push(...values.reverse())
        } else {
            results.push(...values)
        }
    }


    return results

};


console.log(findDiagonalOrder([[1,2,3],[4,5,6],[7,8,9]]))