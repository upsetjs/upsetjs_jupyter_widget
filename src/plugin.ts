// Copyright (c) Samuel Gratzl

import { Application, IPlugin } from '@phosphor/application';
import { Widget } from '@phosphor/widgets';
import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';
import * as widgetExports from './widget';
import { MODULE_NAME, MODULE_VERSION } from './version';

const EXTENSION_ID = '@upsetjs/jupyter_widget:plugin';

/**
 * The example plugin.
 */
const upsetjsPlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry as any],
  activate: activateWidgetExtension,
  autoStart: true,
};

export default upsetjsPlugin;

/**
 * Activate the widget extension.
 */
function activateWidgetExtension(_app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: widgetExports,
  });
}
