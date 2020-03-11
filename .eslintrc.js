module.exports = {
  extends: ['react-app', 'prettier/@typescript-eslint', 'plugin:prettier/recommended'],
  parserOptions: {
    project: './tsconfig.lint.json',
  },
  settings: {
    react: {
      version: '999.999.999',
    },
  },
};
