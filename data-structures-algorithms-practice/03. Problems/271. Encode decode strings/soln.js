    function encode(strs) {
        let encoded = ''
        for(let str of strs){
            encoded+=str.length+'#'+str
        }
        console.log(encoded)
    }

    function decode(str) {
        let i = 0
        let results = []
        while(i < str.length){
            let j = i
            while(str[j]!='#'){
                j++
            }
            let length = Number(str.slice(i,j))
            let start = j+1
            let end = start + length
        results.push(str.slice(start, end))
        i = end
        }
    console.log(results)
    }
    
let str = '4#neet4#code4#love3#you'
console.log(decode(str))