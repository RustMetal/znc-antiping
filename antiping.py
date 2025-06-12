# Copyright 2025
# This program is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software 
# Foundation, version 3 of the License.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with 
# this program. If not, see <https://www.gnu.org/licenses/>.

import znc
import re
import json

class antiping(znc.Module):
    description = "Inserts a zero-width space into certain words to prevent pings"

    def OnLoad(self, args, message):
        self._load_watchlist()
        self.PutModule("antiping module loaded. Obfuscating: " + ", ".join(self.watchlist))
        return True

    def OnUserMsg(self, target, message):
        message.s = self._process_text(message.s)
        return znc.CONTINUE

    def OnUserNotice(self, target, message):
        message.s = self._process_text(message.s)
        return znc.CONTINUE

    def OnUserCTCP(self, target, message):
        if message.s.startswith("ACTION "):
            action_text = message.s[7:]
            new_text = self._process_text(action_text)
            message.s = "ACTION " + new_text
        return znc.CONTINUE

    def OnModCommand(self, command):
        parts = command.strip().split()
        if not parts:
            self.PutModule("Usage: add <word>, del <word>, list")
            return

        cmd = parts[0].lower()

        if cmd == "add" and len(parts) == 2:
            word = parts[1].lower()
            if word in self.watchlist:
                self.PutModule(f"'{word}' is already in the watchlist.")
            else:
                self.watchlist.append(word)
                self._save_watchlist()
                self.PutModule(f"Added '{word}' to watchlist.")

        elif cmd == "del" and len(parts) == 2:
            word = parts[1].lower()
            if word in self.watchlist:
                self.watchlist.remove(word)
                self._save_watchlist()
                self.PutModule(f"Removed '{word}' from watchlist.")
            else:
                self.PutModule(f"'{word}' not found in watchlist.")

        elif cmd == "list":
            if self.watchlist:
                self.PutModule("Current watchlist: " + ", ".join(self.watchlist))
            else:
                self.PutModule("Watchlist is empty.")

        else:
            self.PutModule("Unknown command. Use: add <word>, del <word>, list")

    def _process_text(self, text):
        for word in self.watchlist:
            # Skip obfuscation if the word is preceded by '!!'
            pattern = re.compile(r'(?<![!])(?:!!)?\b(' + re.escape(word) + r')\b', re.IGNORECASE)
    
            def replacer(match):
                full_match = match.group(0)
                clean_word = match.group(1)
    
                # If the match starts with '!!', strip the '!!' and return the clean word unmodified
                if full_match.startswith("!!"):
                    return clean_word  # remove the '!!' and don't obfuscate
    
                # Otherwise, obfuscate
                mid = len(clean_word) // 2
                return clean_word[:mid] + '\u200b' + clean_word[mid:]
    
            text = pattern.sub(replacer, text)
    
        return text


    def _save_watchlist(self):
        self.SetNV("watchlist", json.dumps(self.watchlist))

    def _load_watchlist(self):
        data = self.GetNV("watchlist")
        if data:
            try:
                self.watchlist = json.loads(data)
            except Exception:
                self.watchlist = []
                self.PutModule("Error loading watchlist, starting with empty list.")
        else:
            self.watchlist = ["plugin", "days"]  # default censor list
