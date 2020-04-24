const { Plugin } = require('release-it');
const fs = require('fs');
const path = require('path');

function bumpFile(file, reg, replace) {
  console.log('bumping', file);
  const desc = path.resolve(file);
  const content = fs.readFileSync(desc).toString();
  const newContent = content.replace(reg, replace);
  fs.writeFileSync(desc, newContent);
}

function bumpImpl(version) {
  bumpFile('./upsetjs_jupyter_widget/_frontend.py', /^MODULE_VERSION.*$/gm, `MODULE_VERSION = "^${version}"`);
  bumpFile(
    './upsetjs_jupyter_widget/_version.py',
    /^version_info =.*$/gm,
    `version_info = (${version.split('.').join(', ')})  # pylint: disable=C0103`
  );
  bumpFile('./src/version.ts', /^export const MODULE_VERSION = .*$/gm, `export const MODULE_VERSION = '${version}';`);
}

class MyVersionPlugin extends Plugin {
  bump(version) {
    bumpImpl(version);
  }
}

module.exports = MyVersionPlugin;
