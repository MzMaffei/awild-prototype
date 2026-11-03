#!/usr/bin/env python3
"""Build the A Wild World redesign prototype.

pages/<name>.html  -> docs/<name>.html, wrapped in the shared head/header/footer.
First line of each page file: <!-- title | description | nav-key -->
Run: python3 -I build.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = ROOT / "pages"
OUT = ROOT / "docs"  # served by GitHub Pages (main branch, /docs)
REAL = "https://www.awild.world"

NAV = [
    ("vivi", "vivi.html", "Vivi"),
    ("impara", "impara.html", "Impara"),
    ("lavora", "lavora-con-me.html", "Lavora con me"),
    ("chi", "chi-sono.html", "Chi sono"),
]

HEAD = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Averia+Serif+Libre:wght@700&family=Bitter:wght@400;600&family=Raleway:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
{extra_head}
</head>
<body>
<div class="proto">Prototipo di redesign, non è il sito ufficiale. Acquisti e iscrizioni portano al sito vero, <a href="{real}">awild.world</a> · <a href="protocollo.html">Leggi il protocollo delle modifiche</a></div>
<header class="site">
  <div class="wrap bar">
    <a class="logo" href="index.html">A Wild World<small>di Federica Portentoso</small></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="main" id="nav">
{nav}
      <a class="btn sm" href="wild-fest.html">Wild Fest 2027</a>
    </nav>
  </div>
</header>
<main>
"""

FOOT = """</main>
<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <div class="logo" style="color:#fff">A Wild World</div>
        <p style="margin-top:14px">Fotografia, autoproduzione ed esperienze in natura. Da un casale tra le colline marchigiane.</p>
        <a href="{real}/newsletter" class="btn sm light" style="display:inline-block;margin-top:6px">Iscriviti alla newsletter</a>
      </div>
      <div>
        <h4>Vivi</h4>
        <a href="wild-fest.html">Wild Fest 2027</a>
        <a href="vivi.html#retreat">Retreat</a>
        <a href="vivi.html#viaggi">Viaggi di gruppo</a>
      </div>
      <div>
        <h4>Impara</h4>
        <a href="diventa-fotografo.html">Corsi di fotografia</a>
        <a href="impara.html#autoproduzione">Manuale di autoproduzione</a>
        <a href="metamorphosis.html">Metamorphōsis</a>
        <a href="impara.html#shop">Preset, planner, libro</a>
      </div>
      <div>
        <h4>Info</h4>
        <a href="lavora-con-me.html">Coaching e consulenze</a>
        <a href="{real}/gift-card">Gift card</a>
        <a href="{real}/area-membri">Area membri</a>
        <a href="{real}/contact">Contatti</a>
        <a href="https://www.instagram.com/a.wild.mind/">Instagram</a>
      </div>
    </div>
    <div class="legal">© 2018–2026 A Wild World di Federica Portentoso Guarriello · P.IVA 02583410440 · <a style="display:inline" href="{real}/privacy-policy">Privacy</a> · <a style="display:inline" href="{real}/cookie-policy">Cookie</a> · <a style="display:inline" href="{real}/termini-e-condizioni">Termini e condizioni</a><br>Prototipo preparato da Claude (claude@tasty.lu), assistente AI di Maurizio Maffei, novembre 2026.</div>
  </div>
</footer>
<script>
document.querySelector('.menu-toggle').addEventListener('click',function(){{
  var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o);
}});
</script>
</body>
</html>
"""


def build():
    OUT.mkdir(exist_ok=True)
    built = []
    for src in sorted(PAGES.glob("*.html")):
        text = src.read_text(encoding="utf8")
        first, _, body = text.partition("\n")
        m = re.match(r"<!--\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(\w*)\s*-->", first)
        if not m:
            raise SystemExit(f"{src.name}: missing metadata line")
        title, desc, key = m.groups()
        extra = ""
        if "<!--HEAD" in body:
            extra, body = re.match(r"\s*<!--HEAD\s*(.*?)HEAD-->(.*)", body, re.S).groups()
        nav = "\n".join(
            f'      <a href="{href}"{" aria-current=\"page\"" if k == key else ""}>{label}</a>'
            for k, href, label in NAV
        )
        html = (HEAD.format(title=title, desc=desc, nav=nav, real=REAL, extra_head=extra)
                + body.replace("{REAL}", REAL)
                + FOOT.format(real=REAL))
        (OUT / src.name).write_text(html, encoding="utf8")
        built.append(src.name)
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    (OUT / ".nojekyll").write_text("")
    print("built:", ", ".join(built))


if __name__ == "__main__":
    build()
