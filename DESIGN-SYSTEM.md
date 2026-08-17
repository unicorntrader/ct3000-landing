# CoTrader 3000 Landing Page — Design System Reference

Canonical values in use across all 13 pages, verified by direct audit
of the codebase (not aspirational — this is what's actually shipped).

**Important:** this repo has no shared stylesheet and no build step.
Each of the 13 HTML files is fully self-contained with its own inline
`<style>` block and duplicated `:root` variables, header, and footer
markup. This document is the closest thing to a single source of
truth — if you change a value, it needs to be changed in all 13 files
by hand (or scripted) to stay in sync.

**Header/footer markup specifically is scripted:** `sync-shared.py`
holds the canonical header/footer HTML as one template and rewrites all
13 pages from it. Run `python3 sync-shared.py` after changing the
header/footer template inside that file, or `python3 sync-shared.py
--check` to verify nothing has drifted before a commit. It's a local
script only — GitHub Pages still serves the committed HTML directly, no
build step in the actual deploy pipeline.

This is also *why* drift bugs
happen (see "Known past bugs" at the end) — there's no shared header
component, just 13 copies of the same markup.

---

## Colors

### Brand (blue)
| Token | Hex |
|---|---|
| `--blue-50` | `#eff6ff` |
| `--blue-200` | `#bfdbfe` |
| `--blue-600` | `#2563eb` (primary) |
| `--blue-700` | `#1d4ed8` (hover fill) |
| `--blue-800` | `#1e40af` |
| `--blue-900` | `#1e3a5f` (muted navy, index.html premium panels) |

### Semantic
| Token | Hex |
|---|---|
| `--green-50/100/200/500/600/700/800` | `#f0fdf4` `#dcfce7` `#bbf7d0` `#22c55e` `#16a34a` `#15803d` `#166534` |
| `--red-50/200/500/600/700` | `#fef2f2` `#fecaca` `#ef4444` `#dc2626` `#b91c1c` |
| `--amber-50/100/200/500/700/800` | `#fffbeb` `#fef3c7` `#fde68a` `#f59e0b` `#b45309` `#92400e` |

Semantic role: green = positive/win, red = negative/loss, amber = warning/caution. Never reused for anything else (no decorative green/red/amber).

Extra accents (index.html tag dots, Journal → Tags — decorative variety, not semantic): `--cyan-200 #a5f3fc` / `--cyan-500 #06b6d4`, `--violet-200 #ddd6fe` / `--violet-500 #8b5cf6`, `--rose-200 #fecdd3` / `--rose-500 #f43f5e`, `--emerald-200 #a7f3d0` (emerald dots reuse `--green-500`, no separate emerald-500 defined).

### Neutrals
| Token | Hex |
|---|---|
| `--ink` / `--gray-900` | `#111827` |
| `--gray-700` | `#1f2937` |
| `--gray-600` | `#374151` |
| `--gray-500` | `#6b7280` |
| `--gray-400` | `#9ca3af` |
| `--gray-300` | `#d1d5db` |
| `--gray-200` | `#e5e7eb` |
| `--gray-100` | `#f3f4f6` |
| `--gray-50` | `#f9fafb` |
| `--white` | `#ffffff` |

**Rule:** never introduce a fresh hex value anywhere on the site — pick the closest real step in the palette above. The only sanctioned exception is the logo's fixed `#231f20` fill, which is the literal brand-mark color, not a themeable token.

### Usage conventions (evidence-based — grepped across all 13 files)

**Text on light backgrounds:**
- Headlines (h1/h2/h3), no exceptions found anywhere on the site: `--ink`
- Eyebrow/label text (small uppercase tags above headlines): `--blue-600`
- Body copy on white/light backgrounds: `--ink` — **not** gray. This was an explicit fix earlier this session (user: *"i dont want grey text on white background"*); don't regress it.
- Secondary/meta text (timestamps, captions like "4 min read", helper labels): `--gray-500`
- Nav links: default `--gray-600`, hover → `--ink`, current/active page → `--blue-600`
- Footer column headers (h5, on dark bg): `--blue-200`
- Footer links (on dark bg): `--gray-300`, hover → `--white`

**Dark "premium" sections** key off `--ink`, `--gray-700`, `--blue-900`, and `--blue-600` — never a one-off hex:
- Footer (all 13 pages): `linear-gradient(180deg, var(--ink) 0%, var(--gray-700) 100%)`
- Testimonial card (index.html): `linear-gradient(135deg, var(--ink) 0%, var(--blue-900) 100%)`
- Philosophy (index.html): flat `var(--ink)`
- Mentorship-teaser (index.html): flat `var(--blue-900)` — deliberately a hue change, not just a lightness step, from Philosophy since the two sections sit back-to-back; identical (or too-similar) darks read as one block with no seam.
- Final CTA (index.html): flat `var(--blue-600)` — the one loud, bold-brand-color section on the page (everything else is neutral), matching the reference template's pattern of ending on the boldest visual note instead of a quiet gray.

**Borders:**
- Cards / dividers: `--gray-200` (dominant choice, used ~19x)
- Interactive/button borders: `--blue-600` (primary buttons), `--blue-200` (secondary/outline buttons)

---

## Typography

**Font:** General Sans (Fontshare CDN), weights 400/500/600/700.
Fallback stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`

```html
<link rel="preconnect" href="https://api.fontshare.com">
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&display=swap">
```

Type scale is now fluid (`clamp(min, preferred-vw, max)`) almost everywhere, matched to a measured spec of try-gather.co's production CSS — the `min` in each clamp **is** the mobile value; there's no separate mobile override for most of these.

### Type scale
| Element | Size | Weight | Notes |
|---|---|---|---|
| Hero H1 (index.html) | `clamp(38px, 9.5vw, 86px)` | 800 | line-height 0.88, letter-spacing -0.02em; `34px` fixed override below 640px (prevents 3-line wrap) |
| Landing-page H1 (FAQ/Blog/Mentorship/doc pages) | `clamp(34px, 5vw, 50px)` | 800 | letter-spacing -0.03em |
| Section H2 (feature-tabs-head) | `clamp(28px, 5.5vw, 52px)` | 800 | line-height 1.02, letter-spacing -0.03em |
| Feature-tabs panel H3 | `clamp(28px, 4.6vw, 50px)` | 800 | color `--ink`, line-height 1.04 |
| Eyebrow / section-eyebrow | `clamp(12px, 1.5vw, 14px)` | 700 | letter-spacing 0.12em, uppercase, color `--blue-600` |
| Lead/body paragraph | `17–19px` | 400 | color `--ink` (not gray — see Usage conventions above), line-height 1.6 |
| Nav links | `15px` | 700 | color `--gray-600` |
| Nav CTA button | `14px` | 700 | |
| Header logo | `clamp(20px, 4vw, 24px)` | — | |
| Footer logo | `clamp(28px, 5vw, 34px)` | — | intentionally bigger than header logo (closing brand moment) |

---

## Layout / spacing

| Context | max-width |
|---|---|
| Base `.wrap` (all pages) | `1080px`, padding `0 clamp(20px, 5vw, 48px)` |
| Header `.wrap` | `none` (full-bleed), own gutter `14px clamp(22px, 6vw, 42px)` |
| Footer `.wrap` | `1080px` (same as base — redundant but harmless) |
| Article/doc reading column | `680px` |
| Mentorship-teaser / FAQ-teaser (index.html) | `680px` / `480px` — intentionally narrow, short punchy sections |

**Breakpoints:** `720px` (nav collapses to hamburger menu), `640px` (hero/type-size mobile overrides, mobile-only tweaks like the horizontally-scrolling feature-tab row).

**Section padding:** `clamp(56px, 9vw, 110px) 0` — fluid, replaces the old flat `96px`/`64px` split.

---

## Buttons

All buttons use the same **hollow/fill hover** language site-wide, matching Gather's closing-CTA pattern: solid buttons hollow out to an outline on hover, outline buttons fill solid on hover. Every button needs a `2px`/`1.5px` border on its *base* state (even if transparent) so hover doesn't shift layout.

| Class | Base | Hover |
|---|---|---|
| `.cta-primary` | bg `--blue-600`, white text, border `2px solid --blue-600`, padding `16px 32px`, radius `999px`, shadow `0 8px 24px rgba(37,99,235,.28)` | Hollows: transparent bg, `--blue-600` text+border, `translateY(-2px)`, shadow removed |
| `.nav-cta` | bg `--blue-600`, white text, border `2px solid --blue-600`, padding `9px 18px`, radius `999px`, `transition: all .6s ease` | Hollows: transparent bg, `--blue-600` text+border, `translateY(-1px)` |
| `.cta-outline` | transparent bg, `--blue-600` text, border `1.5px solid --blue-200`, padding `16px 32px`, radius `999px` | Fills: `--blue-600` bg+border, white text |
| `.final-cta .cta-primary` (index.html, scoped) | white bg, `--blue-600` text+border (inverted base, since the section itself is blue-600) | Hollows: transparent bg, white text+border |

**Rule:** if you add a new button variant, it must follow this hollow/fill convention — never a plain darken-on-hover. This was a real, repeated bug this session (`.nav-cta` on 12 of 13 pages only darkened on hover; had to be brought in line with index.html's original).

---

## Header / Footer

**Header:** sticky, `backdrop-filter: blur(12px)`, background `rgba(255,255,255,.85)`, logo height `clamp(20px, 4vw, 24px)`, gutter `clamp(22px, 6vw, 42px)`, nav item gap `26px`. Mobile (≤720px): hamburger toggle replaces nav, drops down all 5 links + Sign Up.

**Footer:** background gradient `linear-gradient(180deg, var(--ink) 0%, var(--gray-700) 100%)`, wrap capped at `1080px`, grid `2fr 1fr 1fr 1fr` with `40px` gap, logo height `clamp(28px, 5vw, 34px)` (recolored white via `fill` override on the SVG paths — the logo's "T" is a `<polygon>`, not a `<path>`, so any recolor rule must include `polygon` or it silently stays black).

**`.brand` / `.footer-brand .brand`:** no `opacity` styling — removed earlier this session per explicit instruction (opacity was dimming the near-black logo fill, making it look gray instead of solid black). Don't reintroduce it.

---

## Known deliberate exceptions

- Article/doc pages use a narrower `680px` reading column instead of the `1080px` section width — intentional, long-form text needs a shorter line length.
- Footer logo (`clamp(28,5vw,34)`) is bigger than header logo (`clamp(20,4vw,24)`) — a real measured reference (try-gather.co) uses `70px` footer vs `30px` header, a much bigger jump than ours; we scaled it down since our wordmark's aspect ratio is much wider than their compact script logo, but kept the same "bigger in the footer" direction.
- `.tab-panels` on index.html has its own `max-width: 1200px` — currently moot/dead since its parent `.wrap` already caps at 1080px, so it never actually applies. Harmless, not worth removing.

---

## Known past bugs (don't reintroduce)

- **`.site-nav a` without `:not(.nav-cta)`** — on faq.html only, this made the Sign Up button's text render `--gray-600` (and `--ink` on hover) instead of white, because `.site-nav a` (specificity 0,1,1) beat `.nav-cta`'s own `color: white` (specificity 0,1,0). Every nav-link selector styling `.site-nav a` must exclude `.nav-cta` or use higher specificity.
- **Missing mobile gutter** — `.article-head`/`.article-body`/`.article-cta` (blog posts) and `.doc-head`/`.doc-body` (privacy/terms) all sat directly in `<main>` with no `.wrap` and no padding of their own. Fine above their own `max-width` (680px), but ran text edge-to-edge on any phone. If you add a new page pattern, make sure it either sits inside `.wrap` or has its own `padding: Ny clamp(20px, 5vw, 48px) Nx` — never `padding: Ny 0 Nx`.
- **Card touching the screen edge** — `.article-cta` (a bordered/background card, not just text) needed `width: calc(100% - 2 * clamp(20px, 5vw, 48px))` alongside `max-width` + `margin: 0 auto`, not just padding — padding on a card pushes its *interior* content, not the card's outer edge away from the viewport.

---

*Generated from a full audit of all 13 HTML files. Last verified: this session (post Gather-alignment pass, mobile-gutter fixes, and hollow/fill hover rollout). If you add a 14th page or change a canonical value, update this file too — it's a snapshot, not enforced by tooling.*
