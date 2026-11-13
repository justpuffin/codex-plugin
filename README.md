# Puffin for Codex

Give Codex its own **Puffin agent**: an email address, Slack, Discord and Telegram chats, texts, contacts, memories, a calendar and tasks. Every message it sends waits for your approval. Then step away from the keyboard and keep working with it **from your phone**.

`Email` · `Slack` · `Discord` · `Telegram` · `Texts` · `Calendar` · `Approvals`

| | What it does | Install |
|---|---|---|
| **Puffin tools in Codex** | Codex reads and searches the agent's inbox and chats, drafts and sends (with approval), looks up contacts, books meetings and hands off tasks | `codex plugin marketplace add justpuffin/codex-plugin`, then add the Puffin plugin |
| **Codex from your phone** | You message your agent from Telegram, Slack, Discord or email. Codex works in your project on your machine, asks you in the same chat before each command or file change (**Allow / Reject**), and replies there | One command with a setup code from the agent's page (below) |

## Puffin tools in Codex

```bash
codex plugin marketplace add justpuffin/codex-plugin
```

Then add **Puffin** from the plugin list. The first time Codex uses a Puffin tool, it opens Puffin in your browser: sign in (or create an account), pick the agent Codex should act as, choose what it may do and click **Allow**. No API key is copied. Disconnect any time in Puffin: **Developer tools → Connected apps**.

Using the Codex CLI without plugins? Append [`config.toml`](config.toml) to `~/.codex/config.toml`, then either set `PUFFIN_API_KEY` to a key from **API keys** in Puffin, or remove the `bearer_token_env_var` line and run `codex mcp login puffin`.

Then just ask: "What's new in my agent's inbox?", "Reply to Priya: Thursday at 3 works", "Book 30 minutes with Raj on Friday". Sends, replies and calendar invites wait for your approval in Puffin, or as **Approve / Reject** buttons in your linked chat.

## Codex from your phone

```
you (phone) ── Telegram / Slack / Discord / email ──▶ Puffin ──▶ puffin codex (your machine)
                                                                      │
                                                     codex app-server in your project
                                                     (asks you before each command or file change)
```

1. In Puffin, open the agent's page → **Coding from your phone** → choose **Codex** → **Turn on** → **Get setup command**.
2. Run the command on the computer that has your project. It needs Codex installed and signed in (`npm install -g @openai/codex`, then `codex login`), and Python 3.10+:

   ```bash
   # Mac or Linux
   curl -fsSL https://www.justpuffin.tech/install/codex.sh | bash -s -- --code ABCDE-FGHJK
   ```

   ```powershell
   # Windows (PowerShell)
   $env:PUFFIN_SETUP_CODE="ABCDE-FGHJK"; irm https://www.justpuffin.tech/install/codex.ps1 | iex
   ```

   The code works once, for 15 minutes. The installer exchanges it for this agent's own key (saved only on your machine), asks for your project folder, and starts the gateway in the background.
3. Link your chat account on Puffin's **Team** page (send `link <code>` to the bot), then message the agent: "the login test fails, fix it".

What you'll see:

```
Agent: Working on it in shop…
Agent: 🔐 Codex wants to run a command:
       bash -lc 'npm test'
       [Allow] [Reject]
Agent: 🔐 Codex wants to change files:
       update src/login.ts
         -if (token)
         +if (!token)
       [Allow] [Reject]
Agent: Fixed: the token check was inverted. All 42 tests pass.
```

How it works:

- The gateway runs `codex app-server` in your project. Each chat or email thread is one Codex thread that later messages continue (12 hours); send `new` to start fresh and `status` to see what's running.
- Codex runs in a **read-only sandbox** with approvals **on request**: every command that needs more and every file change is relayed to you, and your answer goes straight back to Codex. Commands you list at setup (like `npm test`) run without asking unless they are chained with others. Questions a chat can't show (forms, links) are refused, never left hanging.
- **Auto mode** (`auto` at setup) lets Codex write in the project folder without asking (`workspace-write`, never `danger-full-access`).
- Only your own messages count: a linked workspace admin's chat account, or your confirmed email with DMARC passing.
- Codex never sees your Puffin or GitHub keys; its own OpenAI sign-in stays as Codex set it up.

On the machine: `puffin codex status`, `puffin codex doctor`, `puffin codex logs`, `puffin codex stop`. In Codex, ask "set up Codex from my phone" (the `puffin-phone` skill) for a guided check.

## What's in this repo

```
.agents/plugins/marketplace.json        the marketplace (one plugin: puffin)
plugins/puffin/plugin.json              the portable plugin manifest, with Codex's interface metadata
plugins/puffin/mcp.json                 Puffin's hosted MCP server (OAuth sign-in)
plugins/puffin/skills/puffin/           how Codex should use the tools
plugins/puffin/skills/puffin-phone/     set up or check Codex from your phone
config.toml                             MCP settings for the Codex CLI without plugins
install.sh, install.ps1                 the phone gateway installers
scripts/validate.py                     checks the manifests (run by CI)
```

The phone gateway is the `puffin codex` command in the Puffin Python SDK (`puffin-local` 0.4.4 or later), which the installers set up.

## License

MIT
