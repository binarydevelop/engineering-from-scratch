/**
 * @param {number[]} cookies
 * @param {number} k
 * @return {number}
 */
var distributeCookies = function(cookies, k) {
  const children = new Array(k).fill(0);
  let answer = Infinity;

  // Optional: assign larger bags earlier to prune faster
  cookies.sort((a, b) => b - a);

  function backtrack(index) {
    // If current distribution is already worse than our best answer, stop
    const currentMax = Math.max(...children);
    if (currentMax >= answer) {
      return;
    }

    // All cookies assigned
    if (index === cookies.length) {
      answer = Math.min(answer, currentMax);
      return;
    }

    for (let child = 0; child < k; child++) {
      // Choose: give current cookie bag to this child
      children[child] += cookies[index];

      // Explore
      backtrack(index + 1);

      // Undo
      children[child] -= cookies[index];

      // Symmetry pruning:
      // If this child had 0 before receiving the cookie,
      // then trying another empty child is equivalent.
      if (children[child] === 0) {
        break;
      }
    }
  }

  backtrack(0);
  return answer;
};