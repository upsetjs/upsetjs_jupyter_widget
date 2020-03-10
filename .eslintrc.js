module.exports = {
  env: {
    browser: true,
    jest: true,
  },
  extends: ['prettier/@typescript-eslint', 'plugin:prettier/recommended'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: require.resolve('./tsconfig.json'),
  },
  plugins: ['@typescript-eslint'],
};
