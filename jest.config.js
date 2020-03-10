module.exports = {
  transform: {
    '.*\\.(t|j)sx?': require.resolve('ts-jest'),
  },
  transformIgnorePatterns: ['x'], // transform all
  testRegex: 'src/.*\\.spec\\.(ts|tsx)$',
  moduleFileExtensions: ['ts', 'tsx', 'js'],
  verbose: true,
  globals: {
    'ts-jest': {
      tsConfig: './tsconfig.test.json',
      diagnostics: true,
      babelConfig: false,
    },
  },
};
