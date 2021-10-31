const fs = require('fs')
const MiniSearch = require('minisearch')
const parse = require('node-html-parser').parse;

function getFiles(dir) {
  return fs.readdirSync(dir).flatMap((item) => {
    const path = `${dir}/${item}`;
    if (fs.statSync(path).isDirectory()) {
      return getFiles(path);
    }

    return path;
  });
}

function splitToBulks(arr, bulkSize) {
    const bulks = [];
    for (let i = 0; i < Math.ceil(arr.length / bulkSize); i++) {
        bulks.push(arr.slice(i * bulkSize, (i + 1) * bulkSize));
    }
    return bulks;
}

const BATCH_SIZE = 10000
const LOG_EVERY = 1000
const dir = process.argv[2]
const files = getFiles(dir)
console.log(`Got ${files.length} files`)
splitToBulks(files, BATCH_SIZE).forEach((batch, i) => {
  console.log(`processing batch ${i}`)
  const documents = batch.map((f, j) => {
    if (j % LOG_EVERY === 0) {
      console.log(`progress ${j}`)
    }
    const html = fs.readFileSync(f, 'utf8')
    const doc = parse(html)
    const relevant = doc.querySelector('div#divImprimir')
    return {
      id: f,
      html: relevant ? relevant.text.toString() : '',
    }
  })

  let miniSearch = new MiniSearch({
    fields: ['html'],
    storeFields: [],
  })
  miniSearch.addAll(documents)
  fs.writeFileSync(`index${i}.json`, JSON.stringify(miniSearch.toJSON()))
  console.log(`finished batch ${i}`)
})

