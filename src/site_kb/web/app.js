(() => {
  const form = document.querySelector('#filters');
  if (!form) return;
  const search = document.querySelector('#search');
  const ids = ['network', 'country', 'origin', 'variables'];
  const controls = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));
  const cards = [...document.querySelectorAll('.site-card')];
  const params = new URLSearchParams(location.search);
  search.value = params.get('q') || '';
  ids.forEach(id => {
    if (id === 'variables') controls[id].checked = params.get(id) === '1';
    else controls[id].value = params.get(id) || '';
  });
  function update() {
    const words = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      const d = card.dataset;
      const visible = words.every(word => d.search.includes(word)) &&
        (!controls.network.value || JSON.parse(d.networks).includes(controls.network.value)) &&
        (!controls.country.value || d.country === controls.country.value) &&
        (!controls.origin.value || d.origin === controls.origin.value) &&
        (!controls.variables.checked || d.variables === 'true');
      card.hidden = !visible;
      count += Number(visible);
    });
    document.getElementById('result-count').textContent = `${count} of ${cards.length} sites`;
    document.getElementById('empty').hidden = count !== 0;
    const state = new URLSearchParams();
    if (search.value) state.set('q', search.value);
    ids.forEach(id => {
      const value = id === 'variables' ? (controls[id].checked ? '1' : '') : controls[id].value;
      if (value) state.set(id, value);
    });
    history.replaceState(null, '', location.pathname + (state.size ? '?' + state : ''));
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('change', update);
  search.addEventListener('input', update);
  form.addEventListener('reset', () => { search.value = ''; setTimeout(update, 0); });
  document.getElementById('clear-search').addEventListener('click', () => form.reset());
  update();
})();
