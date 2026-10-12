---
status: open
summary: Search visibility for functionstore.tools. The site was crawlable but had no sitemap, no robots.txt, no structured data, and titles without the word TouchDesigner; the build now emits all four, and the share image no longer shows the old domain. What is left is off-site work only the owner can do (Search Console, Bing, backlinks) and a copy pass on short descriptions.
since: 2026-10-10
verified: 2026-10-10, local build: 108 pages and 108 sitemap URLs with none missing either way, 103 JSON-LD blocks parse, tests/test_site_search.py green
---

# Search visibility for functionstore.tools

Asked 2026-10-09: is the site indexable by Google and the rest? It was
crawlable, and no search engine we could query returned a single page from
it. This is the list of what was wrong, what the site build now does about
it, and what is left for the owner. Entries are corrected in place when a
finding changes.

## Where it stood (measured 2026-10-09)

- Every page is static HTML, answers 200 and sends no `X-Robots-Tag`.
  Generated pages carry `robots: index, follow` and a canonical URL.
- `http://` and `www.` both 308 to `https://functionstore.tools/`, so
  each page has one address.
- The landing page links 87 tool pages and `/docs/` links every page, so
  a crawler that reaches the home page reaches everything.
- Across 108 built pages: every page has a canonical, exactly one `<h1>`,
  and no `<img>` without `alt`.
- `/robots.txt` and `/sitemap.xml`: 404 on functionstore.tools and on
  seq.functionstore.tools.
- No structured data, no `og:url`, no Twitter card on any page.
- 102 of 108 titles do not contain "TouchDesigner", which is the word
  people search with ("touchdesigner midi mapper").
- A plain search and a `site:functionstore.tools` search returned no page
  from the domain. Results for the toolkit point at the Derivative asset
  post and Interactive & Immersive HQ articles. That search engine is not
  Google, so Search Console is the real check.

## Built into the site (website/tools/build-site.mjs)

1. **`/sitemap.xml`**: every page the build writes, collected from the
   canonical URL each page is given, plus the landing page. No `lastmod`:
   Vercel builds from a fresh clone, so file times are the clone time, and a
   date that is always "today" teaches Google to ignore the field.
2. **`/robots.txt`**: allows everything and names the sitemap. Corrected
   before it shipped: the first plan disallowed `/docs/pagefind/`, but
   every docs page loads `pagefind-ui.css` and `pagefind-ui.js` from there,
   and Google asks sites not to block the CSS and JS a page renders with.
   The index fragments are only fetched when someone types a search, which
   a crawler does not, so there was nothing to save.
3. **Titles say TouchDesigner.** Tool pages read
   `ColorGen for TouchDesigner | FNSTools docs`, guides
   `Getting started | FNSTools for TouchDesigner`, and the docs index
   `FNSTools docs: every TouchDesigner tool in the toolkit`. A title that
   already contains the word is left alone.
4. **Sharing tags on every page**: `og:url`, `og:site_name`, the image
   size and alt text, and `twitter:card` set to `summary_large_image`, on
   the generated pages, `/get/` and the landing page.
5. **Structured data (JSON-LD)**:
   - Landing page: `WebSite` (name FNSTools, the name Google shows above
     the result) and `Organization` (Function Store, logo, and the GitHub,
     Patreon, YouTube and Instagram profiles).
   - Tool pages, guides and community posts: `BreadcrumbList`
     (Docs, category, page), which Google shows in place of the bare URL.
6. **Community drafts stay out.** A draft is only built when
   `FNS_SHOW_DRAFTS=1` (the CMS preview); such a page gets `noindex` and is
   left out of the sitemap, so a local preview build can never list one.
   No row is a draft today, so this path is pinned by the test and has not
   run on a real draft.
7. **The share image said the old domain.** `og-image.png` still read
   `tools.functionstore.xyz`: the domain migration (efe891e0) fixed the text
   in `make-brand-assets.py` and never re-ran it. Regenerated; the favicon
   came out pixel-identical and was left as committed. The image URL now
   carries a content hash (`og-image.png?v=...`) because link previews cache
   by URL and would keep showing the old picture.
8. **Fixed on the way:** a community post whose own title names its author
   got the author twice ("Pathtracer by Josef Pelz by Josef Pelz").

`tests/test_site_search.py` pins the wiring, and after `npm run build` it
also checks the output: every indexable page in the sitemap and nothing
else, canonical and `og:url` equal on every page, every JSON-LD block
parses.

### Considered and left out

- **`SoftwareApplication` on each tool page.** Google's software app
  result requires `aggregateRating` or `review`. The toolkit has neither,
  and inventing them breaks Google's structured data policy. Without them
  Search Console reports every tool page as an invalid item, which is noise
  in the one report the owner will read.
- **Sitelinks search box** (`WebSite` with a `SearchAction`). Google
  retired it in late 2024.

## For the owner (off-site, cannot be done from the repo)

9. **Google Search Console.** Add functionstore.tools as a Domain property
   (a DNS TXT record at the registrar), submit
   `https://functionstore.tools/sitemap.xml`, then URL Inspection, Request
   indexing on `/` and `/docs/`. This is also where you find out whether
   Google has indexed anything and why not.
10. **Bing Webmaster Tools.** Import the site from Search Console (one
   click once step 9 is done). Bing's index also feeds DuckDuckGo, Yahoo and
   ChatGPT search.
11. **Links pointing at the site.** Google finds and trusts a new domain
   through links to it. The GitHub repo's homepage field already points
   here. Missing: the Derivative asset post
   (derivative.ca/community-post/asset/68350), the functionstore.xyz home
   page and link-in-bio, the Patreon about section, and YouTube video
   descriptions.
12. **seq.functionstore.tools** has the same gaps (no robots.txt, no
    sitemap). Its source is `C:/VJ/TD/Projects/OpSeqDev/web`, a separate
    repo; a `public/robots.txt` and `public/sitemap.xml` there would cover
    it.

## Copy (owner's call)

13. **Short descriptions.** Eleven pages have a meta description under 70
    characters, which gives Google little to show: community/pathtracer,
    community/qr-code-comp, fns-altselect, fns-borderlesstd,
    fns-globalvolcontrol (28), fns-openext, fns-optemplates,
    fns-parrandomizer, fns-quickpane (22), fns-swapops,
    guides/getting-started. Tool descriptions live in
    `packaging/catalog.json` and also feed the picker, so this is a copy
    pass through the CMS.
14. Fifty-one descriptions run past 160 characters. Google cuts them in the
    result; nothing else happens, so they stay.

## Later

15. **IndexNow**: a ping to Bing on each deploy so changed pages are
    recrawled within hours. Needs a key file served from the site.
16. **`/llms.txt`** is committed (46122517) and answers 404 on the live
    site: the release mirror since then did not carry it. It goes out with
    the next `publish_public.py --only website` run.

## Appendix: probes

```
curl -sI https://functionstore.tools/robots.txt     -> 404
curl -sI https://functionstore.tools/sitemap.xml    -> 404
curl -sI https://functionstore.tools/docs/colorgen/ -> 200, no X-Robots-Tag
curl -sI http://functionstore.tools/                -> 308 https://functionstore.tools/
curl -sI https://www.functionstore.tools/           -> 308 https://functionstore.tools/
curl -sI https://seq.functionstore.tools/robots.txt -> 404
curl -sI https://functionstore.tools/llms.txt       -> 404
```
