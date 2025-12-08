const fs = require("fs");
const readline = require("readline");

const getScore = (result, pick) => {
  let s = 3 * result;
  s += pickToNumber(pick);
  return s;
};

const getResult = (own, theirs) => {
  const o = pickToNumber(own);
  const t = pickToNumber(theirs);
  console.log({ o, t });
  if (o === t) {
    return 1; // tie
  } else if (o % 3 === (t + 1) % 3) {
    return 2;
  } else {
    return 0;
  }
};

const pickToNumber = (pick) => {
  if (pick === "A" || pick === "X") {
    return 1;
  } else if (pick === "B" || pick === "Y") {
    return 2;
  } else {
    return 3;
  }
};

async function processLineByLine() {
  let total = 0;

  const rl = readline.createInterface({
    input: fs.createReadStream("2022/input.txt"),
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    if (line.length !== 3) throw new Error("something went wrong");
    // console.log("line", line);
    const result = getResult(line[2], line[0]);
    const score = getScore(result, line[2]);
    console.log({ result, score });
    total += score;
    console.log({ total });
  }
}

const getBonusResult = (res) => {
  if (res === "X") {
    return 0;
  } else if (res === "Y") {
    return 1;
  } else if (res === "Z") {
    return 2;
  }
};

const getBonusChoice = (theirs, result) => {
  const r = result - 1;
  let pick = (pickToNumber(theirs) + r) % 4;
  if (pick === 0) {
    if (r === 1) {
      pick = 1;
    } else {
      pick = 3;
    }
  }
  return pick;
};

const getBonusScore = (result, choice) => {
  let s = result * 3;
  return s + choice;
};

const bonus = async () => {
  let total = 0;

  const rl = readline.createInterface({
    input: fs.createReadStream("input.txt"),
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    const result = getBonusResult(line[2]);
    const choice = getBonusChoice(line[0], result);
    const score = getBonusScore(result, choice);
    total += score;
    console.log({ theirs: line[0], result, choice, score, total });
  }
  console.log(total);
};

// processLineByLine();
bonus();
