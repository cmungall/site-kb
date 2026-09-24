const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const code = fs.readFileSync('src/site_kb/web/app.js', 'utf8');

function load(query = '') {
  const elements = {};
  for (const id of ['filters', 'search', 'network', 'country', 'origin', 'variables', 'result-count', 'empty', 'clear-search']) {
    elements[id] = {value: '', checked: false, handlers: {}, addEventListener(name, fn) { this.handlers[name] = fn; }};
  }
  elements.filters.reset = () => {
    for (const id of ['network', 'country', 'origin']) elements[id].value = '';
    elements.variables.checked = false;
    elements.filters.handlers.reset();
  };
  const cards = [
    {dataset: {search: 'forest neon carbon', networks: '["NEON","DEIMS"]', country: 'United States', origin: 'Imported', variables: 'false'}},
    {dataset: {search: 'ottawa ropec influenza rna', networks: '[]', country: 'Not recorded', origin: 'Curated', variables: 'true'}}
  ];
  const context = {URLSearchParams, location: {pathname: '/site-kb/index.html', search: query}, history: {replaceState(...args) { context.url = args[2]; }}, setTimeout: fn => fn(), document: {querySelector: s => elements[s.slice(1)], getElementById: s => elements[s], querySelectorAll: () => cards}};
  vm.runInNewContext(code, context);
  return {elements, cards, context, update: elements.search.handlers.input};
}

test('deep links restore search and measured-variable filter', () => {
  const {elements, cards, context} = load('?q=influenza&variables=1');
  assert.equal(cards[0].hidden, true);
  assert.equal(cards[1].hidden, false);
  assert.equal(elements['result-count'].textContent, '1 of 2 sites');
  assert.equal(context.url, '/site-kb/index.html?q=influenza&variables=1');
});

test('combined filters match any network membership and reset empty results', () => {
  const {elements, cards, update} = load();
  elements.network.value = 'DEIMS';
  elements.country.value = 'United States';
  update();
  assert.equal(cards[0].hidden, false);
  assert.equal(cards[1].hidden, true);
  elements.search.value = 'RNA';
  update();
  assert.equal(elements.empty.hidden, false);
  elements['clear-search'].handlers.click();
  assert.equal(elements.empty.hidden, true);
  assert.equal(cards.every(card => !card.hidden), true);
});
