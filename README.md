# UpSet.js Jupyter Widget

[![NPM Package][npm-image]][npm-url] [![Github Actions][github-actions-image]][github-actions-url]

A Jupyter Widget Library around [UpSet.js](https://github.com/upsetjs/upsetjs).

This package is part of the UpSet.js ecosystem located at the main [Github Monorepo](https://github.com/upsetjs/upsetjs).

## Installation

You can install using `pip`:

```bash
pip install upsetjs_jupyter_widget
```

Or if you use jupyterlab:

```bash
pip install upsetjs_jupyter_widget
jupyter labextension install @jupyter-widgets/jupyterlab-manager@3.0.0.alpha-0
```

## Usage

```python
from ipywidgets import interact
from upsetjs_jupyter_widget import UpSetWidget
import pandas as pd
```

```python
w = UpSetWidget[str]()
```

```python
w.from_dict(dict(one = ['a', 'b', 'c', 'e', 'g', 'h', 'k', 'l', 'm'], two = ['a', 'b', 'd', 'e', 'j'], three = ['a', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm']))
w
```

![upset_from_dict](https://user-images.githubusercontent.com/4129778/79368564-e4715d00-7f4f-11ea-92f5-23ee89b5332f.png)

```python
df = pd.DataFrame(dict(
    one=[1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1],
    two=[1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    three=[1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1]
), index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'])
w.from_dataframe(df)
w
```

![upset_from_dataframe](https://user-images.githubusercontent.com/4129778/79368563-e3d8c680-7f4f-11ea-92d2-db0c7af2882e.png)

it support the `ipywidget` interact method to get notified about the user input

```python
def selection_changed(s):
    return s.name if s else None
interact(selection_changed, s=w)
```

see also [introduction.ipynb](./master/examples/introduction.ipynb)

see also [![Open in NBViewer][nbviewer]](https://nbviewer.jupyter.org/github/upsetjs/upsetjs_jupyter_widget/blob/master/examples/introduction.ipynb)

## Dev Environment

```sh
npm i -g yarn
yarn set version berry
yarn
yarn pnpify --sdk
pipenv
```

```sh
pipenv shell
pip install -e .
pipenv run jupyter labextension install .
```

## Commands

### Testing

```sh
yarn test
```

### Linting

```sh
yarn lint
```

### Building

```sh
yarn install
yarn build
```

### Release

1. `rm dist/*`
1. `yarn build:lib`
1. `yarn npm publish --access public`
1. `python setup.py clean sdist bdist_wheel`
1. `twine upload dist/*`
1. update version in `package.json`, `upsetjs_jupyter_widget/_frontend.py`, `upsetjs_jupyter_widget/_version.py`, `src/version.ts`

## License

### Commercial license

If you want to use Upset.js for a commercial application the commercial license is the appropriate license. Contact [@sgratzl](mailto:sam@sgratzl.com) for details.

### Open-source license

This library is released under the `GNU AGPLv3` version to be used for private and academic purposes. In case of a commercial use, please get in touch regarding a commercial license.

[npm-image]: https://badge.fury.io/js/%40upsetjs%2Fjupyter_widget.svg
[npm-url]: https://npmjs.org/package/@upsetjs/jupyter_widget
[github-actions-image]: https://github.com/upsetjs/upsetjs_jupyter_widget/workflows/ci/badge.svg
[github-actions-url]: https://github.com/upsetjs/upsetjs_jupyter_widget/actions
[codepen]: https://img.shields.io/badge/CodePen-open-blue?logo=codepen
[nbviewer]: https://img.shields.io/badge/NBViewer-open-blue?logo=jupyter
