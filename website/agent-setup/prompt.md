These are instructions from Function Store for setting up a coding agent to work with FNSTools, a toolkit of TouchDesigner components (https://functionstore.tools). They install the FNSTools agent skill: a folder of plain text pages, generated from the toolkit at every release, that tells an agent what each installed package is, how it is reached from code, its promoted methods, its quick-launch commands, hotkeys and settings.

Complete the steps yourself by running the commands directly. Do not ask the user to run them. Nothing here needs TouchDesigner to be open or FNSTools to be installed; the skill describes the current release either way.

- Install the FNSTools agent skill
- (Other agents) point your instructions file at it

---

## Decide the scope

The skill goes into the project the user is working in, at `.claude/skills/fnstools/`, unless the user asked for it on every project on the machine; then it goes to `~/.claude/skills/fnstools/`. Use the project scope when nothing was said. Run the script below from the project folder, or pass the folder as `--project <path>`.

## Install the FNSTools agent skill

Run this with Python 3 (standard library only; keep the User-Agent header, the release bucket refuses the default one). It reads the release manifest, downloads the skill document the manifest names, checks its SHA-256 against the manifest, and writes the files. It is idempotent: an older copy is replaced, the same release is reported as current, a newer copy is kept.

```python
import hashlib, json, os, shutil, sys, urllib.request
from pathlib import Path

WELL_KNOWN = 'https://functionstore.tools/.well-known/fnstools.json'
args = sys.argv[1:]
scope = 'user' if '--user' in args else 'project'
project = Path(args[args.index('--project') + 1]) if '--project' in args else Path.cwd()
base = Path.home() if scope == 'user' else project
dest = base / '.claude' / 'skills' / 'fnstools'

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'fnstools-agent-setup/1'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

endpoints = json.loads(get(WELL_KNOWN))['endpoints']
manifest = json.loads(get(endpoints['manifest'].rstrip('/') + '/manifest.json'))
skill = manifest.get('agent_skill')
if not skill:
    sys.exit('this release carries no agent skill yet; nothing installed')
raw = get(skill['url'])
digest = hashlib.sha256(raw).hexdigest()
if digest != skill['sha256']:
    sys.exit('agent-skill.json does not match the manifest (sha256 %s, expected %s); nothing installed'
             % (digest[:12], skill['sha256'][:12]))
doc = json.loads(raw)
files, want = doc['files'], doc['version']

def num(v):
    return tuple(int(p) for p in v.strip().lstrip('v').split('.') if p.isdigit())

have = (dest / 'VERSION').read_text(encoding='utf-8').strip() if (dest / 'VERSION').is_file() else ''
if have and num(have) > num(want):
    state = 'kept newer copy %s' % have
elif have == want and all((dest / p).is_file() and (dest / p).read_text(encoding='utf-8') == t
                          for p, t in files.items()):
    state = 'current'
else:
    if dest.is_dir():
        shutil.rmtree(dest)
    for rel, text in files.items():
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
    state = 'installed' if not have else ('refreshed' if have == want else 'updated from %s' % have)
print('FNSTools agent skill %s: %s at %s (%d files, sha256 verified)' % (want, state, dest, len(files)))
```

Save it to a temporary file and run it: `python3 setup_fnstools_skill.py` for the project scope, `python3 setup_fnstools_skill.py --user` for the user scope. On Windows the interpreter may be `python` or `py -3`.

If Python 3 is not available, do the same four steps with whatever runtime you have: read `endpoints.manifest` from the well-known file, read `agent_skill` from `<that>/manifest.json`, download `agent_skill.url` and verify its SHA-256 against `agent_skill.sha256`, then write every entry of the document's `files` map (path to text) under the destination folder.

Do not add the folder to `.gitignore` or commit it; whether the skill is tracked is the user's decision.

## Claude Code

Nothing more to do. Claude Code reads `.claude/skills/fnstools/SKILL.md` from the project, or `~/.claude/skills/fnstools/SKILL.md` for the user scope, and loads it when the conversation turns to FNSTools, an `FNS_` COMP or an `op.FNS_*` shortcut. A session that was already open when the folder arrived may need to be restarted to list it.

## Other agents

The skill is plain markdown in the Agent Skills layout (`SKILL.md` with frontmatter, `references/` beside it). For an agent that reads skills from a different folder, copy or link `fnstools/` there. For an agent that reads `AGENTS.md`, append this block to the project's `AGENTS.md` once (skip it when the marker line is already in the file):

```markdown

<!-- fnstools-agent-skill -->
## FNSTools

This TouchDesigner project uses the FNSTools toolkit. The agent skill describing it (packages, shortcuts, promoted methods, quick-launch commands, registries) is at `.claude/skills/fnstools/SKILL.md`; read it before driving an `FNS_` COMP or an `op.FNS_*` shortcut.
```

Do not edit any other instructions file unless the user asks.

## When TouchDesigner is open

The toolkit carries the same installer as a quick-launch command: **Install agent skill**, or `op.FNS_UPDATER.InstallAgentSkill()` in the Textport (`InstallAgentSkill('user')` for the user scope, `agents_md=True` for the block above). It installs from the machine's copy of the skill, so it works offline. Either route may be used; both agree on `VERSION`.

---

## Report

Print this when done, with the real values:

```
FNSTools agent setup complete

  Skill    <destination folder>   <release from VERSION>   <installed | current | updated from ... | kept newer copy ...>
  Verified SHA-256 against the release manifest

Mention FNSTools, a tool name or an op.FNS_ shortcut and the agent reads the skill.
```

## About these instructions

- Published at https://functionstore.tools/agent-setup/prompt.md, so they can be re-read at any time. They name no release; the release comes from the manifest.
- Integrity is the SHA-256 the release manifest carries for `agent-skill.json`, fetched over HTTPS from the release bucket the well-known file names. The script checks nothing beyond that.
- The skill covers every public package of the current release, whether or not it is installed on this machine; each package page names the access tier it needs.
- Docs: https://functionstore.tools/docs/guides/agent-skill/ (the skill), https://functionstore.tools/llms.txt (rules for agents in a project that uses FNSTools).
