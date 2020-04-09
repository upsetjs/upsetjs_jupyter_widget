// Copyright (c) Samuel Gratzl

import { DOMWidgetModel, DOMWidgetView, ISerializers } from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';
import { isElemQuery, ISetCombinations, ISetLike, isSetQuery, renderUpSet, UpSetProps } from '@upsetjs/bundle';
import { fixCombinations, fixSets, resolveSet } from './utils';

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
  private props: UpSetProps<any> = {
    sets: [],
    width: 300,
    height: 300,
  };
  private elems: any[] = [];
  private readonly elemToIndex = new Map<any, number>();

  render() {
    this.model.on('change', this.changed_prop, this);

    this.updateProps(this.stateToProps());
  }

  private changeSelection = (s: ISetLike<any> | null) => {
    this.model.set(
      'value',
      s
        ? {
            name: s.name,
            elems: s.elems.map((e) => this.elemToIndex.get(e)),
          }
        : null
    );
  };

  private stateToProps(): Partial<UpSetProps<any>> {
    const props: Partial<UpSetProps<any>> = {};
    const state = this.model.get_state(true);

    const toCamelCase = (v: string) => v.replace(/([-_]\w)/g, (g) => g[1].toUpperCase());

    Object.keys(state).forEach((key) => {
      let v = state[key] as any;
      if (key.startsWith('_') || key === 'layout') {
        return;
      }
      const propName = key === 'value' ? 'selection' : toCamelCase(key);
      if (propName === 'fontSizes' || propName === 'combinations') {
        const converted: any = {};
        Object.keys(v).forEach((key: string) => {
          converted[toCamelCase(key)] = (v as any)![key];
        });
        v = converted;
      }
      (props as any)[propName] = v;
    });
    return props;
  }

  private updateProps(delta: any) {
    if (delta) {
      Object.assign(this.props, delta);
    }
    this.fixProps(delta);
    this.renderImpl();
  }

  private fixProps(delta: any) {
    const props = this.props;

    if (delta.elems != null) {
      this.elems = delta.elems;
      this.elemToIndex.clear();
      this.elems.forEach((e, i) => this.elemToIndex.set(e, i));
    }

    if (delta.sets != null) {
      props.sets = fixSets(props.sets, this.elems);
    }
    if (delta.combinations != null) {
      const c = fixCombinations(props.combinations, props.sets, this.elems);
      if (c == null) {
        delete props.combinations;
      } else {
        props.combinations = c;
      }
    }
    if ((delta.selection && typeof delta.selection.name === 'string') || Array.isArray(delta.selection)) {
      props.selection = resolveSet(
        Array.isArray(delta.selection) ? delta.selection : delta.selection.name,
        props.sets,
        props.combinations as ISetCombinations<any>
      );
    }
    if (delta.queries) {
      props.queries!.forEach((query) => {
        if (isSetQuery(query) && (typeof query.set === 'string' || Array.isArray(query.set))) {
          query.set = resolveSet(query.set, props.sets, props.combinations as ISetCombinations<any>)!;
        } else if (isElemQuery(query)) {
          query.elems = Array.from(query.elems).map((i) => this.elems[i]);
        }
      });
    }

    if (this.model.get('mode') === 'click') {
      props.onClick = this.changeSelection;
      delete props.onHover;
    } else {
      props.onHover = this.changeSelection;
      delete props.onClick;
    }
  }

  private changed_prop(evt: any) {
    console.log(evt);
  }

  private renderImpl() {
    const bb = this.el.getBoundingClientRect();

    if (!bb.width || !bb.height) {
      requestAnimationFrame(() => {
        const bb2 = this.el.getBoundingClientRect();
        this.props.width = bb2.width || 600;
        this.props.height = bb2.height || 400;
        renderUpSet(this.el, this.props);
      });
      return;
    }
    this.props.width = bb.width;
    this.props.height = bb.height;
    renderUpSet(this.el, this.props);
  }
}
