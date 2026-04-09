# VCR Chrome Extension — Build TODO

The Python pipeline (`main.py` + 7 modules) is the source of truth. The Chrome
extension is a thin shell around it. Plan:

## Architecture

```
[Chrome page]  <-->  [Content script]  <-->  [Popup UI]
                            |
                            v
                  [Local Flask server :5000]
                            |
                            v
                   [Existing Python pipeline]
```

Reason for Flask: the pipeline is ~3,500 lines of NumPy/lxml/Pillow. Rewriting
in JS is a separate project. A localhost Flask process is the fastest path to
a working extension and matches the "Python tool + Chrome extension" claim in
the thesis intro.

## Flask server (`server/app.py`)

- [ ] Wrap existing pipeline in a Flask app on `localhost:5000`.
- [ ] Endpoints:
  - `POST /detect`  → input: `{svg: "<svg>...</svg>", cvd_type}`
                      output: `{palette_type, n_colors, mismatch: bool,
                                candidates: [{name, meta, colors|stops}],
                                color_mapping: {orig_hex: new_hex, ...}}`
  - `POST /repair`  → same as detect but returns the chosen candidate's full
                      mapping (used when user cycles palettes).
- [ ] CORS: allow `chrome-extension://<id>` origin.
- [ ] Cache results per SVG hash so cycling palettes is instant.
- [ ] Run instructions in `server/README.md`: `pip install -r requirements.txt`
      then `python app.py`.

## Chrome extension (`extension/`)

- [ ] `manifest.json` (MV3): `activeTab`, `scripting`,
      `host_permissions: ["http://localhost:5000/*"]`.
- [ ] `popup.html` — already built (`extension_mockup.html`); rename and split
      inline `<script>`/`<style>` into `popup.js` / `popup.css` (MV3 forbids
      inline scripts).
- [ ] `popup.js`:
  - On open, message content script → get list of detected SVGs.
  - For each SVG, call `/detect` and populate the SVG dropdown + swatches.
  - Toggle / palette nav → message content script with `{svgId, mapping}`.
- [ ] `content.js`:
  - On load, find all `<svg>` nodes containing fill colors (skip tiny icons).
  - Maintain a `Map<svgId, Map<element, originalFill>>` so toggle-off restores.
  - Apply mapping by walking each SVG and rewriting `fill=` / `style.fill`
    on data-mark elements only (server tells us which).
- [ ] Background service worker only if we need it for fetch routing.

## Open questions / risks

- [ ] How to identify "data marks" vs axes from the content script side?
      Two options: (a) server returns a list of CSS selectors / element paths
      to recolor, (b) server returns a `{originalHex → newHex}` map and the
      content script swaps every matching fill. Option (b) is simpler but
      could recolor a non-data element that happens to share a color.
      Start with (b), revisit if it causes problems.
- [ ] Multi-SVG pages: do we run pipeline on all of them at popup-open time
      (slow) or lazily on selection (laggy)? Probably batch in background.
- [ ] CVD-type switch: re-run `/detect` from scratch since simulation matrices
      change.
- [ ] Spot-check flow (DR5): out of scope for v1, can be a static page.
- [ ] D3/Vega charts may re-render on hover/resize and overwrite our fills.
      Mitigation: attach a `MutationObserver` per SVG that re-applies the
      cached mapping whenever a watched node's fill changes. Decide whether
      this is v1 or v2.

## Out of scope for v1

- Porting pipeline to JS/WASM (mentioned as future work in Ch 6).
- Bivariate palette repair.
- Tritanopia (pipeline supports it; UI just needs the option enabled).
- Persisting user choices across sessions.
