/* eslint-env node */

// eslint-disable-next-line @typescript-eslint/no-var-requires
const pkg = require('./package.json');

module.exports = {
  extends: ['react-app', 'plugin:prettier/recommended'],
  parserOptions: {
    project: './tsconfig.eslint.json',
  },
  settings: {
    react: {
      version: pkg.devDependencies.react ? 'detect' : '99.99.99',
    },
  },
  rules: {
    // '@typescript-eslint/explicit-module-boundary-types': 'off',
    // '@typescript-eslint/no-explicit-any': 'off',
    // '@typescript-eslint/no-non-null-assertion': 'off',
  },
};
