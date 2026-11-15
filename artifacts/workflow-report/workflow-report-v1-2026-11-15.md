# Workflow Report — EVL-002 (Требования к форме авторизации)

## 1. Workflow Summary

| Поле | Значение |
|---|---|
| `workflow_status` | **`REQUIRES_HUMAN_DECISION`** |
| `application_name` | Форма авторизации пользователя в системе (модуль авторизации, `EVL-002`) |
| `requirements_source` | Confluence `pageId=6881281` (`https://qai06.atlassian.net/wiki/spaces/~712020d7c124373b1944dcae68dd8af940cca9/pages/6881281/EVL-002`, версия 1 от `2026-11-10T11:39:02.182Z`) -> ссылка на Google Docs `https://docs.google.com/document/d/122SLgz6t9PYL4khXpcmydQk02v0KQIcvGYErLvKU-Sg/edit?tab=t.0` |
| `related_requirements` | Не переданы (анализ ограничен страницей `pageId=6881281` и связанным документом Google Docs, разделы 1–7) |
| `artifacts` | `artifacts/requirement-review/requirement-review-v1-2026-11-15.md` (`v1`, `BLOCKED`) · `artifacts/requirement-review/requirement-review-v2-2026-11-15.md` (`v2`, `PASSED`, заменяет `v1`) · `artifacts/workflow-report/workflow-report-v1-2026-11-15.md` (`v1`) |
| `execution_summary` | Выполнен Stage 1 (Requirement Review) для `pageId=6881281`. В прогоне `v1` страница Confluence содержала только ссылку на внешний Google Doc, поэтому работа была остановлена (`BLOCKED`). Orchestrator получил текст документа по экспортной ссылке Google Docs (`/export?format=txt`) и передал его в `requirement-review-agent` как `requirement_content` (`snapshot`). В прогоне `v2` проанализированы все 7 разделов (`REQ-01`–`REQ-27`), выявлено 8 `BLOCKING`-находок (`BLK-01`–`BLK-08`) и 7 `NON_BLOCKING`-находок (`NB-01`–`NB-07`), `requires_escalation = true`. Независимая проверка Orchestrator (10.1) пройдена (`PASSED`), однако согласно Decision Point Stage 1 и из-за отсутствия целевых параметров `jira_project` и `qase_project` Workflow остановлен до получения решений пользователя. |

## 2. Stage Results

| Этап | Сабагент | Статус | Проверка Orchestrator | Artifact | Ошибки / ограничения |
|---|---|---|---|---|---|
| Stage 1 (прогон 1). Requirement Review | `requirement-review-agent` | `REQUIRES_HUMAN_DECISION` | — (stop-Artifact `v1`) | `artifacts/requirement-review/requirement-review-v1-2026-11-15.md` (`v1`, Gate: `BLOCKED`) | Страница Confluence `6881281` содержит только внешнюю ссылку на Google Docs без текста требований; `Confluence READ` не покрывает Google Docs |
| Stage 1 (прогон 2). Requirement Review | `requirement-review-agent` | `SUCCESS` (`requires_escalation = true`) | `PASSED` (10.1) | `artifacts/requirement-review/requirement-review-v2-2026-11-15.md` (`v2`, Gate: `PASSED`) | Текст требований получен через `snapshot` (`/export?format=txt`) и не верифицирован `Confluence READ`; выявлено 8 `BLOCKING`-находок (`BLK-01`–`BLK-08`) |
| Stage 2a. Task Design | `task-design-agent` | `NOT_STARTED` | — | Не создавался | Заблокирован эскалацией Stage 1 (`requires_escalation = true`) и отсутствием входного параметра `jira_project` |
| Stage 2b. Test Design | `test-design-agent` | `NOT_STARTED` | — | Не создавался | Заблокирован эскалацией Stage 1 (`requires_escalation = true`) и отсутствием входного параметра `qase_project` |
| Stage 3. Final Quality Gate | Orchestrator | `NOT_STARTED` | — | — | Stage 2 не выполнялся |

## 3. Created Entities

Сущности в Jira и Qase **не создавались** (`[]`), так как этапы Task Design и Test Design не запускались.

- **Jira issues:** не создавались.
- **Qase entities:** не создавались.

## 4. Issues and Limitations

1. **Происхождение текста требований (`snapshot`):** Confluence `pageId=6881281` (`EVL-002`, v1) содержит только заголовок «Требования к форме авторизации» и ссылку на Google Docs (`122SLgz6t9PYL4khXpcmydQk02v0KQIcvGYErLvKU-Sg`). Текст разделов 1–7 получен Orchestrator через `webfetch` (`/export?format=txt`) и передан как `requirement_content` (`snapshot`). Версия документа в Google Docs, история изменений, комментарии, вложения и исходное форматирование не верифицированы инструментом Confluence. В частности, в экспорте встречено экранирование `\$` (`BLK-04`).
2. **8 `BLOCKING`-находок в требованиях (`requirements_readiness = NOT_READY`):** без решений владельца требований невозможна однозначная финализация декомпозиции и тест-дизайна по затронутым правилам (`BLK-01`–`BLK-08`).
3. **Не заданы целевые проекты Stage 2:** во входном `task_prompt` не указаны `jira_project` (доступный в Jira проект: `KAN` / `QAI`) и `qase_project` (а также опциональный `qase_suite`).
4. **Уведомление об устаревании Atlassian MCP endpoint:** используемый сервер Jira работает на устаревшем `/v1/mcp` (отключение 2027-03-01). Необходимо обновить конфигурацию MCP на `https://mcp.atlassian.com/v2/mcp`.

## 5. Escalation

- **Этап эскалации:** `Stage 1. Requirement Review` (перед переходом к `Stage 2. Task Design and Test Design`).
- **Заблокированные этапы:** `Stage 2a. Task Design`, `Stage 2b. Test Design`, `Stage 3. Final Quality Gate`.
- **Связанные артефакты и источники:**
  - `artifacts/requirement-review/requirement-review-v2-2026-11-15.md` (разделы 9, 10, 13, 14)
  - `artifacts/requirement-review/requirement-review-v1-2026-11-15.md` (история остановки `v1`)
  - Confluence `pageId=6881281` (`EVL-002`, v1) и Google Doc `122SLgz6t9PYL4khXpcmydQk02v0KQIcvGYErLvKU-Sg`

### Вопросы, требующие решения человека

1. **Подтверждение источника (`snapshot`):** подтвердите, что текст из Google Docs (`122SLgz6t9PYL4khXpcmydQk02v0KQIcvGYErLvKU-Sg`), указанного на странице Confluence `pageId=6881281`, является актуальной утверждённой версией требований (и будет ли он перенесён в Confluence).
2. **`BLK-01` (`MISSING_INFORMATION`, `HIGH`):** какое сообщение (единое или разные для отдельных правил) должно отображаться при нарушении формата `Email` (раздел 3)?
3. **`BLK-02` (`MISSING_INFORMATION`, `HIGH`):** как система должна реагировать на ввод недопустимых символов в `Password` (блокировать ввод, показывать конкретное сообщение без отправки или отправлять на сервер) и каков приоритет ошибок длины и состава?
4. **`BLK-03` (`AMBIGUITY`, `HIGH`):** лимит 254 символа `Email` проверяется до или после удаления крайних пробелов; разрешается ли ввод > 254 символов с ошибкой или ограничивается UI; удаляются ли крайние пробелы визуально в поле при сохранении значений по `REQ-25`?
5. **`BLK-04` (`AMBIGUITY`, `MEDIUM`):** подтвердите по оригиналу Google Docs, означает ли `\$` в разделах 3 и 4 один допустимый символ `$` (артефакт текстового экспорта)?
6. **`BLK-05` (`AMBIGUITY`, `MEDIUM`):** допустимы ли подряд идущие точки (`..`) в имени пользователя/домене, точка в начале/конце имени пользователя, дефис в начале/конце сегмента домена, цифровой TLD, и ограничены ли буквы домена только базовой латиницей `a-z`, `A-Z`?
7. **`BLK-06` (`AMBIGUITY`, `HIGH`):** считается ли первое нажатие `Login`, заблокированное клиентской валидацией, «первой попыткой входа»; по какому событию (`onInput` или `onBlur`) срабатывает перевалидация обоих полей; скрывается ли «Неверный email или пароль» при правке поля и выводятся ли ошибки индивидуально у каждого поля?
8. **`BLK-07` (`AMBIGUITY`, `MEDIUM`):** сохраняются ли крайние пробелы в не полностью пробельном пароле при подсчёте длины 8–64 и аутентификации, и относятся ли к «пробелам» только `U+0020` или любые whitespace-символы?
9. **`BLK-08` (`MISSING_INFORMATION`, `MEDIUM`):** когда срабатывает редирект на `/login` после 30 дней с `Remember me` (в реальном времени или при действии/перезагрузке), есть ли таймаут сессии без `Remember me`, куда перенаправляется неавторизованный пользователь с `/dashboard` и авторизованный пользователь при переходе на `/login`?
10. **Параметры Stage 2 (`jira_project`, `qase_project`, `qase_suite`):** укажите целевой проект Jira (в системе доступен проект `KAN` / `QAI`), целевой код проекта Qase и при необходимости корневой раздел `qase_suite`, а также подтвердите, требуется ли продолжение Stage 2 только для независимой части или после обновления Artifact `v3` с вашими ответами.
