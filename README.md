# 🤖 MultiAgentQA

Мультиагентная система автоматизации QA-процессов на базе [OpenCode](https://opencode.ai/v2/docs/).
Требования из Confluence → задачи в Jira → тестовая модель в Qase, с проверкой результата на каждом шаге.

## 📚 Содержание

- [Назначение проекта](#-назначение-проекта)
- [Участники Workflow](#-участники-workflow)
- [Этапы Workflow](#-этапы-workflow)
- [Структура репозитория](#-структура-репозитория)
- [Требования и настройка](#-требования-и-настройка)
- [Запуск агентов](#-запуск-агентов)
- [Evals (опционально)](#-evals-опционально)

___

## 🎯 Назначение проекта

Система автоматизирует рутину между требованиями и тестированием: разбирает требования, раскладывает их на задачи и проектирует проверки. Работа распределена между специализированными агентами, а результат каждого этапа проверяется, прежде чем идти дальше.

**Чем полезна:**

-  **Экономит время на разборе требований.** Противоречия, неоднозначности, пробелы и риски собираются в один отчёт со ссылками на исходный текст.
- **Даёт готовые задачи и тест-модель.** Задачи в Jira — с Acceptance Criteria и зависимостями, тест-модель — в виде Test Suites и Test Cases в Qase.
- **Не принимает решения за пользователя.** Спорные и недостающие требования возвращаются вопросом владельцу требований, а не додумываются агентом.
- **Оставляет след.** По каждому прогону есть отчёт: что сделано, что реально создано и что осталось нерешённым.

___

## 👥 Участники Workflow

Пользователь работает только с Orchestrator — он ставит задачи остальным агентам и собирает их результаты; вручную вызывать сабагентов не нужно.

| Участник | Инструкция | Что делает | Результат |
|---|---|---|---|
| **Orchestrator Agent** | `.opencode/agents/orchestrator-agent.md` | Ведёт этапы, раздаёт задачи, проверяет результаты, формирует отчёт | Workflow Report |
| **Requirement Review Agent** | `.opencode/agents/requirement-review-agent.md` | Читает требования в Confluence и проводит их QA-ревью | Requirement Review Artifact |
| **Task Design Agent** | `.opencode/agents/task-design-agent.md` | Декомпозирует требования и создаёт задачи в Jira | Jira Tasks Artifact |
| **Test Design Agent** | `.opencode/agents/test-design-agent.md` | Проектирует тест-модель и создаёт Test Suites / Test Cases в Qase | Test Model Artifact |
| **Пользователь** | — | Ставит задачу и отвечает на вопросы, требующие решения человека | Task Prompt |

Artifact — файл с результатом этапа в каталоге `artifacts/`; следующий этап работает именно с ним.

___

## 🔄 Этапы Workflow

Этапы идут по порядку, и после каждого стоит проверка — **Quality Gate**. Пока она не пройдена, результат дальше не передаётся. Если проверка выявила вопрос, требующий решения человека, Workflow останавливается и возвращает вопрос пользователю.


### Этап 1. Ревью требований (Requirement Review)

1. Orchestrator проверяет входные данные и передаёт задачу Requirement Review Agent.
2. Агент читает страницу Confluence инструментом `confluence` (персональные данные маскируются автоматически) и применяет Skill `requirement-review`.
3. Orchestrator проверяет полученный Artifact. При блокирующих находках Workflow останавливается, а вопросы передаются пользователю.


### Этап 2. Задачи в Jira и тест-модель (Task Design + Test Design)

1. Оба агента получают один и тот же проверенный Requirement Review Artifact.
2. Работают независимо: Task Design не смотрит в тест-модель, Test Design — в задачи Jira.
3. Агенты могут работать параллельно или последовательно; к Этапу 3 нужны результаты обоих.

### Этап 3. Финальная проверка (Final Quality Gate)

Orchestrator сверяет результат с требованиями: задачи и тест-модель должны соответствовать Artifact, а созданные сущности — подтверждаться ответами инструментов. Заново анализ здесь не выполняется.

### Этап 4. Отчёт (Final Reporting)

Orchestrator собирает итог: что сделано, какие Artifacts получены, какие сущности созданы (с ID), что осталось нерешённым. Итоговый статус прогона — `SUCCESS`, `PARTIAL`, `FAILED` или `REQUIRES_HUMAN_DECISION`.

___

## 📁 Структура репозитория

```text
MultiAgentQA/
├─ AGENTS.md                      # Общие правила агентов: принципы, источники истины, статусы, PII Protection
├─ README.md                      # Этот документ
├─ .env.example                   # Шаблон переменных окружения для Confluence
├─ .env                           # Локальные секреты (в Git не попадает)
│
├─ .opencode/
│  ├─ agents/
│  │  ├─ orchestrator-agent.md         # Управляющий агент (primary)
│  │  ├─ requirement-review-agent.md   # Агент ревью требований (subagent)
│  │  ├─ task-design-agent.md          # Агент декомпозиции на Jira Tasks (subagent)
│  │  └─ test-design-agent.md          # Агент тест-дизайна (subagent)
│  ├─ skills/
│  │  ├─ requirement-review/SKILL.md
│  │  ├─ task-design/SKILL.md
│  │  └─ test-design/SKILL.md
│  └─ plugins/
│     └─ confluence/
│        └─ index.ts               # Плагин проекта: инструмент `confluence` + маскирование PII
│
├─ artifacts/                     # Результаты прогонов (Artifacts)
│  ├─ requirement-review/
│  ├─ jira-tasks/
│  ├─ test-model/
│  └─ workflow-report/
│
└─ evals/                         # Оценка качества агентов (LLM-as-a-Judge)
   ├─ dataset/golden_dataset.json # Golden Dataset (Eval Cases)
   ├─ eval_runner.py              # Запуск агента по Eval Cases и расчёт метрик
   ├─ evaluator.py                # Оценка ответа агента моделью-судьёй
   └─ opencode_cli.py             # Запуск `opencode run --format json`
```

___

## ⚙️ Требования и настройка

### Предварительные условия

| Компонент | Что нужно |
|---|---|
| OpenCode | Установлен OpenCode V2, команда `opencode --version` работает в терминале |
| Node.js / npx | Для локального MCP-сервера Qase, который запускается через `npx` |
| Confluence | Аккаунт, API token и доступ к страницам с требованиями |
| Jira | Аккаунт Atlassian с доступом к проекту (вход по OAuth) |
| Qase | API token и доступ к проекту |
| Python (опционально) | Python 3.10+ для запуска `evals/`; внешние зависимости не нужны |

Три системы подключены тремя разными способами — это часть учебной задачи: Confluence через плагин проекта, Jira через удалённый MCP, Qase через локальный MCP.

### ○ Confluence: плагин проекта

Плагин `.opencode/plugins/confluence/index.ts` подключается автоматически и добавляет инструмент `confluence`:

- **Вход:** `pageId`.
- **Запрос:** `GET {CONFLUENCE_URL}/wiki/api/v2/pages/{pageId}?body-format=storage` с Basic Auth (`email:api_token`).
- **Проверка PII:** пароли, токены, email и телефоны маскируются в заголовке и теле страницы; в ответе есть `piiCheck` (`piiFound`, `detectedPII`).

**Настройка:**

1. Скопировать `.env.example` в `.env` в корне проекта.
2. Заполнить переменные:

   ```env
   CONFLUENCE_URL=https://your-domain.atlassian.net
   CONFLUENCE_EMAIL=you@example.com
   CONFLUENCE_API_TOKEN=YOU_CONFLUENCE_API_TOKEN
   ```

3. `.env` исключён из Git (`.gitignore`) — коммитить его нельзя.

Плагин перечитывает `.env` при каждом вызове, поэтому после правки значений перезапуск не нужен. Если переменные не заданы, инструмент вернёт ошибку с указанием, какого файла не хватило и какие ключи пусты.

### ○ Jira: удалённое подключение к MCP

Jira подключается как удалённый MCP-сервер с авторизацией по OAuth. Команда и набор вопросов могут отличаться в зависимости от ОС.

1. `opencode mcp add` → имя `jira`, тип `remote`, адрес `https://mcp.atlassian.com/v1/mcp`, авторизация **OAuth authentication**.
2. На вопрос «Do you have a pre-registered client id?» — **NO**.
3. `opencode mcp auth jira` → **Approve** → выбрать рабочее пространство → **Accept**. Альтернатива: `/mcps` → выбрать сервер → войти.
4. `opencode mcp list` → сервер должен быть в статусе `connected`.

> **Примечание:** Atlassian переводит MCP на `https://mcp.atlassian.com/v2/mcp`, старый `/v1/mcp` помечен как deprecated. При новой настройке актуальный адрес проверяется в документации Atlassian.

### ○ Qase: локальное подключение к MCP

Локальный MCP-сервер OpenCode запускает сам, как дочерний процесс.

1. Команда запуска — `["npx", "-y", "@qase/mcp-server"]`; документация: [qase-tms/qase-mcp-server](https://github.com/qase-tms/qase-mcp-server#quick-start).
2. Добавить сервер в конфигурацию OpenCode — глобальный файл `C:\Users\USER\.config\opencode\opencode.json`:

   ```jsonc
   {
     "$schema": "https://opencode.ai/config.json",
     "mcp": {
       "servers": {
         "qase": {
           "type": "local",
           "command": ["npx", "-y", "@qase/mcp-server"],
           "environment": {
             "QASE_API_TOKEN": "{env:QASE_API_TOKEN}"
           }
         }
       }
     }
   }
   ```

3. `opencode mcp list` или `/mcps` → статус `connected`.

> **Важно:** имена серверов должны быть **внутри** `mcp.servers`. Если `qase` указан рядом с `servers` по старой схеме, его нужно перенести внутрь — иначе сервер не найдётся.
>
> **Безопасность:** токен Qase лучше не хранить в файле — подстановка `{env:QASE_API_TOKEN}` берёт его из переменных окружения.

Конфигурация перечитывается автоматически после сохранения файла; принудительно — командой `/reload`.

### Проверка готовности

```sh
opencode --version          # OpenCode установлен
opencode mcp list           # jira и qase в статусе connected
```

В OpenCode `/mcps` показывает серверы и позволяет подключиться или авторизоваться. Также должно быть выполнено: `.env` заполнен; есть доступ к странице Confluence, проекту Jira и проекту Qase; модель из frontmatter агентов (`openrouter/deepseek/deepseek-v4.1-flash-1017`) доступна у провайдера. Если модели нет — `model` меняется в `.opencode/agents/*.md`.

___

## 🚀 Запуск агентов

> **Коротко:** `opencode` → `/agents` → `orchestrator-agent` → промпт с параметрами задачи.

### Запуск Workflow

1. Открыть терминал в корне проекта и запустить OpenCode:

   ```sh
   opencode
   ```

2. Выбрать `/agents` → `orchestrator-agent`.
3. Отправить промпт с параметрами задачи:

   ```text
   Проанализируй требования со страницы Confluence <pageId>,
   создай задачи в проекте <JIRA_PROJECT> в Jira
   и создай тестовую модель в проекте <QASE_PROJECT> в Qase.
   ```

   `<pageId>` — ID страницы Confluence, `<JIRA_PROJECT>` — ключ проекта Jira, `<QASE_PROJECT>` — код проекта Qase.

4. Дальше Orchestrator ведёт этапы сам: при необходимости задаст уточняющие вопросы и в конце вернёт Workflow Report.

> **Совет:** промпт можно ограничить одним этапом — например, только анализом требований. Тогда `jira_project` и `qase_project` не передаются, и Workflow завершится после Этапа 1.

### Где смотреть результаты

| Что | Куда |
|---|---|
| Артефакты этапов | каталог `artifacts/` (см. [Структура репозитория](#-структура-репозитория)) |
| Итоговый отчёт | `artifacts/workflow-report/workflow-report-*-v*-*.md` |
| Созданные задачи Jira | проект Jira; ID и ссылки — в Jira Tasks Artifact и Workflow Report |
| Созданные Test Suites / Test Cases | проект Qase; ID — в Test Model Artifact и Workflow Report |

___

## 🧪 Evals (опционально)

В `evals/` лежит контур оценки качества: ответ агента проверяет независимая модель-судья по Expected Properties и Forbidden Behavior.

```sh
cd evals
python eval_runner.py
```

Результат — `evals/results/eval_results.json`. Quality Gate: Pass Rate ≥ 95 %, Expected Properties ≥ 95 %, нарушения Forbidden Behavior = 0, ошибок = 0. Поддерживается только источник `confluence` (`page_id`); скрипт использует установленный OpenCode CLI и сам находит его на Windows.
