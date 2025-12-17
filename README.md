# Why Turn On Computer? (Terminal Edition)

A minimal terminal-based session tracker that helps you stay focused on your goals. Start your session by answering one question: "Why did you turn on your computer?" - then evaluate your progress when done.

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Build the executables:**
   ```bash
   uv run build.py
   ```

3. **Install aliases (automatic):**
   ```bash
   bash install.sh
   source ~/.bashrc  # or ~/.zshrc
   ```

4. **Start using:**
   ```bash
   why          # Start a session or view current session
   why-done     # Complete session with evaluation
   ```

## Commands

### `why` - Display or Start Session

If you have an active session, displays your current reason and session duration.

If no active session exists, prompts you to start one:

```
$ why

No active session.

Why did you turn on your computer?
> Write documentation for the project

✓ Session started: Write documentation for the project
```

### `why-done` - Complete Session

Ends your current session with a quick evaluation:

```
$ why-done

Session to complete:

Current session started at 15:30

  "Write documentation for the project"

Session duration: 1h 23m

Did you accomplish what you set out to do?
Not at all [1] [2] [3] [4] [5] Very much
> 4

Did you stay focused on your goal?
Not at all [1] [2] [3] [4] [5] Very much
> 3

Any additional comments?
(Press Esc then Enter when done, or just Enter for no comment)

> Got distracted by email but made good progress overall

✓ Session completed and saved!
Log: ~/.why_computer/session_2025-12-17T15:30:00.txt
```

## Configuration

Edit `~/.config/why-turn-on-computer/config.json` to customize:

```json
{
  "question_text": "What are you working on?",
  "evaluation_questions": [
    "Did you accomplish your goal?",
    "Did you stay focused?"
  ]
}
```

Default values will be used if config doesn't exist.

## Autostart on Ubuntu

To run the program automatically when you log in:

### Option 1: GNOME Startup Applications (Recommended)

1. Open **Startup Applications** (search in applications menu)
2. Click **Add**
3. Fill in:
   - **Name:** Why Turn On Computer
   - **Command:** `gnome-terminal -- /full/path/to/dist/why`
   - **Comment:** Ask why I turned on my computer
4. Click **Add**

Replace `/full/path/to/dist/why` with the actual path to your executable.

### Option 2: XDG Autostart (Manual)

Create `~/.config/autostart/why-turn-on-computer.desktop`:

```bash
cat > ~/.config/autostart/why-turn-on-computer.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Why Turn On Computer
Exec=gnome-terminal -- /full/path/to/dist/why
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
```

Replace `/full/path/to/dist/why` with the actual path.

### Option 3: Systemd User Service

Create `~/.config/systemd/user/why-turn-on-computer.service`:

```ini
[Unit]
Description=Why Turn On Computer
After=graphical-session.target

[Service]
Type=oneshot
ExecStart=/full/path/to/dist/why
StandardInput=tty
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

Enable it:
```bash
systemctl --user enable why-turn-on-computer.service
systemctl --user start why-turn-on-computer.service
```

**Note:** This runs without a terminal window. For interactive prompts, use Option 1 or 2.

## Data Storage

- **Config:** `~/.config/why-turn-on-computer/config.json`
- **Active session:** `~/.why_computer/.current_session.json`
- **Session logs:** `~/.why_computer/session_*.txt`

Session logs are saved in key=value format:

```
start_time=2025-12-17T15:30:00
reason=Write documentation for the project
duration=4980.5
question_1=Did you accomplish what you set out to do?
answer_1=4
question_2=Did you stay focused on your goal?
answer_2=3
comment=Got distracted by email but made good progress overall
end_time=2025-12-17T17:13:00
```

## Alias Setup

### Option 1: Automatic (Recommended)

```bash
bash install.sh
source ~/.bashrc  # or ~/.zshrc
```

### Option 2: Manual

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias why='/full/path/to/dist/why'
alias why-done='/full/path/to/dist/why-done'
```

Then: `source ~/.bashrc` or restart terminal

### Option 3: System-wide (requires sudo)

```bash
sudo cp dist/why /usr/local/bin/
sudo cp dist/why-done /usr/local/bin/
sudo chmod +x /usr/local/bin/why
sudo chmod +x /usr/local/bin/why-done
```

## Development

Run without building:

```bash
uv run python why.py
uv run python why_done.py
```

### Dependencies

- Python 3.12+
- prompt-toolkit
- appdirs

Install with:
```bash
uv sync
```

## Migration from v1.x

The terminal edition (v2.0+) is a complete rewrite with breaking changes:

- GUI replaced with terminal interface
- Purpose concept removed (just track immediate reason)
- Evaluation simplified to 2 questions

**Good news:** Old session logs remain readable and your data directory is unchanged. The old `purpose` field in config will simply be ignored.
