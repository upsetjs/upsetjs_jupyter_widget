/**
 * @upsetjs/jupyter_widget
 * https://github.com/upsetjs/upsetjs_jupyter_widget
 *
 * Copyright (c) 2021 Samuel Gratzl <sam@sgratzl.com>
 */

import { DOMWidgetModel, DOMWidgetView, ISerializers } from '@jupyter-widgets/base';

import { MODULE_VERSION, MODULE_NAME } from './version';
import {
  isElemQuery,
  ISetCombinations,
  ISetLike,
  isSetQuery,
  render,
  UpSetProps,
  UpSetQuery,
  boxplotAddon,
  fromIndicesArray,
  VennDiagramProps,
  renderVennDiagram,
  renderKarnaughMap,
  KarnaughMapProps,
  categoricalAddon,
  createVennJSAdapter,
  ISets,
} from '@upsetjs/bundle';
import { layout } from '@upsetjs/venn.js';
import { fixCombinations, fixSets, resolveSet, IElem, fromExpression } from './utils';

const adapter = createVennJSAdapter(layout);

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

declare type UpSetNumericAttrSpec = {
  type: 'number';
  name: string;
  domain: [number, number];
  values: ReadonlyArray<number>;
  elems?: ReadonlyArray<string>;
};
declare type UpSetCategoricalAttrSpec = {
  type: 'categorical';
  name: string;
  categories: ReadonlyArray<string>;
  values: ReadonlyArray<string>;
  elems?: ReadonlyArray<string>;
};

declare type UpSetAttrSpec = UpSetNumericAttrSpec | UpSetCategoricalAttrSpec;

export class UpSetView extends DOMWidgetView {
  private props: UpSetProps<IElem> & VennDiagramProps<IElem> = {
    sets: [],
    width: 300,
    height: 300,
  };
  private elems: IElem[] = [];
  private readonly elemToIndex = new Map<IElem, number>();
  private attrs: UpSetAttrSpec[] = [];

  render() {
    this.model.on('change', this.changed_prop, this);

    this.updateProps(this.stateToProps());
  }

  private changeSelection = (s: ISetLike<IElem> | null) => {
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

  private stateToProps(): Partial<UpSetProps<any> & VennDiagramProps<any> & KarnaughMapProps<any>> {
    const props: Partial<UpSetProps<any> & VennDiagramProps<any> & KarnaughMapProps<any>> = {};
    const state = this.model.get_state(true);

    const toCamelCase = (v: string) => v.replace(/([-_]\w)/g, (g) => g[1].toUpperCase());

    const toPropName = (key: string) => {
      if (key === 'value') {
        return 'selection';
      }
      return toCamelCase(key);
    };

    Object.keys(state).forEach((key) => {
      let v = state[key] as any;
      if (v == null || (Array.isArray(v) && v.length === 0) || key.startsWith('_') || key === 'layout') {
        return;
      }
      const propName = toPropName(key);
      if (propName === 'fontSizes') {
        const converted: any = {};
        Object.keys(v).forEach((key: string) => {
          const vi = (v as any)![key];
          if (vi != null) {
            converted[toCamelCase(key)] = typeof vi === 'number' ? `${vi}px` : String(vi);
          }
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

  private syncAddons() {
    if (this.attrs.length === 0) {
      delete this.props.setAddons;
      delete this.props.combinationAddons;
      return;
    }
    const toAddon = (attr: UpSetAttrSpec, vertical = false) => {
      if (attr.type === 'number') {
        return boxplotAddon<IElem>(
          (v) => v.attrs[attr.name] as number,
          { min: attr.domain[0], max: attr.domain[1] },
          {
            name: attr.name,
            quantiles: 'hinges',
            orient: vertical ? 'vertical' : 'horizontal',
          }
        );
      }
      return categoricalAddon<IElem>(
        (v) => v.attrs[attr.name] as string,
        {
          categories: attr.categories,
        },
        {
          name: attr.name,
          orient: vertical ? 'vertical' : 'horizontal',
        }
      );
    };
    this.props.setAddons = this.attrs.map((attr) => toAddon(attr, false));
    this.props.combinationAddons = this.attrs.map((attr) => toAddon(attr, true));
  }

  private fixProps(delta: any) {
    const props = this.props;
    if (delta.elems)
      if (delta.elems != null) {
        this.attrs = delta.attrs ?? this.attrs;
        const lookups = this.attrs.map((attr) => (attr.elems ? new Map(attr.elems.map((e, i) => [e, i])) : null));
        this.elems = (delta.elems as any[]).map((name, i) => {
          const attrs: any = {};
          this.attrs.forEach(
            (attr, j) => (attrs[attr.name] = attr.values[lookups[j] ? lookups[j]!.get(name) ?? i : i])
          );
          return { name, attrs };
        });
        this.elemToIndex.clear();
        this.elems.forEach((e, i) => this.elemToIndex.set(e, i));
        this.syncAddons();
      } else if (delta.attrs != null) {
        // only attrs same elems
        this.attrs = delta.attrs;
        const lookups = this.attrs.map((attr) => (attr.elems ? new Map(attr.elems.map((e, i) => [e, i])) : null));
        this.elems.forEach((elem, i) => {
          const attrs: any = {};
          this.attrs.forEach(
            (attr, j) => (attrs[attr.name] = attr.values[lookups[j] ? lookups[j]!.get(elem.name) ?? i : i])
          );
          elem.attrs = attrs;
        });
        this.syncAddons();
      }
    delete (this.props as any).elems;
    delete (this.props as any).attrs;

    if (delta.sets != null) {
      props.sets = fixSets(delta.sets, this.elems);
    }
    if (delta.combinations != null) {
      if (this.model.get('_expression_data')) {
        const r = fromExpression(delta.combinations);
        props.combinations = r.combinations as ISetCombinations<IElem>;
        props.sets = r.sets as ISets<IElem>;
      } else {
        const c = fixCombinations(delta.combinations, props.sets, this.elems);
        if (c == null) {
          delete props.combinations;
        } else {
          props.combinations = c;
        }
      }
    }
    if (delta.selection) {
      props.selection = resolveSet(
        delta.selection,
        props.sets ?? [],
        (props.combinations ?? []) as ISetCombinations<IElem>,
        this.elems
      );
    }
    if (delta.queries) {
      props.queries = delta.queries.map((query: UpSetQuery<any>) => {
        if (isSetQuery(query)) {
          return Object.assign({}, query, {
            set: resolveSet(
              query.set,
              props.sets ?? [],
              (props.combinations ?? []) as ISetCombinations<IElem>,
              this.elems
            )!,
          });
        } else if (isElemQuery(query)) {
          return Object.assign({}, query, {
            elems: fromIndicesArray(query.elems as any[], this.elems),
          });
        }
        return query;
      });
    }

    delete props.onHover;
    delete props.onClick;
    delete props.onContextMenu;
    if (this.model.get('mode') === 'click') {
      props.onClick = this.changeSelection;
    } else if (this.model.get('mode') === 'hover') {
      props.onHover = this.changeSelection;
    } else if (this.model.get('mode') === 'contextMenu') {
      props.onContextMenu = this.changeSelection;
    }
  }

  private changed_prop(model: any) {
    this.updateProps(model.changed);
  }

  private renderImpl() {
    const bb = this.el.getBoundingClientRect();
    const p = Object.assign({}, this.props);
    const renderMode = this.model.get('_render_mode');

    const renderComponent = () => {
      if (renderMode === 'venn') {
        delete p.layout;
        renderVennDiagram(this.el, p);
      } else if (renderMode === 'euler') {
        p.layout = adapter;
        renderVennDiagram(this.el, p);
      } else if (renderMode === 'kmap') {
        renderKarnaughMap(this.el, p);
      } else {
        render(this.el, p);
      }
    };

    if (!bb.width || !bb.height) {
      requestAnimationFrame(() => {
        const bb2 = this.el.getBoundingClientRect();
        p.width = bb2.width || 600;
        p.height = bb2.height || 400;
        renderComponent();
      });
      return;
    }
    p.width = bb.width;
    p.height = bb.height;
    renderComponent();
  }
}
