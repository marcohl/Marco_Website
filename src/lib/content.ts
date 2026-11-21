// Reads the editable text files in content/ (one per page) and turns their sections into HTML.
// File format and editing rules: content/README.md.
import { Marked } from "marked";
import { markedSmartypants } from "marked-smartypants";
import { fill, type Vars } from "./fill";

const raw = import.meta.glob("/content/**/*.md", { query: "?raw", import: "default", eager: true }) as Record<string, string>;
const md = new Marked({ gfm: true }).use(markedSmartypants());

// A section starts at a line like [[intro]] and runs to the next one. Text before the first section is ignored.
function sections(file: string, src: string) {
  const out: Record<string, string> = {};
  let cur: string | null = null, buf: string[] = [];
  const close = () => { if (cur) out[cur] = buf.join("\n").trim(); };
  for (const line of src.replace(/\r\n?/g, "\n").split("\n")) {
    const m = line.match(/^\[\[\s*([\w-]+)\s*\]\]\s*$/);
    if (!m) { if (cur) buf.push(line); continue; }
    close();
    if (m[1] in out) throw new Error(`${file}: section [[${m[1]}]] appears twice`);
    cur = m[1]; buf = [];
  }
  close();
  return out;
}

export function content(name: string, vars: Vars = {}) {
  const file = `content/${name}.md`;
  const src = raw[`/${file}`];
  if (src === undefined) throw new Error(`Missing text file ${file}`);
  const sec = sections(file, src);
  const get = (s: string) => {
    if (!(s in sec)) throw new Error(`${file}: missing section [[${s}]]`);
    return sec[s];
  };
  const filled = (s: string) => fill(get(s), vars, `${file} [[${s}]]`);
  const inline = (t: string) => md.parseInline(t) as string;

  return {
    /** Markdown section as HTML (paragraphs, headings, lists, links). */
    block: (s: string) => md.parse(filled(s)) as string,
    /** One-paragraph section as inline HTML, for use inside an existing <p> or <h1>. */
    inline: (s: string) => inline(filled(s).replace(/\s*\n\s*/g, " ")),
    /** "key: value" lines as an object of plain strings. Placeholders are left for the caller. */
    labels: (s: string) => {
      const o: Record<string, string> = {};
      for (const line of get(s).split("\n")) {
        const t = line.trim();
        if (!t || t.startsWith("#")) continue;
        const i = t.indexOf(": ");
        if (i < 1) throw new Error(`${file} [[${s}]]: line "${t}" needs the form  key: text`);
        o[t.slice(0, i).trim()] = t.slice(i + 2).trim();
      }
      return o;
    },
    /** "- label | value" lines, e.g. key figures. Both parts as inline HTML. */
    pairs: (s: string) => filled(s).split("\n").map((l) => l.trim()).filter((l) => l.startsWith("- ")).map((l) => {
      const [label, value = ""] = l.slice(2).split(" | ");
      return { label: inline(label.trim()), value: inline(value.trim()) };
    }),
    /** Numbered list ("1. ...") as one inline HTML string per item. */
    items: (s: string) => filled(s).split(/\n(?=\s*\d+\.\s)/).map((t) => t.replace(/^\s*\d+\.\s+/, "").replace(/\s*\n\s*/g, " ").trim()).filter(Boolean).map(inline),
    /** Notes section: text before the first "###" is the heading; each "###" starts a column. */
    columns: (s: string) => {
      const parts = filled(s).split(/\n(?=###\s)/);
      const head = parts[0].trim().startsWith("###") ? "" : parts.shift()!;
      return { head: md.parse(head) as string, cols: parts.map((p) => md.parse(p) as string) };
    },
  };
}

/** Title, description and eyebrow of a project, from the [[page]] section of content/projects/<slug>.md. */
export const projectInfo = (slug: string) => content(`projects/${slug}`).labels("page");
