/**
 * @upsetjs/jupyter_widget
 * https://github.com/upsetjs/upsetjs_jupyter_widget
 *
 * Copyright (c) 2021 Samuel Gratzl <sam@sgratzl.com>
 */

// Entry point for the notebook bundle containing custom model definitions.
//
// Setup notebook base URL
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
(window as any).__webpack_public_path__ =
  document.querySelector('body')!.getAttribute('data-base-url') + 'nbextensions/upsetjs_jupyter_widget';

export * from './index';
