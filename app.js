const status = m => document.getElementById('status').textContent = m;

function fill(selector, rows) {
  document.querySelector(selector + ' tbody').innerHTML =
    rows.map(r => '<tr>' + r.map(c => `<td>${c ?? ''}</td>`).join('') + '</tr>').join('');
}

function render(p) {
  document.getElementById('results').hidden = false;
  document.getElementById('r-name').textContent = p.name;
  document.getElementById('r-rows').textContent = p.rows.toLocaleString();
  document.getElementById('r-cols').textContent = p.columns_count;

  fill('#t-columns', p.columns.map(c => [c.name, c.kind, `${c.missing} (${c.missing_pct}%)`, c.unique]));
  fill('#t-numeric', p.numeric_summary.map(s => [s.column, s.mean, s.median, s.std, s.min, s.max]));
  fill('#t-corr', p.correlations.slice(0, 10).map(c => [c.a, c.b, c.r]));

  document.querySelector('#t-preview thead').innerHTML =
    '<tr>' + p.headers.map(h => `<th>${h}</th>`).join('') + '</tr>';
  fill('#t-preview', p.preview);
}

async function analyze(file) {
  const fd = new FormData();
  fd.append('file', file);
  status('Analyzing...');
  const res = await fetch('/api/profile', { method: 'POST', body: fd });
  const data = await res.json();
  if (!res.ok) { status('Error: ' + (data.error || res.status)); return; }
  status('');
  render(data);
}

document.getElementById('analyze').addEventListener('click', () => {
  const f = document.getElementById('file').files[0];
  if (!f) { status('Choose a CSV file first.'); return; }
  analyze(f);
});

document.getElementById('sample').addEventListener('click', async () => {
  status('Loading sample...');
  const res = await fetch('/api/sample');
  const data = await res.json();
  status('');
  render(data);
});
