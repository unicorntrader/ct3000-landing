#!/usr/bin/env python3
"""
Keeps the header and footer blocks byte-identical across all 13 pages.

This is NOT part of the deploy pipeline -- GitHub Pages still serves the
committed HTML directly, unchanged. Run this locally after editing the
header/footer template below, then commit the regenerated files like any
other edit. It exists purely to stop the "fixed 12 of 13 files" class of
bug (see DESIGN-SYSTEM.md "Known past bugs").

Usage:
    python3 sync-shared.py            # rewrite header+footer in all pages
    python3 sync-shared.py --check    # exit 1 if any page would change
"""
import re
import sys

LOGO_SVG = '''<svg viewBox="0 0 685.29 120.16" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CT3000">
          <path fill="#231f20" d="M98.96,0H21.2C9.49,0,0,9.49,0,21.2v77.76C0,110.67,9.49,120.16,21.2,120.16h77.76c11.71,0,21.2-9.49,21.2-21.2V21.2c0-11.71-9.49-21.2-21.2-21.2ZM98.96,28.53v70.43h-21.2v-26.94c0-5.4-6.53-8.1-10.34-4.28l-31.23,31.23h-14.99v-14.99l31.23-31.23c3.82-3.82,1.11-10.34-4.28-10.34h-26.94v-21.2h70.43c4.05,0,7.33,3.28,7.33,7.33h0Z"/>
          <circle fill="#231f20" cx="77.76" cy="42.4" r="10.6"/>
          <path fill="#231f20" d="M200.79,3.75h-39c-11.35,0-20.58,9.23-20.58,20.58v71.52c0,11.35,9.23,20.58,20.58,20.58h39c11.35,0,20.58-9.23,20.58-20.58v-20.58h-21.65v16.94c0,1.41-1.15,2.56-2.56,2.56h-31.73c-1.41,0-2.56-1.15-2.56-2.56V27.96c0-1.41,1.15-2.56,2.56-2.56h31.73c1.41,0,2.56,1.15,2.56,2.56v16.94h21.65v-20.58c0-11.35-9.23-20.58-20.58-20.58Z"/>
          <polygon fill="#231f20" points="232.61 25.4 259.36 25.4 259.36 116.42 281.01 116.42 281.01 25.4 307.75 25.4 307.75 3.75 232.61 3.75 232.61 25.4"/>
          <path fill="#231f20" d="M378.57,3.75h-39c-11.35,0-20.58,9.23-20.58,20.58v20.58h21.65v-16.9c0-1.43,1.17-2.6,2.6-2.6h31.65c1.43,0,2.6,1.17,2.6,2.6v18.66c0,1.43-1.17,2.6-2.6,2.6h-24.41v21.65h24.41c1.43,0,2.6,1.17,2.6,2.6v18.66c0,1.43-1.17,2.6-2.6,2.6h-31.65c-1.43,0-2.6-1.17-2.6-2.6v-16.9h-21.65v20.58c0,11.35,9.23,20.58,20.58,20.58h39c11.35,0,20.58-9.23,20.58-20.58v-19.5c0-8.07-4.74-13.95-12.58-16.26,7.84-2.31,12.58-8.19,12.58-16.26v-19.5c0-11.35-9.23-20.58-20.58-20.58ZM378.57,60.08h0,0Z"/>
          <path fill="#231f20" d="M473.96,3.75h-39c-11.35,0-20.58,9.23-20.58,20.58v71.52c0,11.35,9.23,20.58,20.58,20.58h39c11.35,0,20.58-9.23,20.58-20.58V24.32c0-11.35-9.23-20.58-20.58-20.58ZM472.88,27.98v64.21c0,1.42-1.16,2.57-2.57,2.57h-31.69c-1.42,0-2.57-1.16-2.57-2.57V27.98c0-1.42,1.16-2.57,2.57-2.57h31.69c1.42,0,2.57,1.16,2.57,2.57Z"/>
          <path fill="#231f20" d="M569.34,3.75h-39c-11.35,0-20.58,9.23-20.58,20.58v71.52c0,11.35,9.23,20.58,20.58,20.58h39c11.35,0,20.58-9.23,20.58-20.58V24.32c0-11.35-9.23-20.58-20.58-20.58ZM568.26,27.98v64.21c0,1.42-1.16,2.57-2.57,2.57h-31.69c-1.42,0-2.57-1.16-2.57-2.57V27.98c0-1.42,1.16-2.57,2.57-2.57h31.69c1.42,0,2.57,1.16,2.57,2.57Z"/>
          <path fill="#231f20" d="M664.72,3.75h-39c-11.35,0-20.58,9.23-20.58,20.58v71.52c0,11.35,9.23,20.58,20.58,20.58h39c11.35,0,20.58-9.23,20.58-20.58V24.32c0-11.35-9.23-20.58-20.58-20.58ZM663.64,27.98v64.21c0,1.42-1.16,2.57-2.57,2.57h-31.69c-1.42,0-2.57-1.16-2.57-2.57V27.98c0-1.42,1.16-2.57,2.57-2.57h31.69c1.42,0,2.57,1.16,2.57,2.57Z"/>
        </svg>'''


def cls(active):
    return ' class="current"' if active else ''


def build_header(how_it_works_href, nav_current):
    """nav_current: 'faq' | 'blog' | 'mentorship' | None"""
    faq_c = cls(nav_current == 'faq')
    blog_c = cls(nav_current == 'blog')
    ment_c = cls(nav_current == 'mentorship')
    links = f'''<a href="{how_it_works_href}">How it works</a>
        <a href="/faq"{faq_c}>FAQ</a>
        <a href="/blog"{blog_c}>Blog</a>
        <a href="/mentorship"{ment_c}>Mentorship</a>
        <a href="https://cotrader3000.com/subscribe" class="nav-cta">Find my edge</a>'''
    return f'''<header class="site-header">
    <div class="wrap">
      <a href="/" class="brand">
        {LOGO_SVG}
      </a>
      <nav class="site-nav">
        {links}
      </nav>
      <button class="menu-toggle" aria-label="Menu" aria-expanded="false">
        <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
      </button>
    </div>
    <nav class="mobile-menu">
      {links}
    </nav>
  </header>'''


def build_footer(how_it_works_href, legal_current):
    """legal_current: 'privacy' | 'terms' | None"""
    priv_c = cls(legal_current == 'privacy')
    terms_c = cls(legal_current == 'terms')
    return f'''<footer class="site-footer">
    <div class="wrap">
      <div class="footer-inner">
        <div class="footer-brand">
          <a href="/" class="brand">
            {LOGO_SVG}
          </a>
          <p>Know your edge.</p>
          <a href="mailto:thinker@philoinvestor.com" class="footer-email">thinker@philoinvestor.com</a>
        </div>
        <div class="footer-col">
          <h5>Links</h5>
          <a href="{how_it_works_href}">How it works</a>
          <a href="/faq">FAQ</a>
          <a href="/blog">Blog</a>
          <a href="/mentorship">Mentorship</a>
        </div>
        <div class="footer-col">
          <h5>Legal</h5>
          <a href="/privacy"{priv_c}>Privacy</a>
          <a href="/terms"{terms_c}>Terms</a>
        </div>
        <div class="footer-col">
          <h5>Guides</h5>
          <a href="/blog">All guides</a>
          <a href="/blog-connecting-ibkr">Connecting IBKR</a>
          <a href="/blog-overtrading">Why traders overtrade</a>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; 2026 CoTrader 3000. All rights reserved.</span>
        <span class="footer-bottom-links">
          <a href="/privacy">Privacy</a>
          <a href="/terms">Terms</a>
        </span>
      </div>
    </div>
  </footer>'''


# filename -> (nav_current, legal_current)
PAGES = {
    'index.html':               (None, None),
    'faq.html':                 ('faq', None),
    'blog.html':                ('blog', None),
    'blog-callouts.html':       ('blog', None),
    'blog-connecting-ibkr.html':('blog', None),
    'blog-first-week.html':     ('blog', None),
    'blog-icarus.html':         ('blog', None),
    'blog-overtrading.html':    ('blog', None),
    'blog-revenge-trading.html':('blog', None),
    'blog-trade-plan.html':     ('blog', None),
    'blog-weekly-review.html':  ('blog', None),
    'mentorship.html':          ('mentorship', None),
    'privacy.html':             (None, 'privacy'),
    'terms.html':                (None, 'terms'),
}

HEADER_RE = re.compile(r'<header class="site-header">.*?</header>', re.DOTALL)
FOOTER_RE = re.compile(r'<footer class="site-footer">.*?</footer>', re.DOTALL)


def main():
    check_only = '--check' in sys.argv
    changed = []
    for fname, (nav_current, legal_current) in PAGES.items():
        is_home = fname == 'index.html'
        how_it_works_href = '#plans' if is_home else '/#plans'
        header = build_header(how_it_works_href, nav_current)
        footer = build_footer(how_it_works_href, legal_current)

        with open(fname, encoding='utf-8') as f:
            content = f.read()

        new_content = HEADER_RE.sub(lambda m: header, content, count=1)
        new_content = FOOTER_RE.sub(lambda m: footer, new_content, count=1)

        if new_content != content:
            changed.append(fname)
            if not check_only:
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(new_content)

    if check_only:
        if changed:
            print('Out of sync:', ', '.join(changed))
            sys.exit(1)
        print('All pages in sync.')
    else:
        print(f'Synced. Changed: {changed if changed else "none"}')


if __name__ == '__main__':
    main()
