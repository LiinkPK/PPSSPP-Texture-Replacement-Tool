CHANGELOG = {
    "v1.0.3": [
        "After testing with other games, app has been renamed to 'PPSSPP Texture Replacement Tool'",
        "Changed category and sub-category prefix from '#' to '>' to avoid conflicts with INI comment syntax.",
        "Added 'Edit' button next to Category and Sub-Category dropdowns: allows adding sub-categories, renaming, and deleting directly from the UI.",
        "Added a '✓' confirm button when adding a New Category.",
        "Fonts embedded to package.",
        "Changed body fonts and some capitalization.",
        "Fixed aspect ratio warning not showing: User now has a prompt to choose whether to proceed or go back before appending.",
        "Preview frames are now centered: If the image was too thin, the Original Texture frame was anchored to the top while Replaced Texture was centered. Both are now centered.",
        "Added 'Show in Explorer' function: A folder icon appears on both directory blocks once a PNG is selected, opening the containing folder and highlighting the file.",
        "Added current version label next to title: Clicking it shows the Changelog.",
        "Fixed filename duplicate warning: Previously only triggered if the hex filename was already in textures.ini. Now also checks the Replaced Texture's filename.",
        "[macOS] Larger overall GUI text.",
        "[macOS] Removed context menu when right-clicking empty preview frames.",
        "[macOS] Fixed Applications alias in installation disk image.",
    ],
    "v1.0.2": [
        "Fixed crash when textures.ini is empty.",
        "Improved aspect ratio warning message.",
        "Minor UI adjustments.",
        "Added pointer animation to append button.",
        "Added macOS support.",
    ],
    "v1.0.1": [
        "Initial release of 'Dissidia 012 Texture Replacement Tool'.",
    ],
}