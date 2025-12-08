const fs = require("fs");
const readline = require("readline");

const charToPrio = (char) => {
  const ascii = char.charCodeAt(0);
  return ascii > 96 ? ascii - 96 : ascii - 64 + 26;
};

async function getResult() {
  let total = 0;
  let foundItems = [];

  const rl = readline.createInterface({
    input: fs.createReadStream("2022/input.txt"),
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    const [front, back] = [
      line.slice(0, line.length / 2),
      line.slice(line.length / 2),
    ];
    for (var i = 0; i < front.length; i++) {
      const char = front.charAt(i);
      if (back.includes(char)) {
        foundItems.push({ char, priority: charToPrio(char) });
        break;
      }
    }
  }
  console.log(
    "result",
    foundItems.reduce((p, c) => p + c.priority, 0)
  );
}

getResult();
