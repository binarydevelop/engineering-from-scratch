function soln(nums) {
    let results = [];

    for (let i = 0; i < nums.length; i++) {
        let product = 1;

        for (let j = 0; j < nums.length; j++) {
            if (i !== j) {
                product *= nums[j];
            }
        }

        results[i] = product;
    }

    return results;
}

let nums = [1, 2, 3, 4];
console.log(soln(nums));