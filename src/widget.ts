// Copyright (c) Samuel Gratzl

import { DOMWidgetModel, DOMWidgetView, ISerializers } from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';
import { renderUpSet, UpSetProps, ISetLike } from '@upsetjs/bundle';

export class UpSetModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: UpSetModel.model_name,
      _model_module: UpSetModel.model_module,
      _model_module_version: UpSetModel.model_module_version,
      _view_name: UpSetModel.view_name,
      _view_module: UpSetModel.view_module,
      _view_module_version: UpSetModel.view_module_version,
    };
  }

  static readonly serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static readonly model_name = 'UpSetModel';
  static readonly model_module = MODULE_NAME;
  static readonly model_module_version = MODULE_VERSION;
  static readonly view_name = 'UpSetView'; // Set to null if no view
  static readonly view_module = MODULE_NAME; // Set to null if no view
  static readonly view_module_version = MODULE_VERSION;
}

export class UpSetView extends DOMWidgetView {
  render() {
    this.model.on('change:value', this.value_changed, this);
    this.renderImpl();
  }

  private changeSelection = (s: ISetLike<any> | null) => {
    this.model.set('value', s ? s.name : null);
  };

  private generateProps(): UpSetProps<any> {
    const state = this.model.get_state(true);

    const props: UpSetProps<any> = {
      sets: [],
      width: 300,
      height: 300,
    };

    const toCamelCase = (v: string) => v.replace(/([-_]\w)/g, (g) => g[1].toUpperCase());

    Object.keys(state).forEach((key) => {
      let v = state[key];
      if (key.startsWith('_') || ['layout', 'value'].includes(key) || v == null) {
        return;
      }
      const propName = toCamelCase(key);
      if (propName === 'fontSizes' || propName === 'combinations') {
        const converted: any = {};
        Object.keys(v).forEach((key) => {
          converted[toCamelCase(key)] = (v as any)![key];
        });
        v = converted;
      }
      (props as any)[propName] = v;
    });

    // TODO convert sets, queries, combinations

    if (state.mode === 'click') {
      props.onClick = this.changeSelection;
    } else {
      props.onHover = this.changeSelection;
    }

    return props;
  }

  private renderImpl() {
    const props = this.generateProps();
    const bb = this.el.getBoundingClientRect();
    if (!bb.width || !bb.height) {
      requestAnimationFrame(() => {
        const bb2 = this.el.getBoundingClientRect();
        props.width = bb2.width || 600;
        props.height = bb2.height || 400;
        renderUpSet(this.el, props);
      });
      return;
    }
    props.width = bb.width;
    props.height = bb.height;
    renderUpSet(this.el, props);
  }

  value_changed() {
    this.renderImpl();
  }
}
