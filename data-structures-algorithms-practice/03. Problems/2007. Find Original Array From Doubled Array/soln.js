/**
 * @param {number[]} changed
 * @return {number[]}
 */
var findOriginalArray = function(changed) {
    let map = new Map()
    const results = []
    changed.sort((a,b) => a-b)
    if (changed.length % 2 !== 0) return [];
    for (let i  =0; i < changed.length; i++){
        map.set(changed[i], (map.get(changed[i]) || 0 ) + 1)
    }

    for(let i = 0; i < changed.length; i++){
        let twice = changed[i] * 2;
        if (map.get(changed[i]) === 0) continue;
        if(!map.has(twice) || map.get(twice) == 0) return []
        
        results.push(changed[i]);

        map.set(changed[i], map.get(changed[i]) - 1)
        map.set(twice, map.get(twice) -1)
    }

    return results
};

console.log(findOriginalArray([6,3,0,1]))