const path = require('path');
const version = require('./package.json').version;
const PnpWebpackPlugin = require('pnp-webpack-plugin');

// Custom webpack rules
const rules = [{ test: /\.ts$/, loader: 'ts-loader', options: { configFile: 'tsconfig.build.json' } }];

// Packages that shouldn't be bundled but loaded at runtime
const externals = ['@jupyter-widgets/base'];

const resolve = {
  // Add '.ts' and '.tsx' as resolvable extensions.
  extensions: ['.webpack.js', '.web.js', '.ts', '.js'],
  plugins: [PnpWebpackPlugin],
};
const resolveLoader = {
  plugins: [PnpWebpackPlugin.moduleLoader(module)],
};

module.exports = [
  /**
   * Notebook extension
   *
   * This bundle only contains the part of the JavaScript that is run on load of
   * the notebook.
   */
  {
    entry: './src/extension.ts',
    output: {
      filename: 'index.js',
      path: path.resolve(__dirname, 'upsetjs_jupyter_widget', 'nbextension', 'static'),
      libraryTarget: 'amd',
    },
    module: {
      rules: rules,
    },
    devtool: 'source-map',
    externals,
    resolve,
    resolveLoader,
  },

  /**
   * Embeddable upsetjs_jupyter_widget bundle
   *
   * This bundle is almost identical to the notebook extension bundle. The only
   * difference is in the configuration of the webpack public path for the
   * static assets.
   *
   * The target bundle is always `dist/index.js`, which is the path required by
   * the custom widget embedder.
   */
  {
    entry: './src/index.ts',
    output: {
      filename: 'index.js',
      path: path.resolve(__dirname, 'dist'),
      libraryTarget: 'amd',
      library: '@upsetjs/jupyter_widget',
      publicPath: 'https://unpkg.com/@upsetjs/jupyter_widget@' + version + '/dist/',
    },
    devtool: 'source-map',
    module: {
      rules: rules,
    },
    externals,
    resolve,
    resolveLoader,
  },

  /**
   * Documentation widget bundle
   *
   * This bundle is used to embed widgets in the package documentation.
   */
  {
    entry: './src/index.ts',
    output: {
      filename: 'embed-bundle.js',
      path: path.resolve(__dirname, 'docs', 'source', '_static'),
      library: '@upsetjs/jupyter_widget',
      libraryTarget: 'amd',
    },
    module: {
      rules: rules,
    },
    devtool: 'source-map',
    externals,
    resolve,
    resolveLoader,
  },
];
