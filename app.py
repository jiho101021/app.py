from flask import Flask, render_template_string

app = Flask(__name__)

html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Goal Kings</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-6">

  <div class="max-w-4xl mx-auto">
    <h1 id="title" class="text-3xl font-bold mb-2">Goal Kings</h1>
    <p id="subtitle" class="text-gray-600 mb-6">역대 축구 선수 득점 순위</p>

    <div class="mb-4">
      <select id="lang" onchange="changeLang()" class="border p-2 rounded">
        <option value="ko">한국어</option>
        <option value="en">English</option>
        <option value="es">Español</option>
        <option value="ja">日本語</option>
      </select>
    </div>

    <input type="text" id="search" placeholder="선수 검색" 
           onkeyup="filter()" class="w-full p-3 border rounded mb-6">

    <table class="w-full border-collapse bg-white shadow">
      <thead>
        <tr class="bg-gray-800 text-white">
          <th id="th-rank" class="p-3 text-left">순위</th>
          <th id="th-player" class="p-3 text-left">선수</th>
          <th id="th-goals" class="p-3 text-right">득점</th>
        </tr>
      </thead>
      <tbody id="table-body"></tbody>
    </table>
  </div>

  <script>
    let players = [
      {rank:1, name:"Cristiano Ronaldo", goals:970},
      {rank:2, name:"Lionel Messi", goals:910},
      {rank:3, name:"Robert Lewandowski", goals:697},
      {rank:4, name:"Luis Suarez", goals:599},
      {rank:5, name:"Harry Kane", goals:480},
      {rank:6, name:"Karim Benzema", goals:480},
      {rank:7, name:"Mohamed Salah", goals:380},
      {rank:8, name:"Kylian Mbappe", goals:320}
    ];

    const langData = {
      ko: { title: "Goal Kings", subtitle: "역대 축구 선수 득점 순위", search: "선수 검색", rank: "순위", player: "선수", goals: "득점" },
      en: { title: "Goal Kings", subtitle: "All-Time Top Goal Scorers", search: "Search player", rank: "Rank", player: "Player", goals: "Goals" },
      es: { title: "Reyes de Goles", subtitle: "Máximos Goleadores", search: "Buscar jugador", rank: "Posición", player: "Jugador", goals: "Goles" },
      ja: { title: "Goal Kings", subtitle: "歴代得点ランキング", search: "選手検索", rank: "順位", player: "選手", goals: "得点" }
    };

    function renderTable(filteredPlayers) {
      const tbody = document.getElementById('table-body');
      tbody.innerHTML = filteredPlayers.map(p => `
        <tr class="border-b hover:bg-gray-50">
          <td class="p-3">${p.rank}</td>
          <td class="p-3 font-medium">${p.name}</td>
          <td class="p-3 text-right font-bold">${p.goals}</td>
        </tr>
      `).join('');
    }

    function filter() {
      const term = document.getElementById('search').value.toLowerCase();
      const filtered = players.filter(p => p.name.toLowerCase().includes(term));
      renderTable(filtered);
    }

    function changeLang() {
      const lang = document.getElementById('lang').value;
      const t = langData[lang];
      
      document.getElementById('title').textContent = t.title;
      document.getElementById('subtitle').textContent = t.subtitle;
      document.getElementById('search').placeholder = t.search;
      document.getElementById('th-rank').textContent = t.rank;
      document.getElementById('th-player').textContent = t.player;
      document.getElementById('th-goals').textContent = t.goals;
    }

    renderTable(players);
  </script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
