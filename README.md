# MAQTA Studio Website

A multilingual business website for **MAQTA Studio**, a creative studio based in Fès, Morocco, offering brand identity, print design, signage & vinyl, websites, e-commerce and digital product design.

**Live website:** https://maqtastudio.com/

---

## Overview

This project is a custom-built, responsive, multilingual website designed to present MAQTA Studio's services, portfolio and contact flow in a clear and premium way.

The website supports:

- French (`/fr/`)
- English (`/en/`)
- Arabic (`/ar/`)
- RTL and LTR layouts
- Responsive desktop, tablet and mobile experiences
- Technical and local SEO for Fès, Morocco
- Structured service and business information
- WhatsApp-based project enquiries

The site is intentionally lightweight and does not depend on a large front-end framework.

---

## Tech Stack

- **HTML5**
- **CSS3**
- **Vanilla JavaScript**
- **JSON-LD / Schema.org structured data**
- **Netlify-ready static hosting configuration**

No React, Next.js or CMS is used in the current implementation.

---

## Main Features

### Multilingual architecture

Each language has its own complete page structure rather than relying on client-side translation.

This improves:

- search engine indexing
- accessibility
- language consistency
- correct RTL behavior for Arabic
- shareable language-specific URLs

### Responsive design

The interface is designed to work across desktop, tablet and mobile layouts, with dedicated navigation and mobile contact behavior.

### Technical SEO

The project includes:

- canonical URLs
- `hreflang` tags for FR / EN / AR
- `x-default` language targeting
- semantic page titles and descriptions
- Open Graph metadata
- Twitter card metadata
- `robots.txt`
- `sitemap.xml`
- structured data using Schema.org
- breadcrumb structured data
- local business information for Fès

### Local SEO

The website includes structured information for MAQTA Studio's physical business presence in Fès, including:

- business location
- service area
- opening hours
- phone number
- service categories
- supported languages

### Project enquiry flow

The contact form does not store form data on the website.

Instead, JavaScript prepares the project information and opens a pre-filled WhatsApp message for the visitor.

---

## Website Structure

```text
/
├── index.html
├── fr/
│   ├── index.html
│   ├── services/
│   ├── work/
│   ├── faq/
│   └── contact/
├── en/
│   ├── index.html
│   ├── services/
│   ├── work/
│   ├── faq/
│   └── contact/
├── ar/
│   ├── index.html
│   ├── services/
│   ├── work/
│   ├── faq/
│   └── contact/
├── assets/
│   ├── site.css
│   ├── site.js
│   ├── images...
│   └── favicons...
├── robots.txt
├── sitemap.xml
├── _headers
└── _redirects
```

---

## Services Presented

The website presents MAQTA Studio's main service areas:

- Brand identity and logo design
- Business cards and print design
- Packaging, labels and stickers
- Signage and vinyl graphics
- Vehicle graphics
- Landing pages
- Business websites
- E-commerce websites
- Web applications and client portals
- Mobile application design

---

## Selected Case Studies

The portfolio includes selected visual case studies such as:

- **LUNA Boutique**
- **NAWA Café**
- **PURE ORGANIC — Concept Case Study**
- **Urban Move**

> **Portfolio note:** PURE ORGANIC is presented as a concept case study and should not be interpreted as commissioned client work.

---

## Design Direction

The visual identity follows MAQTA Studio's premium editorial direction:

- minimal luxury aesthetic
- restrained typography
- dark neutral palette
- oxide-red accents
- strong spacing and hierarchy
- presentation-focused project pages

The goal is to make the website itself function as part of the studio's portfolio.

---

## Accessibility & UX

The implementation includes practical accessibility and usability considerations such as:

- semantic HTML structure
- language declarations
- RTL support
- responsive typography and layouts
- accessible navigation labels
- descriptive image alternative text where applicable
- progressive reveal animations using `IntersectionObserver`
- graceful fallback when browser APIs are unavailable

---

## JavaScript

The custom JavaScript remains intentionally small and is used for:

- FAQ accordion behavior
- reveal-on-scroll interactions
- WhatsApp project enquiry preparation

This keeps the site lightweight and easy to maintain.

---

## Deployment

The project is designed as a static site and can be deployed to services such as Netlify or any static web host.

The production website is available at:

**https://maqtastudio.com/**

---

## Project Status

Production website — actively maintained.

---

## About MAQTA Studio

MAQTA Studio is a creative studio in Fès, Morocco, working across branding, print, signage and digital experiences.

Website: https://maqtastudio.com/

Instagram: https://www.instagram.com/maqta_studio/

---

© 2026 MAQTA Studio
