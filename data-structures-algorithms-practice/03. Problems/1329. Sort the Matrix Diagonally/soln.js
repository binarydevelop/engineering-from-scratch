/**
 * @param {number[][]} mat
 * @return {number[][]}
 */
var diagonalSort = function(matrix) {
    console.log(matrix)
    let map = new Map()
    let rows =matrix.length;
    let cols = matrix[0].length;
    for(let i = 0; i < rows; i++){
        for(let j = 0; j < cols; j++){
            let key  = i- j
            if(!map.has(key)){
                map.set(key, [])
            }
            map.get(key).push(matrix[i][j])
        }
    }

    for(let arr of map.values()){
        arr.sort((a,b) => a-b)
    }

    for(let i = rows-1; i >= 0; i--){
        for(let j = cols-1; j >= 0; j--){
            matrix[i][j] = map.get(i-j).pop()
        }
    }

    return matrix
};

let matrix =[[11,25,66,1,69,7],[23,55,17,45,15,52],[75,31,36,44,58,8],[22,27,33,25,68,4],[84,28,14,11,5,50]]
console.log(diagonalSort(matrix))