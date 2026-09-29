function generateParenthesis(n) {
  // result will store all valid combinations.
  const result = [];

  // backtrack builds the current parentheses string.
  // current = string built so far
  // open = number of "(" used so far
  // close = number of ")" used so far
  function backtrack(current, open, close) {
    // Base case:
    // If current length is 2 * n, we used all parentheses.
    if (current.length === 2 * n) {
      result.push(current);
      return;
    }

    // Choice 1: Add "("
    // We can add "(" only if we have not used all n opening brackets.
    if (open < n) {
      backtrack(current + "(", open + 1, close);
    }

    // Choice 2: Add ")"
    // We can add ")" only if there are more "(" than ")".
    // This keeps the string valid.
    if (close < open) {
      backtrack(current + ")", open, close + 1);
    }
  }

  // Start with an empty string and zero brackets used.
  backtrack("", 0, 0);

  return result;
}