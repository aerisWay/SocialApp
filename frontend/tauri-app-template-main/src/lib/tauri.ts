/**
 * Detect whether the app is running inside the Tauri desktop runtime.
 *
 * When the frontend is served as a plain web page (e.g. GitHub Pages),
 * the Tauri IPC bridge is absent, so native APIs must be skipped to avoid
 * runtime errors that would otherwise blank the page.
 */
export function isTauri(): boolean {
  return typeof window !== "undefined" && "__TAURI_INTERNALS__" in window;
}
