# UpSet.js Jupyter Widget

[![NPM Package][npm-image]][npm-url] [![Github Actions][github-actions-image]][github-actions-url] [![Open in NBViewer][nbviewer]][nbviewer-url] [![Open in Binder][binder]][binder-j-url] [![Open API Docs][docs]][docs-j-url] [![Open Example][example]][example-j-url]

A Jupyter Widget Library around [UpSet.js](https://github.com/upsetjs/upsetjs).

This package is part of the UpSet.js ecosystem located at the main [Github Monorepo](https://github.com/upsetjs/upsetjs).

## Installation

You can install using `pip`:

jupyter-lab 1.2.x:

```bash
pip install ipywidgets==7.5.1 upsetjs_jupyter_widget
# for notebooks
jupyter nbextension enable --sys-prefix --py upsetjs_jupyter_widget
# for lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager @upsetjs_jupyter_widget
```

jupyter-lab 2.1.x:

```bash
# some ipywidget 8.x.x alpha vesion
pip install ipywidgets upsetjs_jupyter_widget
# for notebooks
jupyter nbextension enable --sys-prefix --py upsetjs_jupyter_widget
# for lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager@3.0.0-alpha.0 @upsetjs_jupyter_widget
```

## Usage

```python
from ipywidgets import interact
from upsetjs_jupyter_widget import UpSetJSWidget
import pandas as pd
```

```python
w = UpSetJSWidget[str]()
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

see also ![Open in NBViewer][nbviewer]][nbviewer-url] ![Open in Binder][binder]][binder-url]

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
jupyter nbextension install --sys-prefix --overwrite --py upsetjs_jupyter_widget
jupyter nbextension enable --sys-prefix --py upsetjs_jupyter_widget
jupyter labextension install @jupyter-widgets/jupyterlab-manager@3.0.0-alpha.0
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

based on release-it

**within the pipenv**

```sh
yarn release:major
yarn release:minor
yarn release:patch
```

## Privacy Policy

UpSet.js is a client only library. The library or any of its integrations doesn't track you or transfers your data to any server. The uploaded data in the app are stored in your browser only using IndexedDB. The Tableau extension can run in a sandbox environment prohibiting any server requests. However, as soon as you export your session within the app to an external service (e.g., Codepen.io) your data will be transferred.

## License / Terms of Service

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
[nbviewer-url]: https://nbviewer.jupyter.org/github/upsetjs/upsetjs_jupyter_widget/blob/master/examples/introduction.ipynb
[binder]: https://mybinder.org/badge_logo.svg
[binder-j-url]: https://mybinder.org/v2/gh/upsetjs/upsetjs_jupyter_widget/master?urlpath=lab/tree/examples/introduction.ipynb
[docs]: https://img.shields.io/badge/API-open-blue
[docs-j-url]: https://upset.js.org/api/jupyter
[example]: https://img.shields.io/badge/Example-open-red
[example-j-url]: https://upset.js.org/integrations/jupyter
