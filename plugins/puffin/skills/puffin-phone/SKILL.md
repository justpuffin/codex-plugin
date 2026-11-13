---
name: puffin-phone
description: Set up or check Codex from your phone - the user messages their Puffin agent from Telegram, Slack, Discord or email, and Codex works in a project on this machine, asking in the same chat before each command or file change. Use when the user asks to code from their phone, control Codex remotely, or check the Puffin gateway.
---

# Codex from your phone

Puffin's gateway (`puffin codex`) turns the user's own messages to their Puffin agent into turns in a Codex thread in a project folder. Codex works in a read-only sandbox; every command that needs more and every file change becomes an Allow / Reject prompt in the user's chat, and Codex's answer is posted back there.

Keep each reply short and plain.

1. Check whether the `puffin` command exists (`puffin --help`). If not, tell the user to run the installer in their own terminal (it asks for the project folder), with the one-time code from the agent's page in Puffin:
   - Mac or Linux: `curl -fsSL https://www.justpuffin.tech/install/codex.sh | bash -s -- --code <CODE>`
   - Windows (PowerShell): `$env:PUFFIN_SETUP_CODE="<CODE>"; irm https://www.justpuffin.tech/install/codex.ps1 | iex`

   The code comes from the agent's page: **Coding from your phone** → choose **Codex** → **Turn on** → **Get setup command**. It works once, for 15 minutes.
2. If `puffin` exists, run `puffin codex status` and `puffin codex doctor`, and explain each `FIX` line with the exact command or dashboard step.
3. If it is installed but not set up, tell the user to run `puffin codex setup --code <CODE>` in their own terminal, then `puffin codex start`.
4. When everything is `ok`, tell them to message the agent from their phone. In the chat, `new` starts a fresh thread and `status` shows what's running.

Never ask the user to paste an API key or setup code into this conversation, and don't run the setup yourself.
