module.exports = {
  transform: {
    '^.+\\.(t|j)sx?$': require.resolve('ts-jest'),
  },
  transformIgnorePatterns: [], // transform all
  testRegex: 'src/.*\\.spec\\.(ts|tsx)$',
  moduleFileExtensions: ['ts', 'tsx', 'js'],
  verbose: true,
  globals: {
    'ts-jest': {
      tsConfig: require.resolve('./tsconfig.json'),
      diagnostics: true,
      babelConfig: false,
    },
  },
};
