# DocuDex Automation - NCC (Playwright)

Python + Playwright port of the original Selenium scripts in
`DocuDex Automation-NCC`. Same login flows, same button clicks, same workflow
steps — just driven by Playwright instead of Selenium/webdriver-manager.

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

(Already done once in this environment — Chromium is installed under
`%LOCALAPPDATA%\ms-playwright`.)

## Shared helpers — `common.py`

Every script imports from `common.py`, which holds:

- `new_page()` — launches Chromium (headed) and yields a `Page` with JS
  alerts/confirms auto-accepted (replaces every `WebDriverWait(...).until(EC.alert_is_present())`
  block from the original scripts).
- `login()` / `force_logout()`
- `initiate_account_opening_workflow()` — the full "start Account Opening
  Process (Non-Individual) -> fill form -> upload AOF document -> proceed to
  Step-2" sequence shared verbatim by `workflow_initiate.py`,
  `workflow_reassign.py`, `workflow_releaseToGroup.py`, `workflow_sendBack.py`
  and `workflow_skip.py` in the original scripts.
- Smaller step helpers (`accept_and_confirm`, `click_proceed_forward`,
  `upload_and_create_tp_document`, `edit_properties_and_extend_expiry`, ...)
  reused across the workflow / document-property scripts.
- `PDF_DIR` / `OCR_DIR` — point at `./Demo file Upload for Testing/...`,
  copied next to this README so the scripts are self-contained (the original
  scripts hardcoded `C:\Users\Devnet\Desktop\...`, a path from a different
  machine).

## Running a script

Each script is still standalone, exactly like the original Selenium ones:

```bash
python login.py
python workflow_initiate.py
python workflow_2nd_Step.py
...
```

`workflow_initiate.py` (and the scripts that call
`initiate_account_opening_workflow`) write the generated tracking number to
`tracking_no.txt`; `workflow_2nd_Step.py` / `3rd_Step.py` / `4th_Step.py`
read it back from there, same as before.

## Notes

- Credentials and the server URL (`http://203.76.124.126:5058`) are kept
  as-is from the original scripts (see `common.py` / each script's `login()`
  call) — change them there if the environment changes.
- Browser runs headed (`headless=False`) by default so you can watch it,
  matching the original scripts' `input("Check UI. Press Enter to close
  browser...")` pause at the end.
