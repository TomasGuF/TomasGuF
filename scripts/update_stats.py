"""Generate profile cards from GitHub's public data using the standard library."""

import json
import os
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
COLORS = ['#abd4c4', '#95cdf6', '#b98bc5', '#87b3a5', '#6b839d', '#7d3b94', '#e9f0ee']


def github(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'TomasGuF-profile'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    request = Request('https://api.github.com' + path, headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def svg_frame(title, content, date, height=272, width=580):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="6" fill="#28303d" stroke="#4c6264"/>
<text x="28" y="35" fill="#abd4c4" font-size="17" font-weight="700" font-family="Arial, DejaVu Sans, sans-serif">{escape(title)}</text>
<path d="M28 51H{width-28}" stroke="#4c6264"/>
{content}
<text x="28" y="{height-18}" fill="#c0d0ce" font-size="11" font-family="DejaVu Sans, sans-serif">Datos públicos · {escape(date)}</text>
</svg>'''


def stats_card(user, repos, date):
    metrics = [
        (len(repos), 'Repositorios propios'),
        (sum(repo.get('stargazers_count', 0) for repo in repos), 'Estrellas recibidas'),
        (user.get('followers', 0), 'Seguidores'),
        (sum(repo.get('forks_count', 0) for repo in repos), 'Forks recibidos'),
    ]
    parts = []
    for index, (value, label) in enumerate(metrics):
        x = 28 + index * 209
        y = 103
        parts.append(f'<text x="{x}" y="{y}" fill="#e9f0ee" font-size="33" font-weight="700" font-family="Arial, DejaVu Sans, sans-serif">{value:,}</text>')
        parts.append(f'<text x="{x}" y="{y+24}" fill="#c0d0ce" font-size="13" font-family="DejaVu Sans, sans-serif">{escape(label)}</text>')
        if index:
            parts.append(f'<path d="M{x-18} 76V128" stroke="#4c6264"/>')
    return svg_frame('Actividad pública', '\n'.join(parts), date, height=170, width=860)


def languages_card(languages, date):
    total = sum(languages.values())
    if not total:
        content = '''<text x="28" y="101" fill="#d4d8d5" font-size="17" font-family="DejaVu Sans, sans-serif">Aún no hay código público propio</text>
<text x="28" y="131" fill="#a1a6a7" font-size="15" font-family="DejaVu Sans, sans-serif">para calcular esta distribución.</text>
<text x="28" y="179" fill="#b0b5b2" font-size="13" font-family="DejaVu Sans, sans-serif">Mis conocimientos están en la sección de tecnologías.</text>'''
        return svg_frame('Lenguajes', content, date)
    top = languages.most_common(6)
    remaining = total - sum(value for _, value in top)
    if remaining:
        top.append(('Otros', remaining))
    x = 28.0
    parts = []
    for i, (language, value) in enumerate(top):
        width = value / total * 524
        parts.append(f'<rect x="{x:.2f}" y="72" width="{width:.2f}" height="12" fill="{COLORS[i]}"/>')
        x += width
        lx = 28 + (i % 2) * 278
        ly = 118 + (i // 2) * 30
        parts.append(f'<circle cx="{lx+4}" cy="{ly-5}" r="4" fill="{COLORS[i]}"/>')
        label = f'{language} {value / total * 100:.1f}%'
        parts.append(f'<text x="{lx+17}" y="{ly}" fill="#d4d8d5" font-size="13" font-family="DejaVu Sans, sans-serif">{escape(label)}</text>')
    parts.append('<text x="28" y="229" fill="#a1a6a7" font-size="11" font-family="DejaVu Sans, sans-serif">Proporción de bytes de código. Excluye forks y este perfil.</text>')
    return svg_frame('Lenguajes', '\n'.join(parts), date)


def main():
    username = os.environ.get('PROFILE_USERNAME', 'TomasGuF')
    if username != 'TomasGuF':
        raise ValueError('This profile is configured for TomasGuF')
    user = github('/users/' + quote(username, safe=''))
    public = []
    page = 1
    while True:
        batch = github(f'/users/{quote(username, safe="")}/repos?type=owner&per_page=100&page={page}')
        public.extend(repo for repo in batch if not repo.get('private') and not repo.get('fork'))
        if len(batch) < 100:
            break
        page += 1
    languages = Counter()
    for repo in public:
        if repo['name'].lower() == username.lower():
            continue
        languages.update(github('/repos/' + repo['full_name'] + '/languages'))
    assets = ROOT / 'assets'
    assets.mkdir(exist_ok=True)
    date = datetime.now(timezone.utc).strftime('%Y-%m-%d UTC')
    (assets / 'github-stats.svg').write_text(stats_card(user, public, date), encoding='utf-8')
    (assets / 'languages.svg').write_text(languages_card(languages, date), encoding='utf-8')
    print(f'Updated public profile cards for {username}; {len(public)} repositories')


if __name__ == '__main__':
    main()
