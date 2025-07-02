const API = 'http://127.0.0.1:5000/api';

document.addEventListener('DOMContentLoaded', () => {
  renderArtistBar();
  renderGenrePie();
  renderAboveAvg();
  renderPlaylistTable();
});


async function renderArtistBar() {
  // 1. chama a API (Consulta 1)
  const res   = await fetch(`${API}/artists/popularity`);
  const dados = await res.json();              // [{artist:"...", avg_popularity:87}, …]

  // 2. separa rótulos e valores
  const labels = dados.map(r => r.artist);
  const values = dados.map(r => r.avg_popularity);

  // 3. cria / reaproveita o <canvas>
  const ctx = document.getElementById('chartArtists').getContext('2d');

  // 4. instancia o Chart.js
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Popularidade média',
        data:  values,
        backgroundColor: 'rgba(32,212,112,0.7)',
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { y: { beginAtZero: true } }
    }
  });
}

async function renderGenrePie() {
  const res   = await fetch(`${API}/genres/playlists`);
  const dados = await res.json();              // [{genre:"pop", n_playlists:123}, …]

  const labels = dados.map(r => r.genre);
  const values = dados.map(r => r.n_playlists);

  const ctx = document.getElementById('chartGenres').getContext('2d');

  new Chart(ctx, {
    type: 'pie',       // troque para 'bar' + indexAxis:'y' se preferir barra horizontal
    data: {
      labels,
      datasets: [{ data: values }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      // extra: cores automáticas
      plugins: { legend: { position: 'bottom' } }
    }
  });
}

async function renderAboveAvg() {
  const res   = await fetch(`${API}/artists/above-average`);
  const dados = await res.json();              // [{artist:"...", avg_popularity:70}, …]

  const ul = document.getElementById('listAboveAvg');
  ul.innerHTML = '';                           // limpa conteúdo anterior

  dados.forEach(row => {
    const li = document.createElement('li');
    li.textContent = `${row.artist} (${row.avg_popularity})`;
    ul.appendChild(li);
  });
}

async function renderPlaylistTable() {
  const res   = await fetch(`${API}/playlists/albumcount`);
  const dados = await res.json();              // [{playlist:"Morning Run", n_albums:42}, …]

  const tbody = document
      .getElementById('tblPlaylistAlbums')
      .querySelector('tbody');

  tbody.innerHTML = '';                        // limpa conteúdo anterior

  dados.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
       <td>${row.playlist}</td>
       <td style="text-align:right">${row.n_albums}</td>`;
    tbody.appendChild(tr);
  });
}
