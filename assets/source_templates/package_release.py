"""Create the standalone Springer source and research evidence ZIP files."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables';OUT.mkdir(exist_ok=True)

SOURCE_FILES=[
    'paper/anonymous.tex','paper/identified.tex','paper/body.tex',
    'paper/preamble.tex','paper/numbers.tex','paper/anonymous.bbl',
    'paper/identified.bbl','paper/references.bib','paper/llncs.cls',
    'paper/splncs04.bst','paper/build.py','paper/tables/data.tex',
    'paper/tables/runtime.tex','paper/figures/overview.pdf',
    'paper/figures/performance.pdf','paper/figures/mechanism.pdf',
    'paper/figures/scale.pdf','paper/figures/workload_regimes.pdf',
    'paper/figures/speedup_distributions.pdf','paper/figures/runtime_structure.pdf',
    'README.md']

def add(z,path,arc):
    z.write(path,arcname=arc)

def source_zip():
    target=OUT/'dasfaa2027_far_springer_source.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in SOURCE_FILES:
            arc=rel.removeprefix('paper/')
            add(z,ROOT/rel,arc)
    return target

def research_zip():
    target=OUT/'dasfaa2027_far_research_package.zip'
    roots=['src','results','literature']
    files=[]
    for folder in roots:
        files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    files.extend(p for p in (ROOT/'paper').rglob('*') if p.is_file() and 'build' not in p.parts)
    files.extend(p for p in (ROOT/'qa').glob('*') if p.is_file())
    files.extend([ROOT/x for x in ['README.md','METHOD.md','RESEARCH_PLAN.md','USER_REQUIREMENTS.md','论文说明_CN.md']])
    files.extend((ROOT/'data').glob('*.json'))
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(set(files)):
            add(z,p,Path(ROOT.name)/p.relative_to(ROOT))
    return target

if __name__=='__main__':
    for p in [source_zip(),research_zip()]:print(p.name,p.stat().st_size)
