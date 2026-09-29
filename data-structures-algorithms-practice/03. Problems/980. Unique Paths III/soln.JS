/**
 * @param {number[][]} grid
 * @return {number}
 */
var uniquePathsIII = function(grid) {
    let rows = grid.length
    let cols = grid[0].length

    let count = 0 // Number of paths found 
    let empty_squares = 0
    let start_x = -1
    let start_y = -1

    for(let i = 0; i<rows; i++){
        for(let j = 0; j<cols; j++){
            if(grid[i][j] == 0) empty_squares++
            if(grid[i][j] == 1) {
                start_x = i
                start_y = j
            }
        }
    }
    let squaresToVisit = empty_squares + 1;

    function backTrack(i,j, visitedCount){
        if(
            i < 0 ||
            i >= rows ||
            j < 0 ||
            j >= cols ||
            grid[i][j] == -1 
        ){
            return;
        }

        if(grid[i][j] == 2){
            if(visitedCount == squaresToVisit){
                count++
                return
            }
        }

        let temp = grid[i][j];
        grid[i][j] = -1

        backTrack(i+1, j, visitedCount+1)
        backTrack(i-1, j, visitedCount+1)
        backTrack(i, j+1, visitedCount+1)
        backTrack(i, j-1, visitedCount+1)
        
        grid[i][j] = temp

        return
    }
    backTrack(start_x, start_y, 0)

    return count
};