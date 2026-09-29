/**
 * @param {number[]} cookies
 * @param {number} k
 * @return {number}
 */
var distributeCookies = function(cookies, k) {
  const children = new Array(k).fill(0);
  let answer = Infinity;

  function backtrack(index) {
    // All cookie bags have been assigned
    if (index === cookies.length) {
      const unfairness = Math.max(...children);
      answer = Math.min(answer, unfairness);
      return;
    }

    // Try giving current cookie bag to every child
    for (let child = 0; child < k; child++) {
      // Choose
      children[child] += cookies[index];

      // Explore
      backtrack(index + 1);

      // Undo
      children[child] -= cookies[index];
    }
  }

  backtrack(0);
  return answer;
};