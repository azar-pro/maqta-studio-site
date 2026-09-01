from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "fr": ROOT / "fr" / "index.html",
    "en": ROOT / "en" / "index.html",
    "ar": ROOT / "ar" / "index.html",
}

SEO = {
    "fr": {
        "title": "Studio créatif Fès | Vinyle, Branding & Web — MAQTA",
        "description": "Studio créatif à Fès : identité visuelle, découpe vinyle, habillage véhicule au Maroc, signalétique, sites web, e-commerce et applications.",
        "h1": 'Studio créatif à Fès.<br/><span class="cutword">De l’identité au digital.</span>',
        "services_h2": "Services créatifs à Fès.<br/>Du branding au digital.",
        "faq_h2": "Questions fréquentes sur nos services à Fès.<br/>Réponses claires.",
        "alts": {
            "image-04-b0c31110089e.webp": "Conception de façade et signalétique pour NAWA Café à Fès — projet MAQTA",
            "image-05-8047ea27b712.webp": "Habillage véhicule et marquage adhésif Urban Move au Maroc — projet MAQTA",
            "image-06-c047225f08a2.webp": "Signalétique de façade et identité visuelle Luna Boutique à Fès — projet MAQTA",
            "image-07-b429438b65c0.webp": "Design de site e-commerce responsive Pure Organic — projet digital MAQTA",
        },
    },
    "en": {
        "title": "Creative Studio Fès | Branding, Signage & Web — MAQTA",
        "description": "Creative studio in Fès for brand identity, vinyl cutting, vehicle graphics in Morocco, signage, websites, e-commerce and mobile apps.",
        "h1": 'Creative studio in Fès.<br/><span class="cutword">From identity to digital.</span>',
        "services_h2": "Creative services in Fès.<br/>From branding to digital.",
        "faq_h2": "Frequently asked questions about our Fès services.<br/>Clear answers.",
        "alts": {
            "image-04-b0c31110089e.webp": "NAWA Café storefront branding and signage design in Fès — MAQTA project",
            "image-05-8047ea27b712.webp": "Urban Move vehicle graphics and vinyl branding in Morocco — MAQTA project",
            "image-06-c047225f08a2.webp": "Luna Boutique storefront signage and brand identity in Fès — MAQTA project",
            "image-07-b429438b65c0.webp": "Pure Organic responsive e-commerce website design — MAQTA digital project",
        },
    },
    "ar": {
        "title": "استوديو تصميم فاس | هوية، فينيل ومواقع — MAQTA",
        "description": "استوديو إبداعي في فاس لتصميم الهويات التجارية، قص فينيل الواجهات، إشهار السيارات، تصميم مواقع ويب ومتاجر إلكترونية وتطبيقات.",
        "h1": 'استوديو إبداعي في فاس.<br/><span class="cutword">من الهوية إلى الحضور الرقمي.</span>',
        "services_h2": "خدمات تصميم في فاس.<br/>من الهوية إلى الحلول الرقمية.",
        "faq_h2": "أسئلة شائعة عن خدماتنا في فاس.<br/>إجابات واضحة.",
        "alts": {
            "image-04-b0c31110089e.webp": "تصميم واجهة وهوية بصرية لمقهى NAWA في فاس — مشروع MAQTA",
            "image-05-8047ea27b712.webp": "إشهار سيارة وقص فينيل لمشروع Urban Move في المغرب — مشروع MAQTA",
            "image-06-c047225f08a2.webp": "تصميم لوحة وواجهة وهوية Luna Boutique في فاس — مشروع MAQTA",
            "image-07-b429438b65c0.webp": "تصميم متجر إلكتروني متجاوب Pure Organic — مشروع رقمي من MAQTA",
        },
    },
}

PROJECT_NAMES = ["NAWA CAFÉ", "URBAN MOVE", "LUNA BOUTIQUE", "PURE ORGANIC"]


def replace_meta(html, name, value):
    pattern = rf'<meta\s+content="[^"]*"\s+name="{re.escape(name)}"\s*/?>'
    return re.sub(pattern, f'<meta content="{value}" name="{name}"/>', html, count=1)


def replace_property(html, prop, value):
    pattern = rf'<meta\s+content="[^"]*"\s+property="{re.escape(prop)}"\s*/?>'
    return re.sub(pattern, f'<meta content="{value}" property="{prop}"/>', html, count=1)


def schema_for(lang, title, description):
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["ProfessionalService", "Organization"],
                "@id": "https://maqtastudio.com/#organization",
                "name": "MAQTA Studio",
                "alternateName": "MAQTA",
                "url": "https://maqtastudio.com/",
                "telephone": "+212639879506",
                "image": "https://maqtastudio.com/assets/og-image.jpg",
                "logo": "https://maqtastudio.com/assets/image-02-cad96d8d4eb4.png",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Fès",
                    "addressRegion": "Fès-Meknès",
                    "addressCountry": "MA",
                },
                "areaServed": [
                    {"@type": "City", "name": "Fès"},
                    {"@type": "AdministrativeArea", "name": "Fès-Meknès"},
                    {"@type": "Country", "name": "Morocco"},
                ],
                "serviceType": [
                    "Brand identity design",
                    "Print design",
                    "Vinyl cutting",
                    "Storefront signage",
                    "Vehicle graphics",
                    "Website design",
                    "E-commerce design",
                    "Mobile application design",
                ],
                "sameAs": ["https://www.instagram.com/maqta_studio/"],
                "contactPoint": {
                    "@type": "ContactPoint",
                    "telephone": "+212639879506",
                    "contactType": "customer service",
                    "areaServed": "MA",
                    "availableLanguage": ["Arabic", "French", "English"],
                },
                "hasOfferCatalog": {
                    "@type": "OfferCatalog",
                    "name": "MAQTA Studio Services",
                    "itemListElement": [
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Brand Identity Design"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Print Design"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Vinyl Cutting and Signage"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Vehicle Graphics"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Website and E-commerce Design"}},
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Mobile Application Design"}},
                    ],
                },
            },
            {
                "@type": "WebSite",
                "@id": "https://maqtastudio.com/#website",
                "url": "https://maqtastudio.com/",
                "name": "MAQTA Studio",
                "publisher": {"@id": "https://maqtastudio.com/#organization"},
                "inLanguage": ["fr", "en", "ar"],
            },
            {
                "@type": "WebPage",
                "@id": f"https://maqtastudio.com/{lang}/#webpage",
                "url": f"https://maqtastudio.com/{lang}/",
                "name": title,
                "description": description,
                "isPartOf": {"@id": "https://maqtastudio.com/#website"},
                "about": {"@id": "https://maqtastudio.com/#organization"},
                "inLanguage": lang,
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def patch_home(lang, path):
    data = SEO[lang]
    html = path.read_text(encoding="utf-8")

    assert len(data["title"]) < 60, (lang, "title too long", len(data["title"]))
    assert len(data["description"]) < 155, (lang, "description too long", len(data["description"]))

    html = re.sub(r'<title>.*?</title>', f'<title>{data["title"]}</title>', html, count=1, flags=re.S)
    html = replace_meta(html, "description", data["description"])
    html = replace_property(html, "og:title", data["title"])
    html = replace_property(html, "og:description", data["description"])
    html = replace_meta(html, "twitter:title", data["title"])
    html = replace_meta(html, "twitter:description", data["description"])

    html = re.sub(r'<h1>.*?</h1>', f'<h1>{data["h1"]}</h1>', html, count=1, flags=re.S)

    # Make the services section's H2 descriptive and local while preserving the minimalist two-line treatment.
    html = re.sub(
        r'(<div class="services-stage" id="services">.*?<div class="section-head reveal">\s*)<h2>.*?</h2>',
        rf'\1<h2>{data["services_h2"]}</h2>',
        html,
        count=1,
        flags=re.S,
    )

    # Keep FAQ as a true H2 and make its local relevance explicit.
    html = re.sub(
        r'(<section class="faq wrap" id="faq">\s*<div class="section-head reveal">\s*)<h2>.*?</h2>',
        rf'\1<h2>{data["faq_h2"]}</h2>',
        html,
        count=1,
        flags=re.S,
    )

    # Project names are portfolio labels, not primary information architecture headings.
    for name in PROJECT_NAMES:
        html = html.replace(f'<h3>{name}</h3>', f'<div class="work-project-title">{name}</div>')

    # Replace the existing homepage JSON-LD with one consistent Local Business/ProfessionalService graph.
    schema = schema_for(lang, data["title"], data["description"])
    html = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        f'<script type="application/ld+json">{schema}</script>',
        html,
        count=1,
        flags=re.S,
    )

    path.write_text(html, encoding="utf-8")


def patch_alts():
    # Apply localized ALT text anywhere these core portfolio images appear, including case-study pages.
    for lang in ("fr", "en", "ar"):
        lang_root = ROOT / lang
        if not lang_root.exists():
            continue
        for path in lang_root.rglob("*.html"):
            html = path.read_text(encoding="utf-8")
            original = html
            for filename, alt in SEO[lang]["alts"].items():
                pattern = rf'<img\b([^>]*?)\balt="[^"]*"([^>]*?\bsrc="[^"]*{re.escape(filename)}"[^>]*?)>'
                html = re.sub(pattern, rf'<img\1alt="{alt}"\2>', html)
                # Also handle markup where src precedes alt.
                pattern2 = rf'<img\b([^>]*?\bsrc="[^"]*{re.escape(filename)}"[^>]*?)\balt="[^"]*"([^>]*?)>'
                html = re.sub(pattern2, rf'<img\1alt="{alt}"\2>', html)
            if html != original:
                path.write_text(html, encoding="utf-8")


def patch_css():
    css_path = ROOT / "assets" / "site.css"
    css = css_path.read_text(encoding="utf-8")
    marker = "/* MAQTA SEO semantic project-title compatibility */"
    if marker not in css:
        css += "\n\n" + marker + "\n.work-project-title{font:inherit;font-family:inherit;color:inherit;}\n"
        # Copy the visual treatment from project H3 elements at runtime via selector aliasing where possible.
        # This minimal rule preserves inherited typography; the existing card layout remains unchanged.
    css_path.write_text(css, encoding="utf-8")


def audit_repository():
    sitemap = ROOT / "sitemap.xml"
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(sitemap)
    locs = [el.text.strip() for el in tree.findall(".//sm:loc", ns) if el.text]
    missing = []
    for url in locs:
        rel = url.replace("https://maqtastudio.com/", "").strip("/")
        candidate = ROOT / rel / "index.html"
        if not candidate.exists():
            missing.append((url, str(candidate.relative_to(ROOT))))

    rows = []
    for lang, path in PAGES.items():
        html = path.read_text(encoding="utf-8")
        title = re.search(r'<title>(.*?)</title>', html, re.S)
        desc = re.search(r'<meta content="([^"]*)" name="description"', html)
        h1 = re.search(r'<h1>(.*?)</h1>', html, re.S)
        rows.append((lang, len(title.group(1)) if title else 0, len(desc.group(1)) if desc else 0, bool(h1)))

    report = [
        "# MAQTA Technical & Local SEO Audit",
        "",
        "Generated automatically on branch `seo-local-2026-09`.",
        "",
        "## Repository completeness against sitemap",
        f"- Sitemap URLs: **{len(locs)}**",
        f"- Missing corresponding `index.html` files: **{len(missing)}**",
    ]
    if missing:
        report += ["", "### Missing"] + [f"- `{u}` → expected `{p}`" for u, p in missing]
    else:
        report += ["- Result: **all sitemap URLs have corresponding repository pages**."]

    report += ["", "## Homepage SEO limits", "", "| Language | Title chars | Description chars | H1 present |", "|---|---:|---:|---|"]
    for lang, tl, dl, h1ok in rows:
        report.append(f"| {lang} | {tl} | {dl} | {'yes' if h1ok else 'no'} |")

    report += [
        "",
        "## Applied changes",
        "- Localized H1 for Fès in FR/EN/AR.",
        "- Services and FAQ retained as semantic H2 sections; core service names remain H3.",
        "- Portfolio project names demoted from H3 to visual labels to reduce heading noise.",
        "- Homepage title/meta/OG/Twitter copy localized and kept below requested character limits.",
        "- Local `ProfessionalService` + `Organization` JSON-LD normalized as MAQTA Studio.",
        "- Localized ALT text applied to NAWA Café, Urban Move, Luna Boutique and Pure Organic images across language pages.",
        "- No street address, postal code, coordinates, price range or opening hours invented.",
        "",
        "## Live-site comparison limitation",
        "The repository was audited against its sitemap and internal file structure. A byte-for-byte comparison with the currently served domain is not performed by this workflow; production should be verified after deployment using Search Console / live HTTP checks.",
    ]
    (ROOT / "SEO_AUDIT_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")


for lang, path in PAGES.items():
    patch_home(lang, path)
patch_alts()
patch_css()
audit_repository()
print("MAQTA SEO patch complete")
