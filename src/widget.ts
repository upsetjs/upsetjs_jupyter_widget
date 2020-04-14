// Copyright (c) Samuel Gratzl

import { DOMWidgetModel, DOMWidgetView, ISerializers } from '@jupyter-widgets/base';

import { MODULE_VERSION, MODULE_NAME } from './version';
import {
  isElemQuery,
  ISetCombinations,
  ISetLike,
  isSetQuery,
  renderUpSet,
  UpSetProps,
  UpSetQuery,
} from '@upsetjs/bundle';
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
    this.model.off('change', this.changed_prop, null);
    if (!s) {
      this.model.set('value', null);
    } else {
      const setish: any = {
        name: s.name,
        type: s.type,
        cardinality: s.cardinality,
        elems: s.elems.map((e) => this.elemToIndex.get(e)),
      };
      if (s.type !== 'set') {
        setish.degree = s.degree;
        setish.set_names = Array.from(s.sets).map((s) => s.name);
      }
      this.model.set('value', setish);
    }
    this.props.selection = s;
    this.renderImpl();
    this.touch();
    this.model.on('change', this.changed_prop, this);
  };

  private stateToProps(): Partial<UpSetProps<any>> {
    const props: Partial<UpSetProps<any>> = {};
    const state = this.model.get_state(true);

    const toCamelCase = (v: string) => v.replace(/([-_]\w)/g, (g) => g[1].toUpperCase());

    const toPropName = (key: string) => {
      if (key === 'value') {
        return 'selection';
      }
      if (key.startsWith('_')) {
        return toCamelCase(key.slice(1));
      }
      return toCamelCase(key);
    };

    Object.keys(state).forEach((key) => {
      let v = state[key] as any;
      if (
        v == null ||
        (Array.isArray(v) && v.length === 0) ||
        (key.startsWith('_') && key !== '_queries' && key !== '_sets') ||
        key === 'layout'
      ) {
        return;
      }
      const propName = toPropName(key);
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
    if (delta.selection) {
      props.selection = resolveSet(
        delta.selection,
        props.sets,
        props.combinations as ISetCombinations<any>,
        this.elems
      );
    }
    if (delta.queries) {
      props.queries = delta.queries.map((query: UpSetQuery<any>) => {
        if (isSetQuery(query)) {
          return Object.assign({}, query, {
            set: resolveSet(query.set, props.sets, props.combinations as ISetCombinations<any>, this.elems)!,
          });
        } else if (isElemQuery(query)) {
          return Object.assign({}, query, {
            elems: Array.from(query.elems).map((i) => this.elems[i]),
          });
        }
        return query;
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

  private changed_prop(model: any, options: any) {
    console.log(model, options);
  }

  private renderImpl() {
    const bb = this.el.getBoundingClientRect();
    const p = Object.assign({}, this.props);

    if (!bb.width || !bb.height) {
      requestAnimationFrame(() => {
        const bb2 = this.el.getBoundingClientRect();
        p.width = bb2.width || 600;
        p.height = bb2.height || 400;
        renderUpSet(this.el, p);
      });
      return;
    }
    p.width = bb.width;
    p.height = bb.height;
    renderUpSet(this.el, p);
  }
}
