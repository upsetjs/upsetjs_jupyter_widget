# UpSet.js Jupyter Widget

[![NPM Package][npm-image]][npm-url] [![Github Actions][github-actions-image]][github-actions-url]

A Jupyter Widget Library around [UpSet.js](https://github.com/upsetjs/upsetjs).

## Installation

You can install using `pip`:

```bash
pip install upsetjs_jupyter_widget
```

Or if you use jupyterlab:

```bash
pip install upsetjs_jupyter_widget
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:

```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] upsetjs_jupyter_widget
```

## Dev Environment

```sh
npm i -g yarn
yarn set version berry
yarn plugin import version
yarn install
yarn pnpify --sdk
```

## Commands

## Testing

```sh
yarn test
```

## Linting

```sh
yarn lint
```

## Building

```sh
yarn install
yarn build
```

## License

### Commercial license

If you want to use Upset.js for a commercial application the commercial license is the appropriate license. With this option, your source code is kept proprietary. Contact @sgratzl for details

### Open-source license

GNU AGPLv3

[npm-image]: https://badge.fury.io/js/@upsetjs/jupyter_widget.svg
[npm-url]: https://npmjs.org/package/@upsetjs/jupyter_widget
[github-actions-image]: https://github.com/sgratzl/upsetjs/workflows/ci/badge.svg
[github-actions-url]: https://github.com/sgratzl/upsetjs/actions
[codepen]: https://img.shields.io/badge/CodePen-open-blue?logo=codepen
