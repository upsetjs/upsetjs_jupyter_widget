/**
 * @upsetjs/jupyter_widget
 * https://github.com/upsetjs/upsetjs_jupyter_widget
 *
 * Copyright (c) 2020 Samuel Gratzl <sam@sgratzl.com>
 */

// Entry point for the notebook bundle containing custom model definitions.
//
define(function () {
  'use strict';

  window['requirejs'].config({
    map: {
      '*': {
        '@upsetjs/jupyter_widget': 'nbextensions/@upsetjs/jupyter_widget/index',
      },
    },
  });
  // Export the required load_ipython_extension function
  return {
    load_ipython_extension: function () {},
  };
});
