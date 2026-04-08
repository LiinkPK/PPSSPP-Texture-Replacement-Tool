# Texture Replacement Tool for PPSSPP

A desktop tool for managing HD texture replacements for any game running on [PPSSPP](https://github.com/hrydgard/PPSSPP).

> Previously called **_Dissidia 012 Texture Replacement Tool_**.
>
> Title has been changed after testing the tool with several games and seeing that it works with all that were tested. Also, PPSSPP's creator [hrydgard](github.com/hrydgard/) asked for the tool to be renamed, since its previous name made it look too official.

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
1. Download `TRT_PPSSPP.exe` from the [Releases](../../releases) page.
2. Place the file anywhere on your computer.
3. Run `TRT_PPSSPP.exe`. **No installation required**.
4. If **Windows** blocks the app, click `Run anyway`. 

### macOS
1. Download `TRT_PPSSPP.dmg` from the [Releases](../../releases) page.
2. Open the file to mount the disk image.
3. Drag `TRT_PPSSPP.app` into your **Applications** folder. Replace if prompted.
4. Open `terminal` and copy-paste the following code to allow mac to run the unsigned app:
```
xattr -cr /Applications/TRT_PPSSPP.app/
```

5. Confirm by typing your password if prompted.
6. Run it from **Applications**.

---

## Setup

1. Click **+ Add Game Folder** in the left sidebar.
2. Navigate to your game's textures folder containing `textures.ini`, e.g.:
   `Documents\PPSSPP\PSP\TEXTURES\ULES01505`
3. Give it a display name (e.g. "Dissidia 012 EUR").
4. Game's `texture.ini` and its folder will be loaded when selecting the game.

> **Make sure `textures.ini` is inside that folder or else appending won't work as intented.**

---

## Adding a texture replacement

1. Select the **original texture PNG**: the file extracted from the game, e.g.: `08c464508327c8adba260ba9.png`
2. Select the **replacement texture PNG**: your new HD version, e.g.: `Characters/Tifa/TifaPreBattle.png`
4. Select or load your **textures.ini** file.
5. Choose a **Category** and **Sub-Category** if applicable.
6. Click **Append to textures.ini**.

The entry will be written in the correct format and sorted alphabetically within its section.

> **Do not include spaces or invalid characters. Type everything together or separate it using - or _. Can include numbers.**
---

## It is very important to **NOT** rename the original file.

It should maintain its hexadecimal string for the replacement to work.

**Example:**

>If the filename is `08f8a0600867fb0f764f3a0d.png` do not change it to `KainPortrait_old.png` or PPSSPP will not overwrite it.
---

<img width="521" height="356" alt="v1 4" src="https://github.com/user-attachments/assets/02264207-d39f-4486-948b-4e3ff43e0db6" /><img width="520" height="355" alt="App2" src="https://github.com/user-attachments/assets/cc8d48e3-26c1-4b6b-8a2d-a7fa40e3735c" />


<img width="407" height="539" alt="Kain3" src="https://github.com/user-attachments/assets/abe74b37-29e7-4e76-bb1d-98de56c474e7" />

---

## textures.ini format

PPSSPP identifies textures using a hash code made up of three parts: the memory address, the CLUT (palette) hash, and the data hash. This tool disregards the memory address and uses the remaining 16 digits, prefixed with eight zeroes. This tells PPSSPP to match the texture regardless of its memory address, and the entry is formatted and written to the .ini file automatically.

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
