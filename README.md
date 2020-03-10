
# upsetjs_jupyter_widget

[![Build Status](https://travis-ci.org/upsetjs/upsetjs_jupyter_widget.svg?branch=master)](https://travis-ci.org/upsetjs/upsetjs_jupyter_widget)
[![codecov](https://codecov.io/gh/upsetjs/upsetjs_jupyter_widget/branch/master/graph/badge.svg)](https://codecov.io/gh/upsetjs/upsetjs_jupyter_widget)


A Jupyter Widget Library around UpSet.js

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
