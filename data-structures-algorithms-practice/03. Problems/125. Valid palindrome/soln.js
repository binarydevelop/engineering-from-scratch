function soln(str){
    const regex = /[^a-zA-Z0-9]/g;

    let modifiedString = str.replace(regex, '').toLowerCase()

    let start = 0 
    let end = modifiedString.length-1
  
    while(start<end){
        if(modifiedString[start] !== modifiedString[end]){
            return false
        }
        start++
        end--
    }
    return true
}

let str = "A man, a plan, a canal: Panama"
console.log(soln(str))