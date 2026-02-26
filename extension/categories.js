/**
 * File type → folder category mappings.
 * Mirrors the Python app's FILE_TYPES dictionary exactly.
 */
export const FILE_TYPES = {
  "Installers":    [".exe", ".msi", ".bat", ".cmd", ".sh", ".apk", ".bin", ".jar", ".vbs", ".deb", ".rpm"],
  "Archives":      [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".bz2", ".xz", ".tgz", ".sitx"],
  "Images":        [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff", ".heic", ".raw"],
  "Videos":        [".mp4", ".mkv", ".flv", ".avi", ".mov", ".wmv", ".webm", ".m4v", ".mpeg", ".mpg", ".3gp"],
  "Audio":         [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".alac", ".aiff"],
  "Documents":     [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md", ".tex", ".wpd", ".wps"],
  "Spreadsheets":  [".xls", ".xlsx", ".csv", ".ods", ".xlsm", ".tsv", ".numbers"],
  "Presentations": [".ppt", ".pptx", ".odp", ".pps", ".ppsx", ".key"],
  "Code":          [".py", ".js", ".html", ".css", ".cpp", ".java", ".json", ".sql", ".php", ".cs", ".go", ".rs", ".ts", ".xml", ".yaml", ".lua"],
  "Fonts":         [".ttf", ".otf", ".woff", ".woff2", ".eot"],
  "Ebooks":        [".epub", ".mobi", ".azw3", ".cbz", ".cbr"],
  "Design":        [".psd", ".ai", ".eps", ".indd", ".sketch", ".fig", ".xcf", ".cdr"],
  "3D Models":     [".stl", ".obj", ".fbx", ".blend", ".3ds", ".dae", ".gcode", ".ply"],
  "Disk Images":   [".img", ".vcd", ".toast", ".dmg"],
  "Torrents":      [".torrent"]
};

/** Extensions to never organize */
export const IGNORE_EXTS = [".tmp", ".crdownload", ".part", ".ini", ".download"];

/**
 * Get the destination folder for a given file extension.
 * @param {string} ext - file extension including the dot, e.g. ".exe"
 * @returns {string} folder name, e.g. "Installers", or "Miscellaneous"
 */
export function getCategoryForExtension(ext) {
  const lower = ext.toLowerCase();
  for (const [folder, exts] of Object.entries(FILE_TYPES)) {
    if (exts.includes(lower)) {
      return folder;
    }
  }
  return "Miscellaneous";
}

/**
 * Check if a file extension should be ignored.
 * @param {string} ext - file extension including the dot
 * @returns {boolean}
 */
export function shouldIgnore(ext) {
  return IGNORE_EXTS.includes(ext.toLowerCase());
}
