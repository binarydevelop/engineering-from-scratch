var MinStack = function() {
    this.stack = []
    this.stackTracker = []
    this.currentMin = Infinity
};

/** 
 * @param {number} value
 * @return {void}
 */
MinStack.prototype.push = function(value) {
    this.stack.push(value);

    const minSoFar = this.stackTracker.length
        ? Math.min(this.stackTracker[this.stackTracker.length - 1], value)
        : value;

    this.stackTracker.push(minSoFar);
};

/**
 * @return {void}
 */
MinStack.prototype.pop = function() {
    this.stack.pop()
    this.stackTracker.pop()
};

/**
 * @return {number}
 */
MinStack.prototype.top = function() {
    return this.stack.length ?  this.stack[this.stack.length-1] : -1
};

/**
 * @return {number}
 */
MinStack.prototype.getMin = function() {
    return this.stackTracker[this.stackTracker.length-1]
};

/** 
 * Your MinStack object will be instantiated and called as such:
 * var obj = new MinStack()
 * obj.push(value)
 * obj.pop()
 * var param_3 = obj.top()
 * var param_4 = obj.getMin()
 */