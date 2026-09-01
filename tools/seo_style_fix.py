from pathlib import Path

root = Path(__file__).resolve().parents[1]
css_path = root / "assets" / "site.css"
css = css_path.read_text(encoding="utf-8")
marker = "/* MAQTA SEO portfolio semantic-title visual parity */"
block = r'''

/* MAQTA SEO portfolio semantic-title visual parity */
.work-copy .work-project-title{
  margin:0;
  font-family:Georgia,'Times New Roman',serif;
  font-size:29px;
  line-height:1;
  font-weight:500;
  letter-spacing:.01em;
}
body[dir="rtl"] .work-copy .work-project-title{
  font-family:Georgia,'Times New Roman',serif;
}
@media(max-width:899px){
  .work-copy .work-project-title{text-align:center;}
}
@media(max-width:430px){
  .work-copy .work-project-title{font-size:25px;}
}
'''
if marker not in css:
    css += block
    css_path.write_text(css, encoding="utf-8")
print("Portfolio semantic title styles preserved")
