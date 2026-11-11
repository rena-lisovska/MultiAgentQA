import { Plugin } from "@opencode/plugin"

export default Plugin.define({
    id: "confluence",
    async setup(ctx) {
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
                    const baseUrl = process.env.CONFLUENCE_URL
                    const email = process.env.CONFLUENCE_EMAIL
                    const token = process.env.CONFLUENCE_API_TOKEN

                    if (!baseUrl || !email || !token) {
                        throw new Error("Не заданы переменные окружения Confluence")
                    }

                    const auth = Buffer.from(`${email}:${token}`).toString("base64")

                    const response = await fetch(
                        `${baseUrl}/wiki/api/v2/pages/${(input as { pageId: string }).pageId}?body-format=storage`,
                        {
                            headers: {
                                Authorization: `Basic ${auth}`,
                                Accept: "application/json"
                            },
                            signal: context.signal
                        }
                    )

                    if (!response.ok) {
                        throw new Error(
                            `Confluence API error: ${response.status} ${response.statusText}`
                        )
                    }

                    return { content: JSON.stringify(await response.json()) }
                }
            })
        })
    }
})