# PPSSPP Texture Replacement Tool

A desktop tool for managing HD texture replacements for any game running on PPSSPP.

---

### **Platform Support**

- Windows
- macOS

---

## Features

- Browse and preview original and replacement PNG textures side by side
- Automatically appends entries to `textures.ini` in the correct format
- Organizes entries by category and sub-category
- Alphabetically sorts entries within each section
- Detects duplicate entries before writing
- Warns if replacement texture has a different aspect ratio
- Game history sidebar — save multiple game folders and switch between them
- Dark and light theme toggle
- Open `textures.ini` directly from the app

---

## Installation

### Windows
1. Download `PPSSPP_TRT.exe` from the [Releases](../../releases) page.
2. Place the file anywhere on your computer.
3. Run `PPSSPP_TRT.exe`. **No installation required**.
4. If **Windows** blocks the app, click `Run anyway`. 

### macOS
1. Download `PPSSPP_TRT.dmg` from the [Releases](../../releases) page.
2. Open the file to mount the disk image.
3. Drag `PPSSPP TRT.app` into your **Applications** folder. Replace if prompted.
4. Open `terminal` and copy-paste the following code to allow mac to run the unsigned app:
```
xattr -cr /Applications/PPSSPP\ TRT.app/
```

5. Confirm by typing your password if prompted.
6. Run it from Applications.

---

## Setup

1. Click **+ Add Game Folder** in the left sidebar.
2. Navigate to your PPSSPP textures folder, e.g.:
   `Documents\PPSSPP\PSP\TEXTURES\ULES01505`
3. Give it a display name (e.g. "Dissidia 012 EUR").
4. Game's `texture.ini` and its folder will be loaded when selecting the game.

> **Make sure "textures.ini" is inside that folder or else appending won't work as intented.**

---

## Adding a texture replacement

1. Select the **original texture PNG** — this is the file extracted from the game.
2. Select the **replacement texture PNG** — your new HD version.
3. Select or load your **textures.ini** file.
4. Choose a **Category** and **Sub-Category** if applicable.
5. Click **Append to textures.ini**.

The entry will be written in the correct format and sorted alphabetically within its section.

---

## It is very important to **NOT** rename the original file.

It should maintain its hexadecimal string for the replacement to work.

**Example:**

>If the filename is `0000000000000000668a48bc.png` do not change it to `AerithTexture_old.png` or PPSSPP will not overwrite it.
---

<img width="522" height="356" alt="App1" src="https://github.com/user-attachments/assets/0968b850-b526-4976-b044-afacc18ddc63" /><img width="522" height="356" alt="App2" src="https://github.com/user-attachments/assets/0e4c2377-3d96-4d93-8eda-fe827a2fce6f" />

<img width="407" height="539" alt="Kain3" src="https://github.com/user-attachments/assets/abe74b37-29e7-4e76-bb1d-98de56c474e7" />

---

## textures.ini format

PPSSPP identifies textures using only the last 8 digits of their hash code. The tool automatically formats the entry so only those 8 digits are written to the .ini file.
The tool uses `>` for top-level categories and `>>` for sub-categories:
```
>Characters
>>Aerith
0000000000000000668a48bc = Characters/Aerith/AerithMenuPort.png

>JobCards
00000000000000000e58e631 = JobCards/WhiteMage.png
```

---

## PPSSPP Settings

After appending the entries to the .ini file, make sure `texture replacement` is enabled in PPSSPP:

`Settings > Tools > Developer tools > Texture replacement > Replace textures`

Feel free to test it and share your experience on [Issues](../../issues) or on our [Discord server](https://discord.gg/wbpgtKNSM7).

---

## Links

- 🎮 [Discord](https://discord.gg/wbpgtKNSM7)
- 🐙 [GitHub](https://github.com/LiinkPK/Dissidia-012-HD-Textures)
- 👾 [Reddit](https://www.reddit.com/r/dissidia/comments/1g6peh2/dissidia_012_hd_remastered_wip/)
- 🎨 [Patreon](https://www.patreon.com/c/LinkG/membership)
- 💙 [PayPal](https://www.paypal.com/paypalme/liinkpk)

---

*Thank you so much for using this tool!*

*Created by Link Garcia*
