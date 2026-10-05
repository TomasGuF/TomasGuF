"""Build the profile's reference-style SVG assets from verified icon sources."""

from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)


def save(path, body, width, height, label):
    target = ASSETS / path
    target.parent.mkdir(exist_ok=True)
    target.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}">'
        f'<title>{escape(label)}</title>{body}</svg>', encoding='utf-8')


sources = json.loads((ROOT / 'icon-sources.json').read_text(encoding='utf-8'))
icons = [
    ('CS.svg', 'C#'), ('Java-Dark.svg', 'Java'), ('Python-Dark.svg', 'Python'),
    ('C.svg', 'C'), ('DotNet.svg', '.NET'), ('Angular-Dark.svg', 'Angular'),
    ('React-Dark.svg', 'React'), ('NodeJS-Dark.svg', 'Node.js'),
    ('ExpressJS-Dark.svg', 'Express'), ('PostgreSQL-Dark.svg', 'PostgreSQL'),
    ('SQLite.svg', 'SQLite'), ('Kafka.svg', 'Apache Kafka'), ('Git.svg', 'Git'),
    ('Github-Dark.svg', 'GitHub'), ('Figma-Dark.svg', 'Figma'),
]
parts = []
for index, (name, label) in enumerate(icons):
    attrs, inner = re.search(r'<svg\b([^>]*)>(.*)</svg>', sources[name], re.S).groups()
    match = re.search(r'viewBox="([^"]+)"', attrs)
    viewbox = match.group(1) if match else '0 0 256 256'
    for identifier in sorted(re.findall(r'\bid="([^"]+)"', inner), key=len, reverse=True):
        new_id = f'tech{index}-{identifier}'
        inner = inner.replace(f'id="{identifier}"', f'id="{new_id}"')
        inner = inner.replace(f'url(#{identifier})', f'url(#{new_id})')
        inner = inner.replace(f'href="#{identifier}"', f'href="#{new_id}"')
    row, col = divmod(index, 8)
    x = col * 60 + (30 if row else 0)
    parts.append(f'<svg x="{x}" y="{row*60}" width="50" height="50" viewBox="{viewbox}"><title>{escape(label)}</title>{inner}</svg>')
save('tech-stack.svg', ''.join(parts), 470, 110, ', '.join(label for _, label in icons))
(ASSETS / 'skill-icons-LICENSE.txt').write_text(sources['LICENSE'], encoding='utf-8')

font = 'Arial, DejaVu Sans, sans-serif'
save('header.svg', f'''
<rect width="1200" height="238" rx="8" fill="#161b1d"/>
<path d="M44 44H108" stroke="#8fae9b" stroke-width="3"/>
<text x="44" y="104" font-family="{font}" font-size="47" font-weight="700" fill="#eff1ef">Tomás Guerra Fuentes</text>
<text x="46" y="145" font-family="{font}" font-size="20" fill="#adb5b0">Ingeniería de software · Datos · Diseño de sistemas</text>
<text x="46" y="201" font-family="{font}" font-size="15" fill="#8f9a93">PUCV / Chile</text>
<g transform="translate(1042 54)" fill="none" stroke="#617b69" stroke-width="2">
<rect width="100" height="100" rx="4"/><path d="M0 50H100M50 0V100" stroke="#313c35"/>
<path d="M17 74L41 50L17 26M58 74H82" stroke="#9ab7a3" stroke-width="5"/>
</g>''', 1200, 238, 'Tomás Guerra Fuentes · Ingeniería de software, datos y diseño de sistemas · PUCV, Chile')

learning = [
    ('software.svg', '01', ['Ingeniería de', 'software'], ['Requisitos · Arquitectura', 'Modelamiento · Patrones'], 'APRENDIZAJE AUTÓNOMO'),
    ('applications.svg', '02', ['Desarrollo de', 'aplicaciones'], ['POO · APIs REST', '.NET Core · Angular'], 'APRENDIZAJE AUTÓNOMO'),
    ('data.svg', '03', ['Datos y', 'procesamiento'], ['SQL · Dask · PySpark', 'Apache Kafka'], 'APRENDIZAJE AUTÓNOMO'),
    ('senssa.svg', '04', ['Senssa', 'The Lift PUCV'], ['Primer lugar', 'Torneo 2025'], 'RECONOCIMIENTO'),
]
for name, number, titles, lines, status in learning:
    title_nodes = ''.join(f'<text x="22" y="{58+i*26}" fill="#edf0ed" font-family="{font}" font-size="21" font-weight="700">{escape(line)}</text>' for i, line in enumerate(titles))
    line_nodes = ''.join(f'<text x="22" y="{115+i*20}" fill="#a7b1aa" font-family="{font}" font-size="13">{escape(line)}</text>' for i, line in enumerate(lines))
    save('learning/' + name, f'''
    <rect x="1" y="1" width="278" height="168" rx="6" fill="#22282a" stroke="#3a4440"/>
    <text x="22" y="27" fill="#829b8c" font-family="{font}" font-size="11">{number}</text>
    <path d="M252 20V36M244 28H260" stroke="#708879"/>
    {title_nodes}{line_nodes}
    <text x="22" y="158" fill="#8fae9b" font-family="{font}" font-size="9" letter-spacing=".5">{status}</text>''',
         280, 170, ' · '.join(titles + lines + [status]))

project_icons = {
    'patitasgo': '<ellipse cx="32" cy="39" rx="12" ry="10"/><ellipse cx="15" cy="27" rx="5" ry="7"/><ellipse cx="27" cy="18" rx="5" ry="7"/><ellipse cx="40" cy="18" rx="5" ry="7"/><ellipse cx="51" cy="28" rx="5" ry="7"/>',
    'beetracer': '<path d="M15 22L32 13L49 22V42L32 51L15 42Z M15 22L32 32L49 22 M32 32V51 M23 18L41 28" fill="none" stroke="#a9c5b2" stroke-width="3" stroke-linejoin="round"/>',
    'flights': '<path d="M14 32L29 28L35 13L42 13L40 27L53 30V35L40 38L42 51H35L29 37L14 33Z"/>',
    'senssa': '<rect x="21" y="19" width="23" height="27" rx="6" fill="none" stroke="#a9c5b2" stroke-width="3"/><path d="M27 19V10H38V19M27 46V55H38V46M24 33H29L32 26L36 39L39 33H42" fill="none" stroke="#a9c5b2" stroke-width="3" stroke-linejoin="round"/>',
}
for name, drawing in project_icons.items():
    save('icons/' + name + '.svg', f'<rect width="64" height="64" rx="13" fill="#293330"/><g fill="#a9c5b2">{drawing}</g>', 64, 64, name)

labels = {
    'ionic': 'Ionic', 'react': 'React', 'nodejs': 'Node.js', 'express': 'Express',
    'postgresql': 'PostgreSQL', 'figma': 'Figma', 'dfd': 'DFD',
    'data-modeling': 'Modelamiento', 'documentation': 'Documentación',
    'dask': 'Dask', 'pyspark': 'PySpark', 'parquet': 'Parquet', 'spark-sql': 'Spark SQL',
    'innovation': 'Innovación', 'research': 'Investigación', 'pitch': 'Pitch',
}
for name, label in labels.items():
    width = round(len(label) * 6.6 + 18)
    save('badges/' + name + '.svg',
         f'<rect width="{width}" height="20" fill="#30363d"/><text x="{width/2}" y="14" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="11" fill="#dce1de">{escape(label)}</text>',
         width, 20, label)

save('wave-divider.svg', '''
<path fill="none" stroke="#8fae9b" stroke-opacity=".65" stroke-width="1.5"
 d="M-240 26Q-90 7 60 26T360 26T660 26T960 26T1260 26T1560 26">
<animateTransform attributeName="transform" type="translate" from="0 0" to="600 0" dur="14s" repeatCount="indefinite"/>
</path>
<path fill="none" stroke="#414b46" stroke-width="1" d="M0 29Q150 9 300 29T600 29T900 29T1200 29"/>
''', 1200, 54, 'Separador de ondas animadas en gris y verde')

print('Generated tech stack, four learning cards, project icons, badges and wave divider.')
