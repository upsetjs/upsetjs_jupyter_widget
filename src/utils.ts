/**
 * @upsetjs/jupyter_widget
 * https://github.com/upsetjs/upsetjs_jupyter_widget
 *
 * Copyright (c) 2020 Samuel Gratzl <sam@sgratzl.com>
 */

import {
  asSets,
  asCombinations,
  generateCombinations,
  GenerateSetCombinationsOptions,
  ISetCombinations,
  ISets,
  fromIndicesArray,
} from '@upsetjs/bundle';

export interface IElem {
  name: string;
  attrs: { [key: string]: number };
}

export function fixSets(sets: ISets<any>, elems: IElem[]) {
  if (!sets) {
    return [];
  }
  return asSets(
    sets.map((set) =>
      Object.assign({}, set, {
        elems: fromIndicesArray(set.elems, elems),
      })
    )
  );
}

export function fixCombinations(
  combinations: GenerateSetCombinationsOptions | ISetCombinations<any> | undefined,
  sets: ISets<IElem>,
  elems: IElem[]
) {
  if (!combinations) {
    return null;
  }
  if (!Array.isArray(combinations)) {
    return generateCombinations(
      sets,
      Object.assign(
        {
          elems,
        },
        combinations as GenerateSetCombinationsOptions
      )
    );
  }
  const lookup = new Map(sets.map((s) => [s.name, s]));
  return asCombinations(
    combinations.map((set) =>
      Object.assign({}, set, {
        elems: fromIndicesArray(set.elems, elems),
      })
    ),
    'composite',
    (s: any) => s.set_names.map((si: string) => lookup.get(si)).filter(Boolean)
  );
}

export function resolveSet(
  set: number[] | { name: string; type: string },
  sets: ISets<IElem>,
  combinations: ISetCombinations<IElem>,
  elems: IElem[]
) {
  if (Array.isArray(set)) {
    return set.map((i) => elems[i]);
  }
  const ss: { name: string; type: string } = set;
  if (!ss.type || ss.type === 'set') {
    const s = sets.find((s) => s.name === ss.name);
    if (s) {
      return s;
    }
  }
  return combinations.find((c) => c.name === ss.name);
}
