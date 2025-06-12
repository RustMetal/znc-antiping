# znc-antiping — A ZNC Module

**antiping** is a ZNC module written in Python that prevents IRC nick pings by inserting a **zero-width space** (`\u200b`) into specific words. This is useful for avoiding unwanted notifications when mentioning common names or roles.

---

##  Features

- Obfuscates words mid-character with a zero-width space to prevent pings.
- Case-insensitive matching (e.g., "Hello", "HELLO", "hello" all match).
- Handles:
  - Normal messages
  - Notices
  - `/me` actions (CTCP `ACTION`)
- Built-in commands for managing the watchlist.
- Persistent word list across ZNC restarts.
- Use !! before the word to not obfuscate it.

---

##  Installation

1. Ensure your ZNC has Python module support enabled.
2. Place the `antiping.py` file in your ZNC modules directory (usually `~/.znc/modules/`).
3. From your IRC client, load the module:
   ```bash
   /msg *znc loadmod modpython
   /msg *status loadmod antiping
4. Add or remove words from the list:
   ```bash
   /msg *antiping add <word>
   /msg *antiping del <word>

