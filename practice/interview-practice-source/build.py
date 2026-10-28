#!/usr/bin/env python3
"""Build interview-practice.html from data/*.txt and template.html."""
import glob, hashlib, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = ["Foundations", "Programming Fundamentals", "Languages", "Backend and Frontend Stack",
        "Cloud and Infrastructure", "APIs and Architecture", "Data", "Security and Compliance",
        "Delivery and Operations", "Ways of Working", "AI and LLMs", "AI-Assisted Engineering",
        "Interviews and Career"]


def typo(plain: str) -> str:
    """Escape and apply typographic quotes to prose (never inside code)."""
    t = html.escape(plain, quote=False)
    t = re.sub(r'"([^"]*)"', '\u201c\\1\u201d', t)           # "..." -> “...”
    t = re.sub(r"(^|[\s(\[\u2014\u201c])'", '\\1\u2018', t)   # opening single quote
    t = t.replace("'", '\u2019')                               # apostrophes and closing quotes
    t = t.replace(' -- ', ' \u2014 ')
    return t


def rich(text: str) -> str:
    """Prose with `code` spans -> HTML."""
    parts = re.split(r'(`[^`]*`)', text.strip())
    out = []
    for p in parts:
        if p.startswith('`') and p.endswith('`') and len(p) >= 2:
            out.append('<code>' + html.escape(p[1:-1], quote=False) + '</code>')
        else:
            out.append(typo(p))
    return ''.join(out)


def plain(text: str) -> str:
    return re.sub(r'`([^`]*)`', r'\1', text.strip())


def strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) > 1 and s[0] == '"' and s[-1] == '"' and s.count('"') == 2:
        return s[1:-1]
    return s


def qid(*parts):
    return hashlib.sha1('|'.join(parts).encode()).hexdigest()[:10]


def file_key(path):
    name = os.path.basename(path)
    m = re.match(r'(\d+)-(.*)\.txt$', name)
    num = int(m.group(1)); rest = m.group(2)
    return (num, rest.endswith('-iq'), rest)


def parse():
    files = sorted(glob.glob(os.path.join(HERE, 'data', '*.txt')), key=file_key)
    sheets = {}       # (doc, sheet) -> order
    questions = []
    for path in files:
        doc = sheet = None
        main = None
        for raw in open(path, encoding='utf8'):
            line = raw.rstrip('\n')
            if not line.strip():
                continue
            if line.startswith('#DOC '):
                doc = line[5:].strip(); assert doc in DOCS, doc; continue
            if line.startswith('#SHEET '):
                sheet = line[7:].strip()
                sheets.setdefault((doc, sheet), len(sheets))
                main = None
                continue
            tag, _, body = line.partition(' ')
            d = DOCS.index(doc)
            if tag == 'Q':
                main = {'id': qid(doc, sheet, 'm', plain(body)), 'd': d, 's': sheet, 'k': 'm',
                        'q': rich(body), 'a': '', 'p': [], 'fu': []}
                questions.append(main)
            elif tag == 'A':
                main['a'] = rich(strip_quotes(body))
            elif tag == 'W':
                main['p'].append({'w': rich(body), 's': ''})
            elif tag == 'S':
                if not main['p'] or main['p'][-1]['s']:
                    main['p'].append({'w': '', 's': ''})
                main['p'][-1]['s'] = rich(body)
            elif tag in ('F', 'I'):
                q, sep, a = body.partition(' || ')
                assert sep, f'missing || in {path}: {line[:60]}'
                k = 'f' if tag == 'F' else 'i'
                item = {'id': qid(doc, sheet, k, plain(q)), 'd': d, 's': sheet, 'k': k,
                        'q': rich(q), 'a': rich(a)}
                if k == 'f':
                    assert main, f'follow-up without main question in {path}'
                    item['parent'] = main['id']
                    main['fu'].append(item['id'])
                questions.append(item)
            else:
                raise SystemExit(f'Unknown line in {path}: {line[:80]}')
    order = {k: v for k, v in sheets.items()}
    questions.sort(key=lambda q: (q['d'], order[(DOCS[q['d']], q['s'])], {'m': 0, 'f': 1, 'i': 2}[q['k']]))
    ids = [q['id'] for q in questions]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f'duplicate ids: {dupes}'
    for q in questions:
        if q['k'] == 'm':
            assert q['a'], f"main question without answer: {q['s']}"
    return questions, sheets


def main():
    questions, sheets = parse()
    present = sorted({q['d'] for q in questions})
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf8').read()
    payload = json.dumps({'docs': DOCS, 'questions': questions}, ensure_ascii=False, separators=(',', ':'))
    payload = payload.replace('</', '<\\/')
    out = tpl.replace('/*__DATA__*/null', payload)
    path = os.path.join(HERE, 'interview-practice.html')
    open(path, 'w', encoding='utf8').write(out)
    by_kind = {k: sum(1 for q in questions if q['k'] == k) for k in 'mfi'}
    print(f"{len(questions)} questions ({by_kind['m']} main, {by_kind['f']} follow-ups, {by_kind['i']} interview) "
          f"from {len(sheets)} sheets in {len(present)} docs -> {os.path.getsize(path)//1024} KB")
    for d in range(len(DOCS)):
        n = sum(1 for q in questions if q['d'] == d)
        print(f"  {DOCS[d]}: {n}")


if __name__ == '__main__':
    main()
