module.exports = {
  transformIgnorePatterns: [], // transform all
  preset: 'ts-jest/presets/js-with-ts',
  testRegex: 'src/.*\\.spec\\.(ts|tsx)$',
  globals: {
    'ts-jest': {
      tsConfig: './tsconfig.test.json',
      babelConfig: false,
    },
  },
};
