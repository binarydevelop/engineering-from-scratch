function letterCombinations(digits) {
  // If digits is empty, there are no combinations.
  if (digits.length === 0) {
    return [];
  }

  // Map each digit to its possible letters.
  const phoneMap = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz"
  };

  // This will store all final combinations.
  const result = [];

  // Backtracking helper function.
  // index = which digit we are currently processing.
  // current = string built so far.
  function backtrack(index, current) {
    // Base case:
    // If current length equals digits length,
    // we have built one complete combination.
    if (index === digits.length) {
      result.push(current);
      return;
    }

    // Get the current digit.
    const digit = digits[index];

    // Get the letters for that digit.
    const letters = phoneMap[digit];

    // Try every possible letter for this digit.
    for (const letter of letters) {
      // Choose this letter and move to the next digit.
      backtrack(index + 1, current + letter);
    }
  }

  // Start from index 0 with an empty string.
  backtrack(0, "");

  return result;
}