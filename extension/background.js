import { getCategoryForExtension, shouldIgnore } from './categories.js';

/**
 * Downloads Organizer — Background Service Worker
 *
 * Intercepts Chrome downloads via onDeterminingFilename and redirects
 * them into categorized subfolders (e.g., "Installers/setup.exe").
 * Chrome remains aware of the real path, so clicking the download works.
 */

// --- Default settings ---
const DEFAULT_SETTINGS = {
    enabled: true,
    organizeMisc: true // whether to put unknowns into "Miscellaneous" vs leave in root
};

/**
 * Load settings from chrome.storage.sync
 */
async function getSettings() {
    return new Promise((resolve) => {
        chrome.storage.sync.get(DEFAULT_SETTINGS, (result) => {
            resolve(result);
        });
    });
}

/**
 * Extract file extension from a filename (handles paths with directories).
 * @param {string} filename - e.g., "setup.exe" or "folder/report.pdf"
 * @returns {string} extension including dot, e.g., ".exe", or "" if none
 */
function getExtension(filename) {
    // Get just the basename (last segment after any slashes)
    const basename = filename.split(/[/\\]/).pop() || filename;
    const dotIndex = basename.lastIndexOf('.');
    if (dotIndex <= 0) return ''; // No extension, or hidden file like ".gitignore"
    return basename.substring(dotIndex);
}

/**
 * Core listener: intercept download filename determination.
 *
 * Chrome fires this event after MIME type detection but before the file
 * is written to disk. We suggest a new filename that includes the
 * category subfolder prefix.
 */
chrome.downloads.onDeterminingFilename.addListener(
    (downloadItem, suggest) => {
        // Load settings asynchronously; we return true to indicate
        // we will call suggest() asynchronously.
        getSettings().then((settings) => {
            try {
                // If disabled, don't modify anything
                if (!settings.enabled) {
                    suggest();
                    return;
                }

                const originalFilename = downloadItem.filename;
                const ext = getExtension(originalFilename);

                // Skip temp/partial files
                if (!ext || shouldIgnore(ext)) {
                    suggest();
                    return;
                }

                // Already in a subfolder? Don't re-organize.
                // (handles cases where user manually picks "Save As" into a subfolder)
                if (originalFilename.includes('/') || originalFilename.includes('\\')) {
                    suggest();
                    return;
                }

                const category = getCategoryForExtension(ext);

                // If it's "Miscellaneous" and user disabled misc organizing, leave in root
                if (category === 'Miscellaneous' && !settings.organizeMisc) {
                    suggest();
                    return;
                }

                // Suggest the file be saved into the category subfolder
                const newFilename = `${category}/${originalFilename}`;

                suggest({
                    filename: newFilename,
                    conflictAction: 'uniquify' // auto-rename if file exists (e.g., file_1.exe)
                });
            } catch (err) {
                console.error('[Downloads Organizer] Error:', err);
                suggest(); // Fallback: don't modify
            }
        });

        // Return true to indicate async suggest() call
        return true;
    }
);

/**
 * On install: set default settings and open a welcome notification.
 */
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        chrome.storage.sync.set(DEFAULT_SETTINGS);
    }
});

/**
 * Listen for messages from popup (e.g., requesting current state).
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'getStatus') {
        getSettings().then((settings) => {
            sendResponse({ enabled: settings.enabled });
        });
        return true; // async response
    }
});
