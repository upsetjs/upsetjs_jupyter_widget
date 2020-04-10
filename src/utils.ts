import {
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
    sets.map((set) =>
      Object.assign({}, set, {
        elems: set.elems.map((i) => elems[i]),
      })
    )
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
    combinations.map((set) =>
      Object.assign({}, set, {
        elems: set.elems.map((i: number) => elems[i]),
      })
    ),
    'composite',
    (s: any) => s.set_names.map((si: string) => lookup.get(si)).filter(Boolean)
  );
}

export function resolveSet(
  set: number[] | { name: string; type: string },
  sets: ISets<any>,
  combinations: ISetCombinations<any>,
  elems: any[]
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
