// Replaces {name} placeholders in a text from content/*.md with values.
// Used on the server (strict: an unknown name stops the build) and in chart scripts (lenient: it warns).
export type Vars = Record<string, string | number>;

export function fill(text: string, vars: Vars, where?: string): string {
  return text.replace(/\{([A-Za-z_]\w*)\}/g, (m, k: string) => {
    if (k in vars) return String(vars[k]);
    if (where) throw new Error(`${where}: unknown placeholder {${k}}. Available: ${Object.keys(vars).join(", ") || "none"}`);
    console.warn(`Unknown placeholder {${k}}`);
    return m;
  });
}
