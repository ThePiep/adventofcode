const fs = require("fs");
const readline = require("readline");

// [1st, 2nd, 3rd]
let top = [0, 0, 0];

let current = 0;

const rl = readline.createInterface({
  input: fs.createReadStream("2022/input.txt"),
  crlfDelay: Infinity,
});

const saveScore = (score) => {
  if (score > top[0]) {
    top = [score, ...top.slice(0, 2)];
  } else if (score > top[1]) {
    top = [top[0], score, top[1]];
  } else if (score > top[2]) {
    top = [top[0], top[1], score];
  }
};

rl.on("line", (line) => {
  const int = parseInt(line);
  if (isNaN(int)) {
    saveScore(current);
    console.log(top);
    current = 0;
  } else {
    current += int;
  }
});

rl.on("close", () => {
  saveScore(current);
  console.log("top 3", top);
  console.log(
    "Combined calories of top 3",
    top.reduce((p, c) => p + c)
  );
});
