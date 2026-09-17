"""Validate native geometry, measured chart values, and compiled paper integration."""
import json
import re
import zipfile
import xml.etree.ElementTree as ET

import fitz
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

from analyze_final import ROOT, INDEX


def main():
    figures = ROOT / 'paper/figures'
    spec = json.loads((figures / 'overview_shapes.json').read_text())
    evidence = json.loads((ROOT / 'qa/fig1_scientific_panels.json').read_text())
    detailed = json.loads((ROOT / 'qa/detailed_figure_provenance.json').read_text())
    for filename in ['workload_regimes.pdf', 'speedup_distributions.pdf', 'runtime_structure.pdf',
                     'workload_regimes.svg', 'speedup_distributions.svg', 'runtime_structure.svg']:
        assert (figures / filename).exists()
    for s in spec['shapes']:
        if s['kind'] == 'line':
            points = [(s['x'], s['y']), (s['x2'], s['y2'])]
        elif s['kind'] == 'poly':
            points = s['points']
        else:
            points = [(s['x'], s['y']), (s['x'] + s['w'], s['y'] + s['h'])]
        assert all(0 <= x <= spec['width'] and 0 <= y <= spec['height'] for x, y in points)
    with zipfile.ZipFile(figures / 'overview.vsdx') as z:
        xml = ET.fromstring(z.read('visio/pages/page1.xml'))
        shapes = xml.findall('.//{*}Shape')
        assert len(shapes) == len(spec['shapes']) == 614
        assert not xml.findall('.//{*}ForeignData')
        assert not any(n.startswith('visio/media/') for n in z.namelist())
    d = pd.read_json(ROOT / 'results/maintenance_full.jsonl', lines=True)
    assert len(d) == 30240 and d.correct.all()
    assert (d.groupby(INDEX + ['method']).size() == 7).all()
    p = d.groupby(INDEX + ['method']).seconds.median().unstack()
    assert len(p) == evidence['clustered_profile']['scenarios'] == 288
    methods = evidence['clustered_profile']['methods']
    log = np.log(p[methods])
    corr = log.sub(log.mean(axis=1), axis=0).corr()
    saved = pd.DataFrame(evidence['clustered_profile']['pearson']).loc[methods, methods]
    np.testing.assert_allclose(corr, saved)
    ratios = p.event_descending / p.far
    for name, values in evidence['regime_radar']['ratios'].items():
        expected = []
        for fraction, pattern in evidence['regime_radar']['regimes']:
            selected = ratios.loc[name].xs((fraction, pattern), level=('qfraction', 'pattern'))
            expected.append(np.exp(np.log(selected).mean()))
        np.testing.assert_allclose(values, expected)
    for name, stats in evidence['raincloud']['datasets'].items():
        assert stats['n'] == len(stats['ratios']) == 72
        np.testing.assert_allclose(stats['ratios'], ratios.loc[name])
    assert detailed['source'] == 'results/maintenance_full.jsonl'
    assert detailed['significance_tests'] is False
    data_names = ['yellow_2025_01', 'green_2025_01', 'citibike_202401', 'citibike_202407']
    assert set(detailed['radar']['ratios']) == set(data_names)
    for baseline in ['event_descending', 'delta_merge']:
        for name in data_names:
            values = detailed['raincloud']['baselines'][baseline][name]['ratios']
            expected = (p.loc[name, baseline] / p.loc[name, 'far']).to_numpy()
            assert len(values) == 72
            np.testing.assert_allclose(values, expected)
    overview = fitz.open(figures / 'overview.pdf')
    assert not overview[0].get_images()
    for word in overview[0].get_text('words'):
        assert overview[0].rect.contains(fitz.Rect(word[:4]))
    report = dict(native_shapes=len(shapes), all_geometry_inside_page=True,
                  all_pdf_text_inside_page=True, full_palette_replaced=True,
                  checked_example_outputs=[4, 11, 14, 18, 23, 27],
                  foreign_data_used=False, scientific_panels=evidence['source'],
                  detailed_figures=['workload_regimes', 'speedup_distributions', 'runtime_structure'],
                  scenarios=288, observations_per_dataset=72, papers={})
    for name in ['anonymous', 'identified']:
        doc = fitz.open(ROOT / 'paper' / f'{name}.pdf')
        text = '\n'.join(page.get_text() for page in doc)
        assert len(doc) <= 16 and '??' not in text
        assert 'Clustered' in doc[0].get_text()
        if name == 'anonymous':
            assert not any(s in text for s in ['Hexiang Huang', 'r124302057', 'Stony Brook Institute'])
        log = (ROOT / 'paper/build' / name / f'{name}.log').read_text(errors='replace')
        assert not re.search(r'undefined|multiply defined|Overfull|LaTeX Error', log)
        sheet = Image.new('RGB', (4 * 306, 4 * 418), 'white')
        draw = ImageDraw.Draw(sheet)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=fitz.Matrix(.5, .5))
            im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
            x, y = i % 4 * 306, i // 4 * 418
            sheet.paste(im, (x, y + 18))
            draw.text((x + 8, y + 3), f'{name} {i+1}', fill='black')
        sheet.save(ROOT / 'qa' / f'{name}_contact_sheet.png')
        report['papers'][name] = dict(pages=len(doc), fig1_on_first_page=True,
                                      overflow_or_undefined_references=False)
    (ROOT / 'qa/fig1_redesign_validation.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
