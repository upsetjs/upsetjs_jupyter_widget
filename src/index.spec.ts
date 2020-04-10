// import // Add any needed widget imports here (or from controls)
// '@jupyter-widgets/base';

import { createTestModel } from './__tests__/utils';

import { UpSetModel } from '.';

describe('UpSet', () => {
  describe('UpSetModel', () => {
    it('should be createable', () => {
      let model = createTestModel(UpSetModel);
      expect(model).toBeInstanceOf(UpSetModel);
      expect(model.get('value')).toBeUndefined();
    });

    // it('should be createable with a value', () => {
    //   let state = { value: 'Foo Bar!' };
    //   let model = createTestModel(UpSetModel, state);
    //   expect(model).toBeInstanceOf(UpSetModel);
    //   expect(model.get('value')).toBe('Foo Bar!');
    // });
  });
});
