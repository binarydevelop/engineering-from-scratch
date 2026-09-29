function bucketSort(arr, bucketCount = 10) {
  if (arr.length <= 1) return arr;

  const min = Math.min(...arr);
  const max = Math.max(...arr);

  if (min === max) return arr;

  const buckets = Array.from({ length: bucketCount }, () => []);

  const range = max - min;

  for (const num of arr) {
    let index = Math.floor(((num - min) / range) * bucketCount);

    if (index === bucketCount) {
      index = bucketCount - 1;
    }

    buckets[index].push(num);
  }

  const result = [];

  for (const bucket of buckets) {
    bucket.sort((a, b) => a - b);
    result.push(...bucket);
  }

  return result;
}

const nums = [29, 25, 3, 49, 9, 37, 21, 43];

console.log(bucketSort(nums));