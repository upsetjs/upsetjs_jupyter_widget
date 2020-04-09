import {
  ISetLike,
  ISetCombination,
  asSets,
  asCombinations,
  generateCombinations,
  GenerateSetCombinationsOptions,
  ISetCombinations,
  ISets,
} from '@upsetjs/bundle';

export function fixSets(sets: ISets<any>, elems: any[]) {
  if (!sets) {
    return [];
  }
  return asSets(
    sets.map((set) => {
      (set as any).elems = set.elems.map((i) => elems[i]);
      return set;
    })
  );
}

export function fixCombinations(
  combinations: GenerateSetCombinationsOptions | ISetCombinations<any> | undefined,
  sets: ISets<any>,
  elems: any[]
) {
  if (!combinations || (Array.isArray(combinations) && combinations.length === 0)) {
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
    combinations.map((set) => {
      (set as any).elems = set.elems.map((i: number) => elems[i]);
      return set;
    }),
    'composite',
    (s: any) => s.set_names.map((si: string) => lookup.get(si)).filter(Boolean)
  );
}

function toUnifiedCombinationName(c: ISetCombination<any>) {
  return Array.from(c.sets)
    .map((s) => s.name)
    .sort()
    .join('&');
}

export function resolveSet(set: string | string[], sets: ISets<any>, combinations: ISetCombinations<any>) {
  const s = sets.find((s) => s.name === set);
  if (s) {
    return s;
  }
  const combinedNames = Array.isArray(set) ? set.slice().sort().join('&') : null;
  return combinations.find((c) => {
    return c.name === set || (combinedNames && combinedNames === toUnifiedCombinationName(c));
  });
}

export function resolveSetByElems(elems: ReadonlyArray<any>, sets: ISets<any>, combinations: ISetCombinations<any>) {
  const set = new Set(elems);
  const sameElems = (s: ISetLike<any>) => {
    if (!s.elems || s.elems.length !== set.size) {
      return false;
    }
    return s.elems.every((v) => set.has(v));
  };

  const r = sets.find(sameElems);
  if (r) {
    return r;
  }
  return combinations.find(sameElems);
}
