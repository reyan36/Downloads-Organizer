// --- DOM Elements ---
const enableToggle = document.getElementById('enableToggle');
const miscToggle = document.getElementById('miscToggle');
const statusBadge = document.getElementById('statusBadge');

// --- Load Settings ---
function loadSettings() {
    chrome.storage.sync.get({ enabled: true, organizeMisc: true }, (settings) => {
        enableToggle.checked = settings.enabled;
        miscToggle.checked = settings.organizeMisc;
        updateStatusUI(settings.enabled);
    });
}

// --- Update Status UI ---
function updateStatusUI(enabled) {
    if (enabled) {
        statusBadge.textContent = 'Active';
        statusBadge.classList.remove('inactive');
    } else {
        statusBadge.textContent = 'Paused';
        statusBadge.classList.add('inactive');
    }
}

// --- Event Listeners ---
enableToggle.addEventListener('change', () => {
    const enabled = enableToggle.checked;
    chrome.storage.sync.set({ enabled });
    updateStatusUI(enabled);
});

miscToggle.addEventListener('change', () => {
    const organizeMisc = miscToggle.checked;
    chrome.storage.sync.set({ organizeMisc });
});

// --- Init ---
document.addEventListener('DOMContentLoaded', loadSettings);
