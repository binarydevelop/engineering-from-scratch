function soln(nums) {
    let left = 0;
    let right = nums.length - 1;

    let lmax = 0;
    let rmax = 0;

    let total = 0;

    while (left < right) {
        if (nums[left] < nums[right]) {
            if (nums[left] >= lmax) {
                lmax = nums[left];
            } else {
                total += lmax - nums[left];
            }
            left++;
        } else {
            if (nums[right] >= rmax) {
                rmax = nums[right];
            } else {
                total += rmax - nums[right];
            }
            right--;
        }
    }

    return total;
}

let nums = [4, 2, 0, 3, 2, 5];

console.log(soln(nums)); // 9