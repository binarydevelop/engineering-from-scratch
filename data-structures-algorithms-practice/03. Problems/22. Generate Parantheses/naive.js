function generateParenthesis(n) {
  const result = [];

  function isValid(str) {
    let balance = 0;

    for (const char of str) {
      if (char === "(") {
        balance++;
      } else {
        balance--;
      }

      // More closing than opening at some point
      if (balance < 0) {
        return false;
      }
    }

    return balance === 0;
  }

  function generate(current) {
    if (current.length === 2 * n) {
      if (isValid(current)) {
        result.push(current);
      }
      return;
    }

    generate(current + "(");
    generate(current + ")");
  }

  generate("");
  return result;
}