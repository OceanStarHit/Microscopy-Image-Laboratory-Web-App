// Pattern Matching
const matchPixcels = (baseLine, movingLine) => {
  if (baseLine.length == 0 || movingLine.length == 0) return 0;

  const searchStart =
    baseLine.length >= movingLine.length
      ? -parseInt(movingLine.length / 2)
      : baseLine.length - movingLine.length;
  const searchEnd =
    baseLine.length >= movingLine.length
      ? baseLine.length - parseInt(movingLine.length / 2)
      : 0;

  let scores = [];
  for (let i = searchStart; i < searchEnd; i++) {
    var score = -1000000;
    for (let j = 0; j < movingLine.length; j++) {
      for (let c = 0; c < 4; c++) {
        let baseIdx = i + j;
        if (baseIdx < 0 || baseIdx >= baseLine.length) {
          score += 0;
        } else {
          const s = 255 - Math.abs(baseLine[baseIdx][c] - movingLine[j][c]);
          score += s;
        }
      }
    }
    scores.push(score);
  }
  console.log(scores);
  let maxS = Math.max(...scores);

  console.log(maxS);
  console.log(scores.indexOf(maxS));
  return searchStart + scores.indexOf(maxS);
};

export { matchPixcels };
