"""Export individual vector panels from the authoritative Visio PDF."""
from pathlib import Path
import json
import fitz

ROOT=Path(__file__).resolve().parents[1]
def main():
    fig=ROOT/'paper/figures'
    with fitz.open(fig/'overview.pdf') as source:
        source[0].get_pixmap(matrix=fitz.Matrix(3,3),alpha=False).save(fig/'overview.png')
        for name,(x,y,w,h) in json.loads((ROOT/'qa/fig1_scientific_panels.json').read_text())['panel_rectangles_top_origin_inches'].items():
            clip=fitz.Rect(x*72,y*72,(x+w)*72,(y+h)*72)
            with fitz.open() as doc:
                page=doc.new_page(width=360,height=360*h/w)
                page.show_pdf_page(page.rect,source,0,clip=clip)
                doc.save(fig/f'{name}.pdf',garbage=4,deflate=True)
                (fig/f'{name}.svg').write_text(page.get_svg_image(),encoding='utf8')
                page.get_pixmap(matrix=fitz.Matrix(3,3),alpha=False).save(fig/f'{name}.png')
    print('Overview and three individual chart panels exported')
if __name__=='__main__':main()
