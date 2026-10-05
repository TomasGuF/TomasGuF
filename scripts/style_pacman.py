"""Apply the profile palette without changing contribution data or animation."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'light': {
        '#ffffff': '#f5f6f3', '#57606a': '#606966', '#ebedf0': '#d9ddda',
        '#9be9a8': '#d6e3d9', '#40c463': '#b5cbbd',
        '#30a14e': '#91ac9a', '#216e39': '#577a63',
    },
    'dark': {
        '#0d1117': '#25282a', '#8b949e': '#a1a6a7', '#161b22': '#34383a',
        '#0e4429': '#465c4e', '#006d32': '#606966',
        '#26a641': '#739a82', '#39d353': '#8fae9b',
    },
}

for theme, palette in PALETTES.items():
    suffix = '-dark' if theme == 'dark' else ''
    source = ROOT / 'dist' / f'pacman-contribution-graph{suffix}.svg'
    content = source.read_text(encoding='utf-8')
    content = re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: palette.get(m.group().lower(), m.group()), content)
    (ROOT / 'assets' / f'pacman-{theme}.svg').write_text(content, encoding='utf-8')
print('Updated Pac-Man colors; contribution data and animation preserved.')
