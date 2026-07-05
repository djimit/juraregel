#!/usr/bin/env node
import { readFile, writeFile, mkdir } from "fs/promises";
import { existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { execSync } from "child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");

const commands = {
  init: "Scaffold een nieuwe use case: juraregel init <domein> <port>",
  check: "Run CI gates: juraregel check [use-case]",
  serve: "Start een Rule API: juraregel serve <use-case>",
  validate: "Valideer een JREM export: juraregel validate <jrem-file>",
  generate: "Genereer JREM from parser: juraregel generate <domein>",\n  help: "Toon dit overzicht"
};

function help() {
  console.log("JuraRegel CLI v1.0.0 — Legal RuleOps Platform\n");
  console.log("Commands:");
  for (const [cmd, desc] of Object.entries(commands)) {
    console.log(`  juraregel ${cmd.padEnd(12)} ${desc}`);
  }
}

async function init(domein, port) {
  if (!domein || !port) { console.error("Usage: juraregel init <domein> <port>"); process.exit(1); }
  const dir = join(ROOT, "use-cases", domein);
  if (existsSync(dir)) { console.error(`Use case '${domein}' bestaat al`); process.exit(1); }
  
  await mkdir(join(dir, "regelspraak"), { recursive: true });
  await mkdir(join(dir, "jrem/exports"), { recursive: true });
  await mkdir(join(dir, "api"), { recursive: true });
  await mkdir(join(dir, "tests"), { recursive: true });
  
  await writeFile(join(dir, "regelspraak/begrippen.rspraak"),
    `// Begrippenmodel — ${domein}\nbegrip regelId: "Unieke identificatie." type: tekst.\nbegrip compliant: "Voldoet?" waarden: ja, nee, onbekend.\n`);
  
  await writeFile(join(dir, "api/app.py"),
    `import sys\nfrom pathlib import Path\nSHARED = Path(__file__).parent.parent.parent.parent / "shared"\nsys.path.insert(0, str(SHARED))\nfrom api_base import create_app\nJREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"\napp = create_app("${domein}", JREM_DIR, ${port})\nif __name__ == "__main__":\n    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=${port})\n`);
  
  await writeFile(join(dir, "tests/test_${domein}.py"),
    `import sys\nfrom pathlib import Path\nimport pytest\nfrom fastapi.testclient import TestClient\nSHARED = Path(__file__).parent.parent.parent.parent / "shared"\nsys.path.insert(0, str(SHARED))\nfrom api_base import create_app\nJREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"\napp = create_app("${domein}", JREM_DIR, ${port})\nclient = TestClient(app)\nclass TestHealth:\n    def test_health(self): assert client.get("/v1/health").status_code == 200\n    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "${domein}"\n`);
  
  console.log(`✅ Use case '${domein}' scaffolded at use-cases/${domein}/ (port ${port})`);
  console.log("   Next: schrijf regels, maak JREM export, run tests");
}

async function check(useCase) {
  const cmd = useCase ? `bash ci/run-gates.sh use-cases/${useCase}` : "bash ci/run-all-gates.sh";
  try { execSync(cmd, { cwd: ROOT, stdio: "inherit" }); }
  catch { process.exit(1); }
}

async function serve(useCase) {
  if (!useCase) { console.error("Usage: juraregel serve <use-case>"); process.exit(1); }
  execSync(`python3 use-cases/${useCase}/api/app.py`, { cwd: ROOT, stdio: "inherit" });
}


async function generate(domein) {
  if (!domein) { console.error("Usage: juraregel generate <domein>"); process.exit(1); }
  const parserMap = {
    "bio2": "use-cases/bio2/lib/bio2_parser.py",
    "forumstandaardisatie": "use-cases/forumstandaardisatie/lib/fs_parser.py",
    "overheidsstandaarden": "use-cases/overheidsstandaarden/lib/os_parser.py",
    "nora": "use-cases/nora/lib/nora_parser.py",
    "eu-ai-act": "use-cases/eu-ai-act/lib/aiact_parser.py",
    "avg-gdpr": "use-cases/avg-gdpr/lib/avg_parser.py",
    "ncsc": "use-cases/ncsc/lib/ncsc_parser.py",
    "nis2": "use-cases/nis2/lib/nis2_parser.py",
  };
  const parser = parserMap[domein];
  if (!parser) { console.error(`No parser found for '${domein}'. Available: ${Object.keys(parserMap).join(", ")}`); process.exit(1); }
  try {
    execSync(`python3 ${parser}`, { cwd: ROOT, stdio: "inherit" });
    console.log(`✅ Generated JREM for ${domein}`);
  } catch { console.error(`Failed to generate for ${domein}`); process.exit(1); }
}

async function validate(jremFile) {
  if (!jremFile) { console.error("Usage: juraregel validate <jrem-file>"); process.exit(1); }
  try { execSync(`python3 shared/validate.py --schema shared/jrem-schema.json --instance ${jremFile}`, { cwd: ROOT, stdio: "inherit" }); }
  catch { process.exit(1); }
}

const [cmd, ...args] = process.argv.slice(2);
switch (cmd) {
  case "init": await init(args[0], args[1]); break;
  case "check": await check(args[0]); break;
  case "serve": await serve(args[0]); break;
  case "validate": await validate(args[0]); break;\n  case "generate": await generate(args[0]); break;
  case "help": case "--help": case undefined: help(); break;
  default: console.error(`Unknown command: ${cmd}`); help(); process.exit(1);
}
