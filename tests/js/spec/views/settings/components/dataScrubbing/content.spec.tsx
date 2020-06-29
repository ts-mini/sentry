import React from 'react';

import {mountWithTheme} from 'sentry-test/enzyme';

import Content from 'app/views/settings/components/dataScrubbing/content';
import {
  Rule,
  RuleType,
  MethodType,
} from 'app/views/settings/components/dataScrubbing/types';

const rules: Array<Rule> = [
  {
    id: 0,
    method: MethodType.MASK,
    type: RuleType.CREDITCARD,
    source: '$message',
  },
  {
    id: 1,
    method: MethodType.REPLACE,
    placeholder: 'Scrubbed',
    type: RuleType.PASSWORD,
    source: 'password',
  },
];

const handleEditRule = jest.fn();
const handleDelete = jest.fn();

describe('Content', () => {
  it('default render - empty', () => {
    const wrapper = mountWithTheme(
      <Content rules={[]} onEditRule={handleEditRule} onDeleteRule={handleDelete} />
    );
    expect(wrapper.text()).toEqual('You have no data scrubbing rules');
    expect(wrapper).toMatchSnapshot();
  });

  it('render rules', () => {
    const wrapper = mountWithTheme(
      <Content rules={rules} onEditRule={handleEditRule} onDeleteRule={handleDelete} />
    );
    expect(wrapper.find('List')).toHaveLength(1);
    expect(wrapper).toMatchSnapshot();
  });
});
