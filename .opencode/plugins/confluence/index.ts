import { Plugin } from "@opencode/plugin"
import { existsSync, readFileSync, statSync } from "node:fs"
import { dirname, join } from "node:path"

const ENV_FILENAME = ".env"
const ANCESTOR_DEPTH = 5

type EnvFile = { path: string; mtimeMs: number; values: Map<string, string> }

let cached: EnvFile | undefined

function parseEnvFile(path: string): Map<string, string> {
    const values = new Map<string, string>()

    for (const rawLine of readFileSync(path, "utf8").split(/\r?\n/)) {
        const line = rawLine.trim()
        if (!line || line.startsWith("#")) continue

        const separator = line.indexOf("=")
        if (separator === -1) continue

        const key = line.slice(0, separator).trim()
        let value = line.slice(separator + 1).trim()

        if (
            (value.startsWith('"') && value.endsWith('"')) ||
            (value.startsWith("'") && value.endsWith("'"))
        ) {
            value = value.slice(1, -1)
        }

        if (key) values.set(key, value)
    }

    return values
}

function envCandidates(startDirectories: readonly (string | undefined)[]): string[] {
    const candidates: string[] = []
    const add = (directory: string) => {
        const path = join(directory, ENV_FILENAME)
        if (!candidates.includes(path)) candidates.push(path)
    }

    for (const directory of startDirectories) {
        if (directory) add(directory)
    }

    const root = startDirectories.find((directory) => directory !== undefined)
    let current = root

    for (let depth = 0; current && depth < ANCESTOR_DEPTH; depth++) {
        const parent = dirname(current)
        if (parent === current) break
        add(parent)
        current = parent
    }

    return candidates
}

function readEnvFile(startDirectories: readonly (string | undefined)[]): {
    file?: Map<string, string>
    used?: string
    checked: string[]
} {
    const checked: string[] = []

    for (const path of envCandidates(startDirectories)) {
        checked.push(path)
        if (!existsSync(path)) continue

        const { mtimeMs } = statSync(path)

        if (cached && cached.path === path && cached.mtimeMs === mtimeMs) {
            return { file: cached.values, used: path, checked }
        }

        const values = parseEnvFile(path)
        cached = { path, mtimeMs, values }
        return { file: values, used: path, checked }
    }

    return { checked }
}

export default Plugin.define({
    id: "confluence",
    async setup(ctx) {
        const directories = [ctx.location.directory, ctx.location.project?.canonical]

        await ctx.tool.transform((editor) => {
            editor.add({
                name: "confluence",
                description: "Получить страницу Confluence по pageId (body-format=storage)",
                input: {
                    type: "object",
                    properties: { pageId: { type: "string" } },
                    required: ["pageId"],
                    additionalProperties: false
                },
                options: { codemode: true },
                async execute(input, context) {
                    const env = readEnvFile([...directories, process.cwd()])

                    const setting = (key: string): string | undefined => {
                        const fromFile = env.file?.get(key)?.trim()
                        return fromFile ? fromFile : process.env[key]?.trim() || undefined
                    }

                    const baseUrl = setting("CONFLUENCE_URL")
                    const email = setting("CONFLUENCE_EMAIL")
                    const token = setting("CONFLUENCE_API_TOKEN")

                    const missing = (["CONFLUENCE_URL", "CONFLUENCE_EMAIL", "CONFLUENCE_API_TOKEN"] as const)
                        .filter((key) => !setting(key))

                    if (missing.length > 0 || !baseUrl || !email || !token) {
                        const source = env.used
                            ? `в ${env.used} не задано или пусто: ${missing.join(", ")}`
                            : `.env не найден, проверены: ${env.checked.join(", ")}`
                        throw new Error(
                            `Не заданы переменные окружения Confluence (${source}). ` +
                                `Заполните .env по образцу .env.example.`
                        )
                    }

                    const auth = Buffer.from(`${email}:${token}`).toString("base64")

                    const response = await fetch(
                        `${baseUrl.replace(/\/+$/, "")}/wiki/api/v2/pages/${(input as { pageId: string }).pageId}?body-format=storage`,
                        {
                            headers: {
                                Authorization: `Basic ${auth}`,
                                Accept: "application/json"
                            },
                            signal: context.signal
                        }
                    )

                    if (!response.ok) {
                        const details = await response.text().catch(() => "")
                        const hint = details.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim().slice(0, 300)
                        throw new Error(
                            `Confluence API error: ${response.status} ${response.statusText}` +
                                (hint ? ` — ${hint}` : "")
                        )
                    }

                    return { content: JSON.stringify(await response.json()) }
                }
            })
        })
    }
})
