#!/bin/bash
# Install script for why-turn-on-computer aliases

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"

# Detect shell
SHELL_NAME=$(basename "$SHELL")
case "$SHELL_NAME" in
  bash)
    RC_FILE="$HOME/.bashrc"
    ;;
  zsh)
    RC_FILE="$HOME/.zshrc"
    ;;
  fish)
    RC_FILE="$HOME/.config/fish/config.fish"
    echo "Fish shell detected. Manual configuration required."
    echo "Add these functions to $RC_FILE:"
    echo "  function why; $DIST_DIR/why \$argv; end"
    echo "  function why-done; $DIST_DIR/why-done \$argv; end"
    exit 0
    ;;
  *)
    echo "Unknown shell: $SHELL_NAME"
    echo ""
    echo "Please manually add aliases to your shell RC file:"
    echo "  alias why='$DIST_DIR/why'"
    echo "  alias why-done='$DIST_DIR/why-done'"
    echo ""
    echo "Or install system-wide (requires sudo):"
    echo "  sudo cp $DIST_DIR/why /usr/local/bin/"
    echo "  sudo cp $DIST_DIR/why-done /usr/local/bin/"
    echo "  sudo chmod +x /usr/local/bin/why"
    echo "  sudo chmod +x /usr/local/bin/why-done"
    exit 1
    ;;
esac

# Check if executables exist
if [ ! -f "$DIST_DIR/why" ] || [ ! -f "$DIST_DIR/why-done" ]; then
  echo "Error: Executables not found in $DIST_DIR"
  echo "Please run: python build.py"
  exit 1
fi

# Check if aliases already exist
if grep -q "# Why Turn On Computer aliases" "$RC_FILE" 2>/dev/null; then
  echo "Aliases already exist in $RC_FILE"
  echo "Remove the existing section if you want to reinstall."
  exit 0
fi

# Add aliases to RC file
echo "" >> "$RC_FILE"
echo "# Why Turn On Computer aliases" >> "$RC_FILE"
echo "alias why='$DIST_DIR/why'" >> "$RC_FILE"
echo "alias why-done='$DIST_DIR/why-done'" >> "$RC_FILE"

echo "✓ Aliases added to $RC_FILE"
echo ""
echo "Run this to activate:"
echo "  source $RC_FILE"
echo ""
echo "Or restart your terminal."
echo ""
echo "Commands available:"
echo "  why       - Show current session or start new one"
echo "  why-done  - Complete session with evaluation"
echo ""
echo "Alternative: Install system-wide (requires sudo):"
echo "  sudo cp $DIST_DIR/why /usr/local/bin/"
echo "  sudo cp $DIST_DIR/why-done /usr/local/bin/"
echo "  sudo chmod +x /usr/local/bin/why"
echo "  sudo chmod +x /usr/local/bin/why-done"
