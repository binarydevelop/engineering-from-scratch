function soln(s,t){
    let map = new Map()

    for(let c in s) map.set(c, (map.get(c) || 0) + 1)
    for(let c in t) map.set(c, (map.get(c) || 0) - 1)

    for(let count of map.values()){
        if(count!== 0){
            return false
        }
    }
    return true
}