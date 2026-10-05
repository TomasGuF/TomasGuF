"""Apply the profile palette without changing contribution data or animation."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'light': {
        '#ffffff': '#f2f7f4', '#57606a': '#5e797c', '#ebedf0': '#e2ebe6',
        '#9be9a8': '#cde8db', '#40c463': '#abd4c4',
        '#30a14e': '#78ad98', '#216e39': '#4a7867',
    },
    'dark': {
        '#0d1117': '#202438', '#8b949e': '#c0d0ce', '#161b22': '#2b343b',
        '#0e4429': '#36544e', '#006d32': '#587a74',
        '#26a641': '#83b7a2', '#39d353': '#abd4c4',
    },
}

for theme, palette in PALETTES.items():
    suffix = '-dark' if theme == 'dark' else ''
    source = ROOT / 'dist' / f'pacman-contribution-graph{suffix}.svg'
    content = source.read_text(encoding='utf-8')
    content = re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: palette.get(m.group().lower(), m.group()), content)
    (ROOT / 'assets' / f'pacman-{theme}.svg').write_text(content, encoding='utf-8')
print('Updated Pac-Man colors; contribution data and animation preserved.')
