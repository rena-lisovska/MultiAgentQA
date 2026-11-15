import { Plugin } from "@opencode/plugin"
import { existsSync, readFileSync, statSync } from "node:fs"
import { dirname, join } from "node:path"

const ENV_FILENAME = ".env"
const ANCESTOR_DEPTH = 5

// ==========================================
// REGEX: Поиск и маскирование PII
// ==========================================

type PiiType = "PASSWORD" | "TOKEN" | "EMAIL" | "PHONE"

type PiiResult = {
    piiFound: boolean
    detectedPII: PiiType[]
    maskedText: string
}

// Password
const PASSWORD_REGEX = /(?<![\wА-Яа-яЁё])((?:password|passwd|pwd|пароль)\s*[:=]\s*)[^\s<]+/gi

// API Key / Token
const TOKEN_REGEX =
    /(?<![\wА-Яа-яЁё])((?:(?:api[_-]?|access[_-]?|auth[_-]?|refresh[_-]?)?token|api[_-]?key|apikey|secret)\s*[:=]\s*)[^\s<]+/gi

// Email
const EMAIL_REGEX = /[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}/g

// Phone
const PHONE_REGEX = /(?:\+?\d[\d\s()-]{8,}\d)/g

// HTML-тег целиком, включая атрибуты.
const HTML_TAG_REGEX = /<[^>]*>/g

// Символы, рядом с которыми телефон не может начинаться/заканчиваться (id, hex, дефис).
const ID_NEIGHBOUR_REGEX = /[0-9a-fA-F-]/

/**
 * Применяет маскирование только к текстовым узлам storage-формата.
 * Атрибуты (`local-id="aca81db0-270e-4121-8381-56ad6bfb59b0"` и т.п.) не затрагиваются:
 * иначе телефонный regex вырезает куски UUID и ломает разметку страницы.
 */
function maskOutsideTags(text: string, apply: (chunk: string) => string): string {
    let result = ""
    let lastIndex = 0

    for (const tag of text.matchAll(HTML_TAG_REGEX)) {
        const index = tag.index ?? 0
        result += apply(text.slice(lastIndex, index))
        result += tag[0]
        lastIndex = index + tag[0].length
    }

    return result + apply(text.slice(lastIndex))
}

function maskPII(text: string): PiiResult {
    const detected: PiiType[] = []

    let masked = text.replace(PASSWORD_REGEX, (_match, prefix: string) => {
        detected.push("PASSWORD")
        return `${prefix}[PASSWORD_MASKED]`
    })

    masked = masked.replace(TOKEN_REGEX, (_match, prefix: string) => {
        detected.push("TOKEN")
        return `${prefix}[TOKEN_MASKED]`
    })

    masked = masked.replace(EMAIL_REGEX, () => {
        detected.push("EMAIL")
        return "[EMAIL_MASKED]"
    })

    masked = maskOutsideTags(masked, (chunk) =>
        chunk.replace(PHONE_REGEX, (match: string, offset: number, whole: string) => {

            const digits = match.replace(/\D/g, "").length
            if (digits < 10 || digits > 15) return match

            const before = offset > 0 ? whole[offset - 1] : ""
            const after = whole[offset + match.length] ?? ""

            if (ID_NEIGHBOUR_REGEX.test(before) || ID_NEIGHBOUR_REGEX.test(after)) return match

            if (!/[\s()-]/.test(match)) {
                const local = match.replace(/\D/g, "")
                const looksLikePhone = match.startsWith("+") || (local.length === 11 && /^[78]/.test(local))
                if (!looksLikePhone) return match
            }

            detected.push("PHONE")
            return "[PHONE_MASKED]"
        })
    )

    return {
        piiFound: detected.length > 0,
        detectedPII: [...new Set(detected)],
        maskedText: masked
    }
}

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
                description:
                    "Получить страницу Confluence по pageId (body-format=storage) " +
                    "с проверкой и маскированием PII (password, token, email, phone) в title и body.storage.value",
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

                    const page = (await response.json()) as {
                        title?: unknown
                        body?: { storage?: { value?: unknown } }
                        [key: string]: unknown
                    }

                    const requirements = page.body?.storage?.value

                    if (typeof requirements !== "string") {
                        throw new Error(
                            "Не удалось получить содержимое страницы Confluence (body.storage.value отсутствует)"
                        )
                    }

                    // ==========================================
                    // Regex-проверка PII и маскирование
                    // ==========================================

                    const bodyPii = maskPII(requirements)
                    const titlePii = typeof page.title === "string" ? maskPII(page.title) : undefined

                    const detectedPII = [...new Set([...(titlePii?.detectedPII ?? []), ...bodyPii.detectedPII])]

                    // ==========================================
                    // Возврат: метаданные без изменений, содержимое очищено
                    // ==========================================

                    const storage = page.body?.storage ?? {}

                    const result = {
                        ...page,
                        title: titlePii ? titlePii.maskedText : page.title,
                        piiCheck: { piiFound: detectedPII.length > 0, detectedPII },
                        body: {
                            ...page.body,
                            storage: { ...storage, value: bodyPii.maskedText }
                        }
                    }

                    return { content: JSON.stringify(result) }
                }
            })
        })
    }
})
