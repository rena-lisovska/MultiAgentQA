# Test Model Artifact

## 1. Header

| Поле | Значение |
|---|---|
| `artifact_name` | test-model |
| `artifact_version` | v1 |
| `date` | 2026-11-16 |
| `producer` | QA Test Design Agent (сабагент QA Workflow) |
| `skill` | test-design |
| `application_name` | не установлено — из Artifact требований определяется только функциональность «форма авторизации пользователя»; источник: Confluence pageId 2228225 «Авторизация пользователя в системе», версия 7 от 2026-11-15 |
| `qase_project` | AUTH (резолв подтверждён ответом Tool: `project.code = AUTH`, `project.title = AUTH`) |
| `qase_suite` | не задан — все Test Suites созданы на корневом уровне проекта AUTH (`parent_id = null`) |
| `requirement_review_artifact` | `artifacts/requirement-review/requirement-review-v2-2026-11-16.md` |
| `requirement_review_version` | v2 (`replaces_previous_version: v1`; v1 не использовалась) |
| `requirement_review_gate_status` | `PASSED` (подтверждено Orchestrator) |
| `decision_provenance` | решения владельца требований от 2026-11-16 по BLK-01…BLK-05 использованы только в том виде, в каком они включены в Artifact v2 (`provenance: human decision`) |
| `consumers` | Orchestrator, Final Quality Gate |

Изменения относительно предыдущих версий: первая версия Artifact.

## 2. Test Scope

### 2.1. Область тестирования

`test_scope` не передан — область тестирования принята как **весь Requirement Review Artifact v2**: требования REQ-01…REQ-37, бизнес-правила BR-01…BR-14, критерии AC-01…AC-25, правила валидации VR-01…VR-10, границы B-01…B-11, позитивные потоки PF-01…PF-09, негативные потоки NF-01…NF-17, зависимости DEP-01…DEP-07.

Сужения области не выполнялось. Расширение за пределы Artifact не выполнялось: непроанализированная область (NAS-01…NAS-07) в Test Scope не входит.

### 2.2. Ограничения тестирования (переданы/выведены)

| ID | Ограничение | Влияние на модель |
|---|---|---|
| L-01 | Тестовые данные зарегистрированных пользователей в Artifact не определены (DEP-01, NAS-04) | в предусловиях используется ссылка «Email и пароль из тестовых данных среды» без подстановки значений; примеры значений в шагах помечены как примеры формата |
| L-02 | Управление системным временем недоступно/не подтверждено (B-07, NB-14) | проверки срока Remember me (30 дней, отсутствие продления, истечение) не покрыты исполняемыми тест-кейсами (TC-48, TC-49 — `BLOCKED`) |
| L-03 | Механизм и хранилище сохранённой авторизации вне области требований (DEP-02, NAS-05) | проверяется только наблюдаемое поведение, без проверки cookie/token и срока хранения |
| L-04 | Поведение защищённых страниц и контроль доступа вне формы не описаны (NB-12, NAS-06) | для проверок сессии фиксируется только наблюдаемое «авторизован / требуется авторизация», маршрут и код ответа не проверяются |
| L-05 | Справочник сообщений и локализация отсутствуют (DEP-04, NB-03) | проверяются только тексты, подтверждённые страницей требований и решениями владельца; локализация не проверяется |
| L-06 | Проект Qase AUTH не содержит custom fields и проектных правил маппинга | `priority` передан значениями Qase (`high`/`medium`), `test_type` сохранён тегом как есть, поведение — полем `behavior` (см. раздел 13) |

### 2.3. Требования со статусом покрытия

Статусы: `COVERED`, `PARTIAL`, `NOT_COVERABLE`. `OUT_OF_SCOPE` не применялся — вся область Artifact входит в тестирование.

| REQ | Содержание (сокращённо) | `coverage_status` | Тест-кейсы | Причина `PARTIAL` / `NOT_COVERABLE` |
|---|---|---|---|---|
| REQ-01 | Поле Email | `COVERED` | TC-01 | — |
| REQ-02 | Поле Password | `COVERED` | TC-01 | — |
| REQ-03 | Чекбокс Remember me, по умолчанию снятый | `COVERED` | TC-03, TC-44 | — |
| REQ-04 | Кнопка Login | `COVERED` | TC-01 | — |
| REQ-05 | Email и Password обязательны | `COVERED` | TC-04, TC-08 | — |
| REQ-06 | «Это поле обязательно» для пустого/пробельного поля | `COVERED` | TC-04, TC-05, TC-06, TC-07, TC-08 | — |
| REQ-07 | Проверка обоих полей и одновременный показ всех ошибок | `COVERED` | TC-04, TC-09, TC-34 | — |
| REQ-08 | Формат проверяется только для заполненных полей | `COVERED` | TC-08 | — |
| REQ-09 | При открытии ошибок нет | `COVERED` | TC-02, TC-10 | — |
| REQ-10 | Повторная проверка после первой попытки входа | `COVERED` | TC-10, TC-11, TC-12 | — |
| REQ-11 | При ошибках запрос не отправляется | `COVERED` | TC-04, TC-05, TC-06, TC-09, TC-14, TC-31, TC-43 | — |
| REQ-12 | Обрезка пробелов в начале и конце Email | `COVERED` | TC-24, TC-42 | точка применения лимита 254 относительно обрезки — NB-06 (см. ограничения) |
| REQ-13 | Пробелы внутри Email не допускаются | `COVERED` | TC-16 | — |
| REQ-14 | Структура Email: имя + `@` + домен | `COVERED` | TC-13, TC-14, TC-15 | — |
| REQ-15 | Набор символов имени пользователя | `COVERED` | TC-13, TC-18 | позиции точки и подряд идущие точки в имени — NB-05 (не покрыто) |
| REQ-16 | Набор символов домена | `COVERED` | TC-13, TC-23 | позиции дефиса в метках — NB-05 (не покрыто) |
| REQ-17 | Домен минимум из двух частей, поддомены разрешены | `COVERED` | TC-19, TC-20 | — |
| REQ-18 | Точка не первая и не последняя в домене | `COVERED` | TC-21, TC-22 | — |
| REQ-19 | Email без кириллицы | `COVERED` | TC-17 | — |
| REQ-20 | Максимальная длина Email 254 символа | `PARTIAL` | TC-25, TC-26 | NB-06: единица измерения (символы/байты) и точка применения лимита не определены; покрыты только ASCII-значения |
| REQ-21 | Email сравнивается без учёта регистра | `COVERED` | TC-27 | — |
| REQ-22 | «Неверный email или пароль» при нарушении формата Email, запрос не отправляется | `COVERED` | TC-09, TC-14…TC-23, TC-25, TC-26, TC-43 | — |
| REQ-23 | Длина пароля 8–64 | `COVERED` | TC-07, TC-29, TC-30, TC-31, TC-32, TC-33 | — |
| REQ-24 | Сообщение о длине пароля | `COVERED` | TC-31, TC-32, TC-33, TC-34 | — |
| REQ-25 | При неверной длине запрос не отправляется | `COVERED` | TC-31, TC-32, TC-33, TC-34 | — |
| REQ-26 | Набор символов пароля | `COVERED` | TC-28, TC-34, TC-35, TC-36, TC-37 | — |
| REQ-27 | Пробелы в пароле разрешены; пароль из пробелов допустим | `COVERED` | TC-06, TC-07, TC-33, TC-36, TC-37 | — |
| REQ-28 | Проверка пароля регистрозависима | `COVERED` | TC-38 | — |
| REQ-29 | «Неверный email или пароль» при нарушении формата пароля | `COVERED` | TC-34, TC-35, TC-36, TC-37 | — |
| REQ-30 | Успешная авторизация и переход на `/dashboard` | `COVERED` | TC-39, TC-24, TC-27 | — |
| REQ-31 | Неуспешная авторизация: сообщение, отсутствие авторизации, сохранение значений | `COVERED` | TC-40, TC-41, TC-42, TC-38 | размещение серверного сообщения не проверяется — аспект исключён из области требований (BLK-03 п. 7); жизненный цикл сообщения — NB-01 (не покрыт) |
| REQ-32 | Remember me: сохранение на 30 дней с момента входа | `PARTIAL` | TC-44 | проверено наблюдаемое сохранение после перезапуска браузера; срок 30 дней не проверяется — NB-14 и отсутствие управления временем (L-02) |
| REQ-33 | Срок не продлевается при активности | `NOT_COVERABLE` | TC-49 (`BLOCKED`) | NB-14: исчисление срока не определено; требуется управление временем |
| REQ-34 | Авторизация действует только в текущем профиле браузера | `COVERED` | TC-47 | покрыт сценарий второго профиля; иные способы завершения сохранённой авторизации — NB-13 (не покрыто) |
| REQ-35 | После истечения 30 дней переход на `/login` без сообщения | `NOT_COVERABLE` | TC-48 (`BLOCKED`) | NB-14 + отсутствие управления временем (L-02); границы 29/30/31 день не имеют согласованной трактовки |
| REQ-36 | Без Remember me сессия завершается после закрытия браузера | `COVERED` | TC-45 | ограничение срока/неактивности для режима без Remember me не задано — NB-09 (риск, не покрыто) |
| REQ-37 | Закрытие вкладки, новая вкладка, переходы не завершают сессию | `COVERED` | TC-46 | — |

Требования без записи в таблице отсутствуют.

## 3. Test Strategy

### 3.1. Применяемые техники по функциональным областям

| Функциональная область | Техники | Типы проверок | Обоснование |
|---|---|---|---|
| Состав формы и первоначальное состояние (REQ-01…REQ-04, REQ-09) | проверка состояния UI по AC-01, AC-02 | `POSITIVE` | состав формы и отсутствие ошибок при открытии — основа всех остальных проверок |
| Обязательность полей и модель сообщений (REQ-05…REQ-08) | `Equivalence Partitioning` (пусто / только пробелы / заполнено), таблица решений (какое сообщение показывается, сколько сообщений) | `NEGATIVE`, `POSITIVE` | решения владельца по BLK-01…BLK-03 определили текст, место и количество сообщений → поведение стало проверяемым |
| Момент повторной проверки (REQ-10) | state-based: до первой попытки / после первой попытки; триггеры «ввод» и «вставка из буфера» | `VALIDATION`, `POSITIVE`, `NEGATIVE` | BLK-04 п. 8–9 задаёт два триггера и точку начала; прочие события (RES-02) не регламентированы и не тестируются |
| Формат Email (REQ-13…REQ-20) | `Equivalence Partitioning` (классы нарушения структуры, набора символов, домена, кириллицы, внутренних пробелов), `Boundary Value Analysis` (254/255) | `NEGATIVE`, `POSITIVE`, `BOUNDARY` | BR-05 перечисляет конкретные правила и наборы символов; B-01 задаёт границу длины |
| Нормализация и сравнение Email (REQ-12, REQ-21) | проверка наблюдаемого эффекта обрезки и регистронезависимого сравнения через результат авторизации | `POSITIVE` | VR-02, VR-07 задают наблюдаемый эффект |
| Формат и длина пароля (REQ-23…REQ-29) | `Boundary Value Analysis` (7/8/64/65, 7 символов пробела), `Equivalence Partitioning` (допустимые/недопустимые символы, whitespace-классы) | `NEGATIVE`, `POSITIVE`, `BOUNDARY` | BLK-01 и BLK-02 закрыли трактовку пробелов и приоритет сообщения о длине |
| Регистрозависимость пароля (REQ-28) | проверка сравнения с учётной записью | `NEGATIVE` | VR-07, AC-13 |
| Успешная авторизация (REQ-30) | проверка основного потока до перехода на `/dashboard` | `POSITIVE` | PF-01, AC-11 |
| Неуспешная авторизация и состояние полей (REQ-31) | проверка сообщения, отсутствия авторизации, состояния полей (нормализация Email / отсутствие обрезки пароля) | `NEGATIVE` | BLK-05 п. 10–11 и BR-13 задают наблюдаемое состояние полей |
| Remember me (REQ-32…REQ-37) | проверка наблюдаемого сохранения/завершения сессии, область действия профиля | `POSITIVE`, `NEGATIVE` | наблюдаемая часть BR-07; срок и его исчисление не проверяются (NB-14) |
| Риск совпадения текстов ошибок (NB-07) | риск-ориентированная проверка различимости причин по наличию сетевого запроса | `RISK_BASED` | риск зафиксирован в Artifact (NB-07); Expected Result не добавляет нового поведения продукта |

### 3.2. Что сознательно не покрывается

NFR (безопасность, доступность, браузеры, локализация), серверные и сетевые сбои, жизненный цикл серверного сообщения, неопределённые позиции точек/дефисов, исчисление 30-дневного срока, иные способы завершения сохранённой авторизации, поведение защищённых страниц, состояние кнопки Login во время запроса, автозаполнение и программное изменение значения. Полный перечень с причинами — раздел 12.

### 3.3. Рассмотренные варианты стратегии

| Вариант | Полнота | Риск | Решение |
|---|---|---|---|
| A. Полное покрытие каждого пункта REQ отдельным тест-кейсом | максимальная | высокая стоимость поддержки, много почти совпадающих кейсов | отклонён |
| B. Покрытие по блокам требований с одним поведением на тест-кейс и объединением однотипных нарушений формата в классы эквивалентности | высокая по подтверждённому поведению | средняя стоимость, сохранена проверяемость каждого правила | **принят** |
| C. Минимальный smoke-набор (только позитивные потоки и основные ошибки) | низкая | непокрытые правила валидации и модель сообщений | отклонён |

Обоснование выбора B: Artifact содержит 37 требований и 25 проверяемых критериев прикладного уровня; вариант B сохраняет проверяемость каждого правила AC/VR без дублирования однотипных негативных проверок.

## 4. Test Scenarios

| `scenario_ref` | `title` | `intent` | `source_requirements` | `related_risks` | `case_refs` |
|---|---|---|---|---|---|
| SC-01 | Состав формы и первоначальное состояние | подтвердить наличие элементов формы и отсутствие ошибок до действий пользователя | REQ-01…REQ-04, REQ-09; AC-01, AC-02; PF-06 | — | TC-01, TC-02, TC-03 |
| SC-02 | Обязательность полей | проверить обязательность Email и Password, включая правило для значения из пробелов | REQ-05, REQ-06, REQ-08; AC-03, AC-04, AC-21; VR-01; PF-08, PF-09; NF-01, NF-02 | — | TC-04, TC-05, TC-06, TC-07, TC-08 |
| SC-03 | Модель и количество клиентских сообщений | проверить одновременный показ ошибок, их место и количество | REQ-07; AC-24; VR-08; NF-12; BR-14 | — | TC-09 |
| SC-04 | Повторная проверка после первой попытки входа | проверить момент начала и триггеры повторной проверки | REQ-09, REQ-10; AC-15; VR-09; PF-07; NF-17; BR-12 | — | TC-10, TC-11, TC-12 |
| SC-05 | Структура Email и наборы символов | проверить состав Email, наборы символов имени и домена, кириллицу, внутренние пробелы | REQ-13…REQ-16, REQ-19, REQ-22; AC-05, AC-07; VR-03 | — | TC-13, TC-14, TC-15, TC-16, TC-17, TC-18 |
| SC-06 | Домен Email: части, поддомены, позиция точки | проверить требования к доменной части и позиции точки | REQ-16…REQ-18; AC-08; B-03, B-04 | — | TC-19, TC-20, TC-21, TC-22, TC-23 |
| SC-07 | Нормализация Email | проверить удаление пробелов в начале и конце Email до проверки | REQ-12, REQ-30; VR-02; PF-03 | — | TC-24 |
| SC-08 | Границы длины Email | проверить значения на границе и за границей 254 символов | REQ-20, REQ-22; AC-06; B-01; VR-04 | — | TC-25, TC-26 |
| SC-09 | Регистронезависимость Email | проверить сравнение Email с зарегистрированным без учёта регистра | REQ-21, REQ-30; AC-12; VR-07; PF-02 | — | TC-27 |
| SC-10 | Длина пароля и сообщение о длине | проверить границы длины и приоритет сообщения о длине | REQ-23…REQ-25; AC-09, AC-22; B-02, B-10; VR-05; NF-05, NF-14, NF-16 | — | TC-29, TC-30, TC-31, TC-32, TC-33, TC-34 |
| SC-11 | Набор символов и whitespace-классы пароля | проверить допустимые символы и трактовку пробелов (пробел, табуляция, неразрывный пробел) | REQ-26, REQ-27, REQ-29; AC-10, AC-23; VR-06; B-05; NF-06, NF-13 | — | TC-28, TC-35, TC-36, TC-37 |
| SC-12 | Регистрозависимость пароля | проверить сравнение пароля с учётом регистра | REQ-28, REQ-31; AC-13; VR-07; NF-09 | — | TC-38 |
| SC-13 | Успешная авторизация | проверить авторизацию и переход на `/dashboard` | REQ-30; AC-11; PF-01; BR-09 | — | TC-39 |
| SC-14 | Неуспешная авторизация и состояние полей | проверить сообщение, отсутствие авторизации и состояние полей после отказа | REQ-31; AC-14, AC-25; VR-10; B-11; NF-07, NF-08, NF-15 | NB-08 | TC-40, TC-41, TC-42 |
| SC-15 | Различимость клиентской и серверной ошибки при совпадающем тексте | зафиксировать риск неузнаваемости причины отказа по тексту сообщения | REQ-22, REQ-31; AC-20; NF-07 | NB-07 | TC-43 |
| SC-16 | Remember me: сохранение и область действия | проверить наблюдаемое сохранение авторизации и ограничение профилем браузера | REQ-32, REQ-34, REQ-35, REQ-33; AC-16, AC-17, AC-18; PF-04; NF-10 | NB-13, NB-14 | TC-44, TC-47, TC-48, TC-49 |
| SC-17 | Завершение сессии без Remember me | проверить завершение сессии при закрытии браузера и сохранение сессии внутри вкладок | REQ-36, REQ-37; AC-19; PF-05; NF-11 | NB-09 | TC-45, TC-46 |

## 5. Test Suites

Все разделы созданы на корневом уровне проекта AUTH (`parent_id = null`), вложенность не применялась: требования образуют один уровень логических блоков (разделы 1–7 страницы требований).

| `suite_ref` | `title` | `parent_ref` | `source_requirements` | `suite_decision` | `existing_suite_id` | `creation_status` | `qase_suite_id` | `error` |
|---|---|---|---|---|---|---|---|---|
| SUITE-01 | Состав формы и первоначальное состояние | — | REQ-01…REQ-04, REQ-09; AC-01, AC-02; PF-06 | `CREATE` | Не обнаружено | `CREATED` | 19 | — |
| SUITE-02 | Обязательность полей и клиентские сообщения | — | REQ-05…REQ-11; AC-03, AC-04, AC-15, AC-20, AC-21, AC-24; VR-01, VR-08, VR-09; PF-07, PF-08, PF-09; NF-01, NF-02, NF-12, NF-14, NF-17; BR-01…BR-03, BR-10, BR-12, BR-14 | `CREATE` | Не обнаружено | `CREATED` | 20 | — |
| SUITE-03 | Валидация формата Email | — | REQ-12…REQ-22; AC-05…AC-08, AC-12, AC-20; VR-02, VR-03, VR-04; B-01, B-03, B-04; PF-02, PF-03; NF-02…NF-04 | `CREATE` | Не обнаружено | `CREATED` | 21 | — |
| SUITE-04 | Валидация формата и длины пароля | — | REQ-23…REQ-29; AC-09, AC-10, AC-13, AC-22, AC-23; VR-05, VR-06, VR-07; B-02, B-05, B-10; NF-05, NF-06, NF-09, NF-13, NF-14, NF-16 | `CREATE` | Не обнаружено | `CREATED` | 22 | — |
| SUITE-05 | Успешная авторизация | — | REQ-30; AC-11; PF-01; BR-09 | `CREATE` | Не обнаружено | `CREATED` | 23 | — |
| SUITE-06 | Неуспешная авторизация | — | REQ-31; AC-14, AC-20, AC-25; VR-10; B-11; NF-07, NF-08, NF-15; риск NB-07 | `CREATE` | Не обнаружено | `CREATED` | 24 | — |
| SUITE-07 | Сохранение авторизации (Remember me) | — | REQ-03, REQ-32…REQ-37; AC-16…AC-19; B-07; PF-04, PF-05; NF-10, NF-11 | `CREATE` | Не обнаружено | `CREATED` | 25 | — |

Примечание к SUITE-05: раздел содержит одно требование (REQ-30) и один позитивный поток (PF-01). Сценарии, где успешный вход наблюдается как эффект правил Email (нормализация REQ-12, регистронезависимость REQ-21), размещены в SUITE-03, чтобы каждое требование покрывалось тест-кейсами одного раздела. Раздел содержит `READY`-тест-кейс и создан по правилам Skill.

## 6. Test Cases

Обозначения: `priority` — `HIGH`/`MEDIUM`/`LOW`; `priority_source` — `RISK_ANALYSIS` (критичность поведения для основной функции) или `REQUIREMENT_REVIEW` (следует из закрытых находок Artifact); `test_type` — по Skill. Шаги приведены в виде «действие → ожидаемый результат шага».

### SUITE-01 «Состав формы и первоначальное состояние» (`qase_suite_id` 19)

**TC-01** — Форма авторизации содержит поля Email, Password, чекбокс Remember me и кнопку Login
- `scenario_ref` SC-01 · `suite_ref` SUITE-01 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-01, REQ-02, REQ-03, REQ-04; AC-01; BR-01
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) осмотреть состав формы → на форме присутствуют поле Email, поле Password, чекбокс Remember me, кнопка Login
- `expected_result` Форма содержит все четыре элемента, перечисленные в REQ-01…REQ-04 (AC-01)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 126

**TC-02** — При первоначальном открытии формы сообщения об ошибках отсутствуют
- `scenario_ref` SC-01 · `suite_ref` SUITE-01 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-09; AC-02; PF-06; BR-01
- `preconditions` Пользователь не авторизован; поля пусты; страница авторизации в текущей сессии не открывалась
- `steps` 1) открыть страницу авторизации → сообщений об ошибках нет ни у полей, ни в иной части формы; 2) не выполняя ввода, осмотреть форму повторно → сообщения не появляются
- `expected_result` На первоначальном открытии формы ни одного сообщения об ошибке не отображается (AC-02; REQ-09)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 127

**TC-03** — Чекбокс Remember me при первоначальном открытии снят
- `scenario_ref` SC-01 · `suite_ref` SUITE-01 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-03; AC-01; PF-06; BR-01, BR-07
- `preconditions` Пользователь не авторизован; страница авторизации в текущей сессии не открывалась
- `steps` 1) открыть страницу авторизации и проверить состояние чекбокса → чекбокс Remember me снят
- `expected_result` Remember me по умолчанию снят (REQ-03; PF-06)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 128

### SUITE-02 «Обязательность полей и клиентские сообщения» (`qase_suite_id` 20)

**TC-04** — Login при пустых Email и Password: сообщение «Это поле обязательно» у обоих полей
- `scenario_ref` SC-02 · `suite_ref` SUITE-02 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-05, REQ-06, REQ-07, REQ-11; AC-03, AC-20; VR-01, VR-08; NF-01; BR-02, BR-03, BR-14
- `preconditions` Пользователь не авторизован; открыта страница авторизации; поля Email и Password пусты
- `steps` 1) оставить поля пустыми → сообщений нет; 2) нажать Login → «Это поле обязательно» у каждого поля (два сообщения); 3) проверить сетевой запрос → запрос не отправляется, пользователь не авторизован
- `expected_result` Два сообщения «Это поле обязательно» — по одному у каждого поля; запрос на авторизацию не отправляется (AC-03; AC-20)
- `duplicate_check_result` RELATED (другой проект SHARELANE) → создаётся · `creation_status` CREATED · `qase_case_id` 129

**TC-05** — Email из одних пробелов: сообщение «Это поле обязательно» у поля Email
- `scenario_ref` SC-02 · `suite_ref` SUITE-02 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-06, REQ-11; AC-04, AC-20; VR-01; NF-02; BR-02, BR-03, BR-14
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = «     » (5 пробелов); 2) Password = password1; 3) нажать Login → «Это поле обязательно» только у Email, у Password клиентских сообщений нет; 4) проверить запрос → не отправляется
- `expected_result` Значение из одних пробелов в Email приравнивается к пустому полю: одно сообщение у поля Email; запрос не отправляется (AC-04; VR-01)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 130

**TC-06** — Пустой Email и пароль из 8 символов пробела: сообщение только у поля Email
- `scenario_ref` SC-02 · `suite_ref` SUITE-02 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-06, REQ-11, REQ-23; AC-21, AC-20; VR-01; PF-09; BR-02, BR-03 (BLK-01 п. 1)
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email — пусто; 2) Password = 8 символов пробела; 3) нажать Login → одно сообщение «Это поле обязательно» у Email, у Password сообщений нет; 4) проверить запрос → не отправляется
- `expected_result` У поля Password отсутствуют и сообщение обязательности, и сообщение о длине; единственное сообщение — у поля Email; запрос не отправляется (PF-09; AC-21)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 131

**TC-07** — Пароль из 8 символов пробела при валидном Email: сообщение обязательности не отображается, запрос отправляется
- `scenario_ref` SC-02 · `suite_ref` SUITE-02 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-06, REQ-23, REQ-27; AC-21; VR-01; PF-08; BR-02 (BLK-01 п. 1)
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = 8 символов пробела; 3) нажать Login → у Password нет сообщения обязательности и сообщения о длине; 4) проверить запрос → отправляется
- `expected_result` Whitespace-пароль считается заполненным и проходит проверку длины 8–64; запрос на авторизацию отправляется (AC-21; PF-08)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 132

**TC-08** — Проверка формата выполняется только для заполненных полей
- `scenario_ref` SC-02 · `suite_ref` SUITE-02 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-08; AC-03, AC-20; VR-01; BR-10
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password — пусто; 3) нажать Login → у Password «Это поле обязательно», у Email сообщений нет; 4) проверить запрос → не отправляется
- `expected_result` Формат проверяется только для заполненных полей: сообщение только у пустого поля (REQ-08; BR-10)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 133

**TC-09** — Одновременное нарушение в обоих полях: ровно два клиентских сообщения
- `scenario_ref` SC-03 · `suite_ref` SUITE-02 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-07, REQ-22, REQ-24, REQ-11; AC-24, AC-20; VR-08; NF-12; BR-10, BR-14
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = userexample.com; 2) Password = abcdefg (7 символов); 3) нажать Login → «Неверный email или пароль» у Email и «Пароль должен содержать от 8 до 64 символов» у Password, всего два сообщения; 4) проверить запрос → не отправляется
- `expected_result` Ровно два клиентских сообщения, по одному у каждого поля, показаны одновременно (AC-24; VR-08; NF-12)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 134

**TC-10** — До первой попытки входа ввод значения не вызывает клиентских сообщений
- `scenario_ref` SC-04 · `suite_ref` SUITE-02 · `priority` MEDIUM (`REQUIREMENT_REVIEW`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-09, REQ-10; AC-15; VR-09; NF-17; BR-12 (BLK-04 п. 9)
- `preconditions` Пользователь не авторизован; страница открыта; кнопка Login в текущей сессии не нажималась
- `steps` 1) Email = userexample.com → сообщений нет; 2) Password = abcdefg → сообщений нет; 3) убрать фокус и осмотреть форму → сообщений нет
- `expected_result` До нажатия Login повторная проверка не запускается, клиентские сообщения отсутствуют (NF-17; BLK-04 п. 9)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 135

**TC-11** — После первой попытки входа ввод в поле перепроверяет оба поля без повторного нажатия Login
- `scenario_ref` SC-04 · `suite_ref` SUITE-02 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` VALIDATION · `case_status` READY
- `source_requirements` REQ-10; AC-15; VR-09; PF-07; BR-12, BR-10 (BLK-04 п. 8)
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) нажать Login при пустых полях → два сообщения «Это поле обязательно»; 2) ввести в Email один символ `a` без Login → у Email сообщение меняется на «Неверный email или пароль», у Password остаётся «Это поле обязательно» (проверены оба поля); 3) продолжить ввод до user_name-01@example.com → сообщение у Email снимается без нажатия Login, у Password остаётся
- `expected_result` После первой попытки входа ввод символа запускает повторную проверку обоих полей; сообщения обновляются и снимаются без повторного нажатия Login (AC-15; PF-07; VR-09)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 136

**TC-12** — После первой попытки входа вставка значения из буфера запускает повторную проверку
- `scenario_ref` SC-04 · `suite_ref` SUITE-02 · `priority` MEDIUM (`REQUIREMENT_REVIEW`) · `test_type` VALIDATION · `case_status` READY
- `source_requirements` REQ-10; AC-15; VR-09; PF-07; BR-12 (BLK-04 п. 8)
- `preconditions` Открыта страница авторизации; в буфере обмена значение userexample.com
- `steps` 1) нажать Login при пустых полях → два сообщения; 2) вставить значение из буфера в Email без Login → у Email «Неверный email или пароль», у Password «Это поле обязательно»
- `expected_result` Вставка из буфера запускает повторную проверку обоих полей (AC-15; VR-09; BLK-04 п. 8)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 137

### SUITE-03 «Валидация формата Email» (`qase_suite_id` 21)

**TC-13** — Валидный Email проходит клиентскую проверку: сообщений нет, запрос отправляется
- `scenario_ref` SC-05 · `suite_ref` SUITE-03 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-14, REQ-15, REQ-16; AC-05 (обратная формулировка), AC-20; VR-03; BR-05
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = password1; 3) нажать Login → клиентских сообщений нет; 4) проверить запрос → отправляется
- `expected_result` Значение, соответствующее BR-05, не вызывает клиентских сообщений; запрос на авторизацию отправляется (BR-03)
- `duplicate_check_result` RELATED (другой проект SHARELANE) → создаётся · `creation_status` CREATED · `qase_case_id` 138

**TC-14** — Email без символа @ отклоняется
- `scenario_ref` SC-05 · `suite_ref` SUITE-03 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-14, REQ-22; AC-05, AC-20; VR-03; NF-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = userexample.com; 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Отсутствие обязательных частей Email приводит к сообщению «Неверный email или пароль» у поля Email и блокировке запроса (AC-05)
- `duplicate_check_result` RELATED (другой проект SHARELANE) → создаётся · `creation_status` CREATED · `qase_case_id` 139

**TC-15** — Email без домена отклоняется
- `scenario_ref` SC-05 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-14, REQ-22; AC-05, AC-20; VR-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user@; 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Отсутствие доменной части — нарушение формата: сообщение у поля Email, запрос не отправляется (REQ-14)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 140

**TC-16** — Email с пробелом внутри отклоняется
- `scenario_ref` SC-05 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-12, REQ-13, REQ-22; AC-05, AC-20; VR-03; NF-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user name@example.com; 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Удаляются только пробелы по краям; внутренний пробел остаётся нарушением формата (REQ-13; VR-03)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 141

**TC-17** — Email с кириллическими символами отклоняется
- `scenario_ref` SC-05 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-19, REQ-22; AC-07, AC-20; VR-03; NF-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = пользователь@example.com; 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Кириллица в Email отклоняется с сообщением у поля Email (AC-07; REQ-19)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 142

**TC-18** — Недопустимый символ в имени пользователя Email отклоняется
- `scenario_ref` SC-05 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-15, REQ-22; AC-05, AC-20; VR-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = userü@example.com; 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Символ вне перечня REQ-15 в имени пользователя — нарушение формата (VR-03)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 143

**TC-19** — Домен Email из одной части отклоняется
- `scenario_ref` SC-06 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-17, REQ-22; AC-08, AC-20; B-03; VR-03; NF-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user@example; 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Домен из одной части — нарушение: требуется минимум две части (AC-08; B-03)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 144

**TC-20** — Домен Email с поддоменом принимается
- `scenario_ref` SC-06 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` BOUNDARY · `case_status` READY
- `source_requirements` REQ-17; AC-08; B-03; VR-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user@a.example.com; 2) Password = password1; 3) нажать Login → клиентских сообщений нет; 4) проверить запрос → отправляется
- `expected_result` Домен из трёх частей с поддоменом допустим (AC-08; B-03)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 145

**TC-21** — Точка первым символом домена Email отклоняется
- `scenario_ref` SC-06 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-18, REQ-22; AC-08, AC-20; B-04; VR-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user@.example.com; 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Точка не может быть первым символом домена (REQ-18; B-04)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 146

**TC-22** — Точка последним символом домена Email отклоняется
- `scenario_ref` SC-06 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-18, REQ-22; AC-08, AC-20; B-04; VR-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user@example.com.; 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Точка не может быть последним символом домена (REQ-18; B-04)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 147

**TC-23** — Недопустимый символ в домене Email отклоняется
- `scenario_ref` SC-06 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-16, REQ-22; AC-05, AC-20; VR-03
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user@exa_mple.com; 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Домен содержит только латинские буквы, цифры, дефисы и точки; символ `_` — нарушение (REQ-16)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 148

**TC-24** — Пробелы в начале и конце Email удаляются до проверки: авторизация выполняется
- `scenario_ref` SC-07 · `suite_ref` SUITE-03 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-12, REQ-30; AC-11; VR-02; PF-03; BR-04
- `preconditions` Зарегистрирован пользователь user@example.com с известным правильным паролем (тестовые данные среды; DEP-01); пользователь не авторизован
- `steps` 1) Email = « user@example.com » (пробелы по краям); 2) правильный пароль; 3) нажать Login → проверка формата пройдена, авторизация выполнена, переход на /dashboard
- `expected_result` Пробелы по краям удалены до проверки; авторизация выполнена, выполнен переход на /dashboard (PF-03; VR-02)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 149

**TC-25** — Email длиной 254 символа проходит проверку длины
- `scenario_ref` SC-08 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` BOUNDARY · `case_status` READY
- `source_requirements` REQ-20; AC-06; B-01; VR-04
- `preconditions` Открыта страница авторизации; подготовлено значение ровно из 254 ASCII-символов
- `steps` 1) Email = 242 символа `a` + @example.com (254 символа); 2) Password = password1; 3) нажать Login → клиентских сообщений у Email нет; 4) проверить запрос → отправляется
- `expected_result` Значение на границе 254 символа проходит проверку длины (AC-06; B-01). Единица измерения лимита не проверяется — NB-06
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 150

**TC-26** — Email длиной 255 символов отклоняется
- `scenario_ref` SC-08 · `suite_ref` SUITE-03 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` BOUNDARY · `case_status` READY
- `source_requirements` REQ-20, REQ-22; AC-06, AC-20; B-01; VR-04
- `preconditions` Открыта страница авторизации; подготовлено значение ровно из 255 ASCII-символов
- `steps` 1) Email = 243 символа `a` + @example.com (255 символов); 2) Password = password1; 3) нажать Login → «Неверный email или пароль» у Email; 4) проверить запрос → не отправляется
- `expected_result` Значение за границей 254 символа не проходит проверку длины (AC-06; B-01)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 151

**TC-27** — Email в ином регистре при правильном пароле: авторизация выполняется
- `scenario_ref` SC-09 · `suite_ref` SUITE-03 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-21, REQ-30; AC-12; VR-07; PF-02; BR-06
- `preconditions` Зарегистрирован пользователь user@example.com с правильным паролем (тестовые данные среды; DEP-01)
- `steps` 1) Email = USER@EXAMPLE.COM; 2) правильный пароль; 3) нажать Login → авторизация выполнена, переход на /dashboard
- `expected_result` Email сравнивается с зарегистрированным без учёта регистра: авторизация выполнена (AC-12; VR-07; PF-02)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 152

### SUITE-04 «Валидация формата и длины пароля» (`qase_suite_id` 22)

**TC-28** — Пароль допустимого формата проходит клиентскую проверку
- `scenario_ref` SC-11 · `suite_ref` SUITE-04 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-26; AC-10 (обратная формулировка), AC-20; VR-06; BR-05
- `preconditions` Пользователь не авторизован; открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = P@ssw0rd! (8 допустимых символов); 3) нажать Login → клиентских сообщений у Password нет; 4) проверить запрос → отправляется
- `expected_result` Латиница, цифры и перечисленные спецсимволы входят в допустимый набор (REQ-26; VR-06)
- `duplicate_check_result` RELATED (другой проект SHARELANE) → создаётся · `creation_status` CREATED · `qase_case_id` 153

**TC-29** — Пароль длиной 8 символов проходит проверку длины
- `scenario_ref` SC-10 · `suite_ref` SUITE-04 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` BOUNDARY · `case_status` READY
- `source_requirements` REQ-23; AC-09; B-02; VR-05
- `preconditions` Открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = abcdefg1 (8 символов); 3) нажать Login → сообщения о длине нет; 4) проверить запрос → отправляется
- `expected_result` Нижняя граница 8 символов входит в допустимый диапазон (AC-09; B-02)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 154

**TC-30** — Пароль длиной 64 символа проходит проверку длины
- `scenario_ref` SC-10 · `suite_ref` SUITE-04 · `priority` MEDIUM (`RISK_ANALYSIS`) · `test_type` BOUNDARY · `case_status` READY
- `source_requirements` REQ-23; AC-09; B-02; VR-05
- `preconditions` Открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = 64 символа `a`; 3) нажать Login → сообщения о длине нет; 4) проверить запрос → отправляется
- `expected_result` Верхняя граница 64 символа входит в допустимый диапазон (AC-09; B-02)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 155

**TC-31** — Пароль длиной 7 символов отклоняется по длине
- `scenario_ref` SC-10 · `suite_ref` SUITE-04 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` BOUNDARY · `case_status` READY
- `source_requirements` REQ-24, REQ-25; AC-09, AC-20; B-02; VR-05; NF-05; BR-10
- `preconditions` Открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = abcdefg (7 символов); 3) нажать Login → «Пароль должен содержать от 8 до 64 символов», иного сообщения у поля нет; 4) проверить запрос → не отправляется
- `expected_result` Значение ниже границы даёт сообщение о длине и блокирует запрос (AC-09; VR-05; NF-05)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 156

**TC-32** — Пароль длиной 65 символов отклоняется по длине
- `scenario_ref` SC-10 · `suite_ref` SUITE-04 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` BOUNDARY · `case_status` READY
- `source_requirements` REQ-24, REQ-25; AC-09, AC-20; B-02; VR-05; NF-05; BR-10
- `preconditions` Открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = 65 символов `a`; 3) нажать Login → «Пароль должен содержать от 8 до 64 символов»; 4) проверить запрос → не отправляется
- `expected_result` Значение выше границы даёт сообщение о длине и блокирует запрос (AC-09; VR-05; NF-05)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 157

**TC-33** — Пароль из 7 символов пробела отклоняется по длине
- `scenario_ref` SC-10 · `suite_ref` SUITE-04 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` BOUNDARY · `case_status` READY
- `source_requirements` REQ-23, REQ-24, REQ-25, REQ-27; AC-22, AC-20; B-10; VR-05; NF-14 (BLK-01 п. 1, BLK-02 п. 3)
- `preconditions` Открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = 7 символов пробела; 3) нажать Login → «Пароль должен содержать от 8 до 64 символов», сообщения обязательности нет; 4) проверить запрос → не отправляется
- `expected_result` Whitespace-пароль подчиняется правилу длины: сообщение о длине, запрос не отправляется (AC-22; B-10)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 158

**TC-34** — Неверная длина пароля при недопустимом символе: отображается только сообщение о длине
- `scenario_ref` SC-10 · `suite_ref` SUITE-04 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` VALIDATION · `case_status` READY
- `source_requirements` REQ-24, REQ-29, REQ-07; AC-24 (модель сообщений), AC-20; VR-05, VR-08; NF-16; BR-10 (BLK-02 п. 3–4 + BLK-03 п. 6)
- `preconditions` Открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = Пароль1 (7 символов, содержит кириллицу); 3) нажать Login → у Password одно сообщение «Пароль должен содержать от 8 до 64 символов», «Неверный email или пароль» у поля нет; 4) проверить запрос → не отправляется
- `expected_result` При одновременном нарушении длины и набора символов у поля Password остаётся единственное сообщение о длине (NF-16; VR-05; BR-10)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 159

**TC-35** — Символ вне разрешённого набора в пароле отклоняется
- `scenario_ref` SC-11 · `suite_ref` SUITE-04 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-26, REQ-29; AC-10, AC-20; VR-06; NF-06
- `preconditions` Открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = Пароль12 (8 символов, кириллица); 3) нажать Login → «Неверный email или пароль» у Password; 4) проверить запрос → не отправляется
- `expected_result` Кириллица не входит в набор допустимых символов пароля при корректной длине (AC-10; VR-06; NF-06)
- `duplicate_check_result` RELATED (другой проект SHARELANE) → создаётся · `creation_status` CREATED · `qase_case_id` 160

**TC-36** — Символ табуляции в пароле отклоняется
- `scenario_ref` SC-11 · `suite_ref` SUITE-04 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-26, REQ-27, REQ-29; AC-23, AC-20; VR-06; B-05; NF-13; BR-11 (BLK-01 п. 2)
- `preconditions` Открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = pass<TAB>word (9 символов); 3) нажать Login → «Неверный email или пароль» у Password; 4) проверить запрос → не отправляется
- `expected_result` Табуляция не относится к «пробелам» и не входит в набор допустимых символов (AC-23; VR-06; BR-11)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 161

**TC-37** — Неразрывный пробел в пароле отклоняется
- `scenario_ref` SC-11 · `suite_ref` SUITE-04 · `priority` HIGH (`REQUIREMENT_REVIEW`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-26, REQ-27, REQ-29; AC-23, AC-20; VR-06; B-05; NF-13; BR-11 (BLK-01 п. 2)
- `preconditions` Открыта страница авторизации
- `steps` 1) Email = user_name-01@example.com; 2) Password = pass<NBSP>word (9 символов, U+00A0); 3) нажать Login → «Неверный email или пароль» у Password; 4) проверить запрос → не отправляется
- `expected_result` Неразрывный пробел не относится к «пробелам» и не входит в набор допустимых символов (AC-23; VR-06; BR-11)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 162

**TC-38** — Пароль, отличающийся от правильного только регистром, отклоняется
- `scenario_ref` SC-12 · `suite_ref` SUITE-04 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-28, REQ-31; AC-13; VR-07; NF-09; BR-06
- `preconditions` Зарегистрирован пользователь user@example.com с паролем Password1 (тестовые данные среды; DEP-01)
- `steps` 1) Email = user@example.com; 2) Password = password1; 3) нажать Login → «Неверный email или пароль», пользователь не авторизован, перехода на /dashboard нет
- `expected_result` Пароль сравнивается с учётом регистра: отличие регистром — неправильный пароль (AC-13; VR-07; NF-09)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 163

### SUITE-05 «Успешная авторизация» (`qase_suite_id` 23)

**TC-39** — Успешная авторизация зарегистрированного пользователя при снятом Remember me
- `scenario_ref` SC-13 · `suite_ref` SUITE-05 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-30; AC-11; PF-01; BR-09
- `preconditions` Зарегистрирован пользователь с известным правильным паролем (тестовые данные среды; DEP-01); Remember me снят; пользователь не авторизован
- `steps` 1) ввести зарегистрированный Email → сообщений нет; 2) ввести правильный пароль → сообщений нет; 3) нажать Login → клиентских сообщений нет, запрос отправляется; 4) проверить результат → пользователь авторизован, переход на /dashboard
- `expected_result` Авторизация выполнена, выполнен переход на главную страницу личного кабинета /dashboard (AC-11; PF-01; BR-09)
- `duplicate_check_result` RELATED (другой проект SHARELANE) → создаётся · `creation_status` CREATED · `qase_case_id` 164

### SUITE-06 «Неуспешная авторизация» (`qase_suite_id` 24)

**TC-40** — Незарегистрированный Email при валидном формате: сообщение, отсутствие авторизации, сохранение значений
- `scenario_ref` SC-14 · `suite_ref` SUITE-06 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-31; AC-14; NF-07; BR-08
- `preconditions` Email unregistered_user@example.com не зарегистрирован (тестовые данные среды); пользователь не авторизован
- `steps` 1) Email = unregistered_user@example.com; 2) Password = password1; 3) нажать Login → клиентских сообщений нет, запрос отправляется; 4) проверить результат → «Неверный email или пароль», пользователь не авторизован, переход на /dashboard не выполняется, значения остаются в полях
- `expected_result` Сообщение «Неверный email или пароль», авторизации нет, введённые значения сохранены (AC-14; NF-07). Место отображения сообщения не проверяется (BLK-03 п. 7)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 165

**TC-41** — Зарегистрированный Email и неправильный пароль: сообщение, отсутствие авторизации, сохранение значений
- `scenario_ref` SC-14 · `suite_ref` SUITE-06 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-31; AC-14; NF-08; BR-08
- `preconditions` Зарегистрирован пользователь user@example.com с известным правильным паролем (тестовые данные среды; DEP-01)
- `steps` 1) Email = user@example.com; 2) Password = WrongPass1 (не совпадает с правильным); 3) нажать Login → клиентских сообщений нет, запрос отправляется; 4) проверить результат → «Неверный email или пароль», авторизации нет, значения остаются в полях
- `expected_result` Сообщение «Неверный email или пароль», авторизации нет, значения сохранены (AC-14; NF-08). Маскирование пароля не проверяется — NB-03
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 166

**TC-42** — После неуспешной авторизации Email нормализован, значение пароля не обрезается
- `scenario_ref` SC-14 · `suite_ref` SUITE-06 · `priority` MEDIUM (`REQUIREMENT_REVIEW`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-12, REQ-31; AC-25; VR-10; B-11; NF-15; BR-13 (BLK-05 п. 10–11)
- `preconditions` Email unregistered_user@example.com не зарегистрирован (тестовые данные среды)
- `steps` 1) Email = « unregistered_user@example.com »; 2) Password = «  WrongPass1  » (15 символов, пробелы допустимы по REQ-27); 3) нажать Login → запрос отправляется, «Неверный email или пароль», авторизации нет; 4) проверить значения в полях → Email без пробелов по краям, Password без обрезки
- `expected_result` В поле Email остаётся нормализованное значение; в поле Password — введённое значение без обрезки пробелов (AC-25; VR-10; BR-13)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 167

**TC-43** — Совпадающий текст клиентской и серверной ошибки: различие фиксируется по наличию сетевого запроса
- `scenario_ref` SC-15 · `suite_ref` SUITE-06 · `priority` MEDIUM (`REQUIREMENT_REVIEW`) · `test_type` RISK_BASED · `related_risks` NB-07 · `case_status` READY
- `source_requirements` REQ-22, REQ-31; AC-20; NF-07
- `preconditions` Пользователь не авторизован; известен Email валидного формата, не зарегистрированный в системе
- `steps` 1) Email = userexample.com, Password = password1, Login → «Неверный email или пароль», запрос не отправляется; 2) Email = user_name-01@example.com, Password = password1, Login → тот же текст, запрос отправляется; 3) сравнить поведение → тексты идентичны, причина различима только по факту отправки запроса
- `expected_result` Наблюдаемое различие клиентской и серверной ошибки существует только по наличию сетевого запроса; размещение серверного сообщения не проверяется (NB-07; AC-20)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 168

### SUITE-07 «Сохранение авторизации (Remember me)» (`qase_suite_id` 25)

**TC-44** — Remember me установлен: авторизация сохраняется после перезапуска браузера
- `scenario_ref` SC-16 · `suite_ref` SUITE-07 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-32, REQ-36; AC-16 (частично); PF-04; BR-07
- `preconditions` Зарегистрирован пользователь с правильным паролем (DEP-01); доступен отдельный профиль браузера
- `steps` 1) установить Remember me; 2) ввести Email и правильный пароль, Login → авторизация выполнена, переход на /dashboard; 3) полностью закрыть и открыть браузер в том же профиле; 4) обратиться к системе → пользователь остаётся авторизованным, /dashboard отображается без повторного ввода
- `expected_result` Сохранённая авторизация действует после перезапуска браузера (PF-04; REQ-32; AC-16 частично). `DERIVED` — из REQ-32 в сочетании с REQ-36. Срок 30 дней и отсутствие продления не проверяются — NB-14, L-02
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 169

**TC-45** — Remember me снят: после закрытия браузера сессия завершена
- `scenario_ref` SC-17 · `suite_ref` SUITE-07 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-36; AC-19; NF-11; BR-07
- `preconditions` Remember me снят; зарегистрированный пользователь с правильным паролем (DEP-01)
- `steps` 1) выполнить успешный вход → переход на /dashboard; 2) полностью закрыть браузер; 3) открыть браузер в том же профиле и обратиться к системе → /dashboard не отображается, требуется авторизация
- `expected_result` Сессия завершена после закрытия браузера; требуется повторная авторизация (AC-19; NF-11)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 170

**TC-46** — Remember me снят: закрытие вкладки, новая вкладка и переходы между страницами не завершают сессию
- `scenario_ref` SC-17 · `suite_ref` SUITE-07 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` POSITIVE · `case_status` READY
- `source_requirements` REQ-37; AC-19; PF-05; BR-07
- `preconditions` Remember me снят; зарегистрированный пользователь с правильным паролем (DEP-01)
- `steps` 1) выполнить успешный вход → /dashboard; 2) закрыть текущую вкладку и открыть новую вкладку с системой → пользователь остаётся авторизованным; 3) перейти между несколькими страницами → пользователь остаётся авторизованным
- `expected_result` Закрытие вкладки, новая вкладка и переходы между страницами сессию не завершают (REQ-37; PF-05; AC-19)
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 171

**TC-47** — Remember me установлен: сохранённая авторизация не действует в другом профиле браузера
- `scenario_ref` SC-16 · `suite_ref` SUITE-07 · `priority` HIGH (`RISK_ANALYSIS`) · `test_type` NEGATIVE · `case_status` READY
- `source_requirements` REQ-34; AC-18; BR-07
- `preconditions` Доступны два профиля браузера; зарегистрированный пользователь с правильным паролем (DEP-01)
- `steps` 1) в профиле 1 установить Remember me и выполнить успешный вход → авторизация выполнена; 2) открыть профиль 2 и обратиться к системе → /dashboard не отображается, требуется авторизация; 3) вернуться в профиль 1 → пользователь остаётся авторизованным
- `expected_result` Сохранённая авторизация действует только в текущем профиле браузера (AC-18; REQ-34). Иные способы завершения сохранённой авторизации не проверяются — NB-13
- `duplicate_check_result` NOT_FOUND · `creation_status` CREATED · `qase_case_id` 172

### Заблокированные тест-кейсы (не создавались)

| `test_ref` | `scenario_ref` | `suite_ref` | `title` | `priority` | `test_type` | `case_status` | `block_reason` | `open_questions` | `creation_status` |
|---|---|---|---|---|---|---|---|---|---|
| TC-48 | SC-16 | SUITE-07 | Истечение 30 дней с установленным Remember me: переход на `/login` без сообщения | MEDIUM (`REQUIREMENT_REVIEW`) | STATE_TRANSITION | `BLOCKED` | NB-14: исчисление 30 дней (календарные дни или 24-часовые периоды, часовой пояс) не определено; отсутствует управление системным временем (B-07, L-02). Ожидаемый результат на границах 29/30/31 дня неопределим | NB-14, OQ-01 | `SKIPPED` (blocked) |
| TC-49 | SC-16 | SUITE-07 | Отсутствие продления срока Remember me при активности пользователя | LOW (`REQUIREMENT_REVIEW`) | STATE_TRANSITION | `BLOCKED` | NB-14 и L-02: проверка требует управления временем и согласованной трактовки срока; наблюдаемый эффект «не продлевается» без контроля времени не фиксируется | NB-14 | `SKIPPED` (blocked) |

## 7. Traceability Matrix

### 7.1. Acceptance Criteria

| AC | Тест-кейсы | `coverage_status` | Причина |
|---|---|---|---|
| AC-01 | TC-01, TC-03 | `COVERED` | — |
| AC-02 | TC-02 | `COVERED` | — |
| AC-03 | TC-04, TC-08, TC-11 | `COVERED` | — |
| AC-04 | TC-05, TC-06 | `COVERED` | — |
| AC-05 | TC-13, TC-14…TC-23 | `COVERED` | — |
| AC-06 | TC-25, TC-26 | `PARTIAL` | NB-06: единица измерения и точка применения лимита 254 не определены; покрыты ASCII-значения |
| AC-07 | TC-17 | `COVERED` | — |
| AC-08 | TC-19, TC-20, TC-21, TC-22 | `COVERED` | позиции дефисов и подряд идущие точки не входят в AC-08 (NB-05) |
| AC-09 | TC-29, TC-30, TC-31, TC-32, TC-33 | `COVERED` | — |
| AC-10 | TC-28, TC-35 | `COVERED` | — |
| AC-11 | TC-39, TC-24, TC-27 | `COVERED` | — |
| AC-12 | TC-27 | `COVERED` | — |
| AC-13 | TC-38 | `COVERED` | — |
| AC-14 | TC-40, TC-41 | `COVERED` | место серверного сообщения не проверяется (BLK-03 п. 7) |
| AC-15 | TC-10, TC-11, TC-12 | `COVERED` | — |
| AC-16 | TC-44 | `PARTIAL` | срок 30 дней и отсутствие продления не проверяются (NB-14, L-02); TC-49 `BLOCKED` |
| AC-17 | TC-48 (`BLOCKED`) | `NOT_COVERABLE` | NB-14 + L-02 |
| AC-18 | TC-47 | `COVERED` | — |
| AC-19 | TC-45, TC-46 | `COVERED` | — |
| AC-20 | TC-04, TC-05, TC-06, TC-09, TC-14, TC-31, TC-34, TC-43 и все кейсы с проверкой отсутствия запроса | `COVERED` | — |
| AC-21 | TC-06, TC-07 | `COVERED` | — |
| AC-22 | TC-33 | `COVERED` | — |
| AC-23 | TC-36, TC-37 | `COVERED` | — |
| AC-24 | TC-09, TC-34 | `COVERED` | — |
| AC-25 | TC-42 | `COVERED` | — |

### 7.2. Позитивные и негативные потоки

| Поток | Тест-кейсы | Статус |
|---|---|---|
| PF-01 | TC-39 | `COVERED` |
| PF-02 | TC-27 | `COVERED` |
| PF-03 | TC-24 | `COVERED` |
| PF-04 | TC-44, TC-47 | `PARTIAL` (срок 30 дней — NB-14) |
| PF-05 | TC-46 | `COVERED` |
| PF-06 | TC-02, TC-03 | `COVERED` |
| PF-07 | TC-11, TC-12 | `COVERED` |
| PF-08 | TC-07 | `COVERED` |
| PF-09 | TC-06 | `COVERED` |
| NF-01 | TC-04 | `COVERED` |
| NF-02 | TC-05 | `COVERED` |
| NF-03 | TC-14…TC-23 | `COVERED` (кроме позиций точек/дефисов — NB-05) |
| NF-04 | TC-26 | `PARTIAL` (NB-06) |
| NF-05 | TC-31, TC-32 | `COVERED` |
| NF-06 | TC-35 | `COVERED` |
| NF-07 | TC-40, TC-43 | `COVERED` |
| NF-08 | TC-41 | `COVERED` |
| NF-09 | TC-38 | `COVERED` |
| NF-10 | TC-48 (`BLOCKED`) | `NOT_COVERABLE` (NB-14) |
| NF-11 | TC-45 | `COVERED` |
| NF-12 | TC-09 | `COVERED` |
| NF-13 | TC-36, TC-37 | `COVERED` |
| NF-14 | TC-33 | `COVERED` |
| NF-15 | TC-42 | `COVERED` |
| NF-16 | TC-34 | `COVERED` |
| NF-17 | TC-10 | `COVERED` |

### 7.3. Правила валидации и границы

| ID | Тест-кейсы | Статус |
|---|---|---|
| VR-01 | TC-04, TC-05, TC-06, TC-07, TC-08 | `COVERED` |
| VR-02 | TC-24 | `COVERED` |
| VR-03 | TC-13…TC-23 | `COVERED` |
| VR-04 | TC-26 | `PARTIAL` (NB-06) |
| VR-05 | TC-29…TC-34 | `COVERED` |
| VR-06 | TC-28, TC-35, TC-36, TC-37 | `COVERED` |
| VR-07 | TC-27, TC-38 | `COVERED` |
| VR-08 | TC-04, TC-09, TC-34 | `COVERED` |
| VR-09 | TC-10, TC-11, TC-12 | `COVERED` |
| VR-10 | TC-42 | `COVERED` |
| B-01 | TC-25, TC-26 | `PARTIAL` (NB-06) |
| B-02 | TC-29, TC-30, TC-31, TC-32 | `COVERED` |
| B-03 | TC-19, TC-20 | `COVERED` |
| B-04 | TC-21, TC-22 | `COVERED` |
| B-05 | TC-16, TC-36, TC-37 | `COVERED` |
| B-06 | TC-04, TC-06, TC-07 | `COVERED` |
| B-07 | TC-44, TC-48 (`BLOCKED`) | `NOT_COVERABLE` (NB-14, L-02) |
| B-08 | TC-27, TC-38 | `COVERED` |
| B-09 | TC-38 | `COVERED` |
| B-10 | TC-33 | `COVERED` |
| B-11 | TC-42, TC-24 | `COVERED` |

## 8. Risk Coverage

| Риск / находка | Покрывающие тест-кейсы | Что не покрыто и почему |
|---|---|---|
| NB-07 — совпадение текстов клиентской ошибки и ошибки аутентификации | TC-43 (`RISK_BASED`), TC-14, TC-40 | различение причин по расположению сообщения невозможно — размещение серверного сообщения исключено из области требований (BLK-03 п. 7) |
| NB-08 — сохранение пароля в поле после неуспешной авторизации | TC-41, TC-42 | маскирование пароля не проверяется: требований к типу поля и маскированию нет (NB-03) |
| NB-09 — отсутствие ограничения срока сессии без Remember me | TC-45 | проверяемое условие истечения сессии без Remember me отсутствует; проверяется только завершение при закрытии браузера |
| NB-13 — иные способы завершения сохранённой авторизации | TC-47 | проверен только второй профиль браузера; очистка хранилища, приватное окно, смена пароля не проверяются |
| NB-14 — исчисление 30-дневного срока | — | TC-48, TC-49 `BLOCKED`; управление временем недоступно (L-02) |
| NB-01 — жизненный цикл серверного сообщения | TC-40, TC-41 (фиксируют факт сообщения) | снятие/замена сообщения не проверяются: поведение не определено |
| NB-11 — состояние кнопки Login во время запроса | — | требования отсутствуют |
| NB-12 — поведение защищённых страниц без авторизации | TC-45, TC-47, TC-46 (наблюдение «авторизован / требуется авторизация») | контроль доступа вне формы не проверяется |
| BLK-01 — трактовка whitespace-пароля (закрыт решением) | TC-06, TC-07, TC-33, TC-36, TC-37 | — |
| BLK-02 — приоритет сообщения о длине пароля (закрыт решением) | TC-09, TC-31…TC-34 | — |
| BLK-03 — место и количество клиентских сообщений (закрыт решением) | TC-04, TC-09, TC-43, TC-34 | — |
| BLK-04 — момент повторной проверки (закрыт решением) | TC-10, TC-11, TC-12 | события, не названные в решении (RES-02), не покрыты |
| BLK-05 — состояние полей после отказа (закрыт решением) | TC-42, TC-40, TC-41 | — |

## 9. Duplicate Check Results

### 9.1. Проверка структуры Test Suites

Проверка выполнена через Qase READ (`qase_project_context`, `qql_search`) до создания сущностей: в проекте AUTH на момент проверки `counts.suites = 0`, `counts.cases = 0`. Разделов с совпадающим заголовком и родителем не обнаружено.

| `suite_ref` | Проверенный заголовок | Найденный `qase_suite_id` | Решение | Обоснование |
|---|---|---|---|---|
| SUITE-01 | Состав формы и первоначальное состояние | Не обнаружено | `CREATE` | раздел отсутствует |
| SUITE-02 | Обязательность полей и клиентские сообщения | Не обнаружено | `CREATE` | раздел отсутствует |
| SUITE-03 | Валидация формата Email | Не обнаружено | `CREATE` | раздел отсутствует |
| SUITE-04 | Валидация формата и длины пароля | Не обнаружено | `CREATE` | раздел отсутствует |
| SUITE-05 | Успешная авторизация | Не обнаружено | `CREATE` | раздел отсутствует |
| SUITE-06 | Неуспешная авторизация | Не обнаружено | `CREATE` | раздел отсутствует |
| SUITE-07 | Сохранение авторизации (Remember me) | Не обнаружено | `CREATE` | раздел отсутствует |

### 9.2. Проверка тест-кейсов

Поиск выполнялся по проекту AUTH с расширением на всё рабочее пространство (QQL, фильтры по `login`, `вход`, `авторизац`, `email`, `пароль`, `password`, `remember`). В проекте AUTH совпадений нет ни для одного тест-кейса. В другом проекте рабочего пространства (код `SHARELANE`, подтверждено агрегацией `GROUP BY project`) найдено 17 тест-кейсов формы регистрации (Sign Up, есть поле Confirm Password) — они относятся к другой функциональности и другому проекту, поэтому классифицированы как `RELATED`, а не дубликаты.

| `test_ref` | Класс совпадения | Найденный `qase_case_id` | Решение | Обоснование |
|---|---|---|---|---|
| TC-01…TC-03 | `NOT_FOUND` | — | создаётся | в AUTH совпадений нет |
| TC-04 | `RELATED` | 103, 106 (проект SHARELANE) | создаётся | другой проект и другая функциональность (регистрация); проверяется обязательность двух полей формы входа, а не формы регистрации |
| TC-05 | `NOT_FOUND` | — | создаётся | правило «Email из пробелов» в существующих кейсах не проверяется |
| TC-06…TC-12 | `NOT_FOUND` | — | создаётся | в AUTH совпадений нет |
| TC-13 | `RELATED` | 32, 99 (SHARELANE) | создаётся | существующий кейс проверяет заполнение поля валидным значением в форме регистрации, без правил BR-05 |
| TC-14 | `RELATED` | 100, 104 (SHARELANE) | создаётся | иной проект и функциональность; проверяется конкретное правило структуры Email |
| TC-15…TC-27 | `NOT_FOUND` | — | создаётся | в AUTH совпадений нет |
| TC-28 | `RELATED` | 105, 101 (SHARELANE) | создаётся | другой проект; существующий кейс проверяет валидность пароля регистрации (≤ 4 символа), что противоречит REQ-23 |
| TC-29…TC-34 | `NOT_FOUND` | — | создаётся | границы длины пароля 8/64/7/65 и их сообщения не покрыты |
| TC-35 | `RELATED` | 27, 107 (SHARELANE) | создаётся | иной проект и функциональность; невалидность пароля в существующих кейсах не детализирована |
| TC-36…TC-38 | `NOT_FOUND` | — | создаётся | в AUTH совпадений нет |
| TC-39 | `RELATED` | 34 (SHARELANE) | создаётся | существующий кейс описывает другой продукт (топ-бар, корзина, Logout) и не проверяет переход на `/dashboard` |
| TC-40…TC-47 | `NOT_FOUND` | — | создаётся | в AUTH совпадений нет |

Замечание по расхождению: тест-кейс 101 проекта SHARELANE содержит условие «пароль должен быть ≤ 4 символов», что противоречит REQ-23 Artifact v2 (8–64 символа). Расхождение относится к другому проекту и другой функциональности, существующие сущности не изменялись; передаётся Orchestrator как сведения (раздел 12, X-02).

## 10. Creation Summary

### 10.1. Сводка по разделам

| `creation_status` | Количество |
|---|---|
| `CREATED` | 7 |
| `REUSE` | 0 |
| `FAILED` / `UNKNOWN` | 0 |

Созданные разделы: SUITE-01 → 19, SUITE-02 → 20, SUITE-03 → 21, SUITE-04 → 22, SUITE-05 → 23, SUITE-06 → 24, SUITE-07 → 25.

### 10.2. Сводка по тест-кейсам

| `creation_status` | Количество |
|---|---|
| `CREATED` | 47 |
| `DUPLICATE` | 0 |
| `SKIPPED` (`BLOCKED`) | 2 (TC-48, TC-49) |
| `FAILED` / `UNKNOWN` | 0 |

Таблица подтверждённых CREATE (ответ Tool + проверка READ; URL: `https://app.qase.io/case/AUTH/<id>`):

| `test_ref` | `qase_case_id` | Название | Статус создания |
|---|---|---|---|
| TC-01 | 126 | Форма авторизации содержит поля Email, Password, чекбокс Remember me и кнопку Login | `CREATED` |
| TC-02 | 127 | При первоначальном открытии формы сообщения об ошибках отсутствуют | `CREATED` |
| TC-03 | 128 | Чекбокс Remember me при первоначальном открытии снят | `CREATED` |
| TC-04 | 129 | Login при пустых Email и Password: сообщение «Это поле обязательно» у обоих полей | `CREATED` |
| TC-05 | 130 | Email из одних пробелов: сообщение «Это поле обязательно» у поля Email | `CREATED` |
| TC-06 | 131 | Пустой Email и пароль из 8 символов пробела: сообщение только у поля Email | `CREATED` |
| TC-07 | 132 | Пароль из 8 символов пробела при валидном Email: сообщение обязательности не отображается, запрос отправляется | `CREATED` |
| TC-08 | 133 | Проверка формата выполняется только для заполненных полей | `CREATED` |
| TC-09 | 134 | Одновременное нарушение в обоих полях: ровно два клиентских сообщения | `CREATED` |
| TC-10 | 135 | До первой попытки входа ввод значения не вызывает клиентских сообщений | `CREATED` |
| TC-11 | 136 | После первой попытки входа ввод в поле перепроверяет оба поля без повторного нажатия Login | `CREATED` |
| TC-12 | 137 | После первой попытки входа вставка значения из буфера запускает повторную проверку | `CREATED` |
| TC-13 | 138 | Валидный Email проходит клиентскую проверку: сообщений нет, запрос отправляется | `CREATED` |
| TC-14 | 139 | Email без символа @ отклоняется | `CREATED` |
| TC-15 | 140 | Email без домена отклоняется | `CREATED` |
| TC-16 | 141 | Email с пробелом внутри отклоняется | `CREATED` |
| TC-17 | 142 | Email с кириллическими символами отклоняется | `CREATED` |
| TC-18 | 143 | Недопустимый символ в имени пользователя Email отклоняется | `CREATED` |
| TC-19 | 144 | Домен Email из одной части отклоняется | `CREATED` |
| TC-20 | 145 | Домен Email с поддоменом принимается | `CREATED` |
| TC-21 | 146 | Точка первым символом домена Email отклоняется | `CREATED` |
| TC-22 | 147 | Точка последним символом домена Email отклоняется | `CREATED` |
| TC-23 | 148 | Недопустимый символ в домене Email отклоняется | `CREATED` |
| TC-24 | 149 | Пробелы в начале и конце Email удаляются до проверки: авторизация выполняется | `CREATED` |
| TC-25 | 150 | Email длиной 254 символа проходит проверку длины | `CREATED` |
| TC-26 | 151 | Email длиной 255 символов отклоняется | `CREATED` |
| TC-27 | 152 | Email в ином регистре при правильном пароле: авторизация выполняется | `CREATED` |
| TC-28 | 153 | Пароль допустимого формата проходит клиентскую проверку | `CREATED` |
| TC-29 | 154 | Пароль длиной 8 символов проходит проверку длины | `CREATED` |
| TC-30 | 155 | Пароль длиной 64 символа проходит проверку длины | `CREATED` |
| TC-31 | 156 | Пароль длиной 7 символов отклоняется по длине | `CREATED` |
| TC-32 | 157 | Пароль длиной 65 символов отклоняется по длине | `CREATED` |
| TC-33 | 158 | Пароль из 7 символов пробела отклоняется по длине | `CREATED` |
| TC-34 | 159 | Неверная длина пароля при недопустимом символе: отображается только сообщение о длине | `CREATED` |
| TC-35 | 160 | Символ вне разрешённого набора в пароле отклоняется | `CREATED` |
| TC-36 | 161 | Символ табуляции в пароле отклоняется | `CREATED` |
| TC-37 | 162 | Неразрывный пробел в пароле отклоняется | `CREATED` |
| TC-38 | 163 | Пароль, отличающийся от правильного только регистром, отклоняется | `CREATED` |
| TC-39 | 164 | Успешная авторизация зарегистрированного пользователя при снятом Remember me | `CREATED` |
| TC-40 | 165 | Незарегистрированный Email при валидном формате: сообщение, отсутствие авторизации, сохранение значений | `CREATED` |
| TC-41 | 166 | Зарегистрированный Email и неправильный пароль: сообщение, отсутствие авторизации, сохранение значений | `CREATED` |
| TC-42 | 167 | После неуспешной авторизации Email нормализован, значение пароля не обрезается | `CREATED` |
| TC-43 | 168 | Совпадающий текст клиентской и серверной ошибки: различие фиксируется по наличию сетевого запроса | `CREATED` |
| TC-44 | 169 | Remember me установлен: авторизация сохраняется после перезапуска браузера | `CREATED` |
| TC-45 | 170 | Remember me снят: после закрытия браузера сессия завершена | `CREATED` |
| TC-46 | 171 | Remember me снят: закрытие вкладки, новая вкладка и переходы между страницами не завершают сессию | `CREATED` |
| TC-47 | 172 | Remember me установлен: сохранённая авторизация не действует в другом профиле браузера | `CREATED` |

### 10.3. Дубликаты и пропущенные тест-кейсы

- `DUPLICATE`: Не обнаружено — ни один тест-кейс не пропущен как дубликат в проекте AUTH.
- `SKIPPED`: TC-48 (истечение 30 дней: NB-14, L-02), TC-49 (отсутствие продления: NB-14, L-02).

### 10.4. Ошибки и неоднозначные операции

| ID | Операция | Описание | Результат |
|---|---|---|---|
| E-01 | Qase CREATE (test cases, SUITE-03) | Первая попытка пакетного создания 15 тест-кейсов отклонена валидацией: значение `type = boundary` не входит в справочник типов Qase проекта AUTH. Пакет валидируется целиком, поэтому ни одна сущность не создана | ошибка устранена повторным запросом с `type = functional`; `test_type = BOUNDARY` сохранён тегом; подтверждено, что дубликатов не появилось (итоговое количество кейсов 47) |
| E-02 | Qase READ (проверка создания) | Параллельные `qase_get` по 47 кейсам вызвали ошибку rate limit | проверка повторена последовательными вызовами; все 47 кейсов подтверждены |
| E-03 | Qase READ (QQL) | `qql_search` по проекту AUTH на момент проверки вернул 28 из 47 созданных кейсов (запаздывание индекса); агрегация `GROUP BY suite_id` недоступна (поле не поддерживается в SELECT) | верификация выполнена через `qase_project_context` (47 кейсов, 7 разделов) и персональные `qase_get` по всем ID |

## 11. Проверка создания (Creation Verification)

| Проверка | Результат |
|---|---|
| создание каждого раздела подтверждено ответом Tool | подтверждено: 7 ответов `qase_suite_upsert` с ID 19…25 |
| `qase_suite_id` сохранён и сопоставлен с `suite_ref` | подтверждено (раздел 5) |
| каждый тест-кейс находится в разделе, соответствующем его `suite_ref` | подтверждено: 47 персональных `qase_get`, сверка `suite_id`; распределение 3/9/15/11/1/4/4 совпадает с планом |
| создание каждого тест-кейса подтверждено ответом Tool | подтверждено: `qase_case_bulk_create` вернул 47 ID в порядке подачи |
| `qase_case_id` сохранён и сопоставлен с `test_ref` | подтверждено (раздел 10.2) |
| тест-кейсы, не созданные как дубликаты, имеют `duplicate_reference` | не применимо — дубликатов нет |
| пропущенные тест-кейсы имеют `skip_reason` | подтверждено: TC-48, TC-49 (раздел 6) |
| ошибки и частичные результаты зафиксированы | подтверждено (раздел 10.4) |

**Итог проверки создания: `CONFIRMED`** — все запланированные `READY`-сущности созданы и подтверждены; неприменимые пункты отмечены.

## 12. Сознательно не созданные проверки

| ID | Не созданная проверка | Связанные требования / находки | Причина |
|---|---|---|---|
| X-01 | Жизненный цикл сообщения о неуспешной авторизации: когда снимается, заменяется ли клиентским сообщением | REQ-31, REQ-10; NB-01, DEP-06 | поведение не определено (MISSING_INFORMATION); ожидаемый результат не выводим |
| X-02 | Обработка серверных и сетевых сбоев (5xx, таймаут, недоступность сервиса) | REQ-11, REQ-22, REQ-29, REQ-31; NB-02, DEP-05 | требований и серверного контракта нет |
| X-03 | Нефункциональные проверки: маскирование пароля, ограничение попыток входа/антибрутфорс, транспортная защита, a11y, поддерживаемые браузеры и разрешения, локализация | форма в целом; NB-03 | нефункциональные требования отсутствуют |
| X-04 | Позиции точек и дефисов в начале/конце имени пользователя и меток домена; подряд идущие точки | REQ-15, REQ-16, REQ-18; NB-05 | ожидаемые результаты неопределимы (AMBIGUITY) |
| X-05 | Единица измерения лимита Email (символы/байты) и точка применения лимита относительно обрезки пробелов | REQ-20, REQ-12; NB-06 | аспект не определён; границы 254/255 покрыты только для ASCII-значений (TC-25, TC-26) |
| X-06 | Границы 29/30/31 день срока Remember me | REQ-32, REQ-33, REQ-35; NB-14, B-07 | нет согласованной трактовки срока и управления временем (TC-48, TC-49 `BLOCKED`) |
| X-07 | Иные способы завершения сохранённой авторизации (очистка хранилища, приватное окно, смена пароля, выход на другом устройстве) | REQ-34; NB-13 | не определено, что завершает сохранённую авторизацию |
| X-08 | Размещение сообщения о серверной ошибке аутентификации | REQ-31; BLK-03 п. 7; RES-03 | аспект исключён из области требований решением владельца; не является поведением по умолчанию или предположением |
| X-09 | Автозаполнение и программное изменение значения поля как триггер повторной проверки; потеря фокуса без изменения значения | REQ-10; RES-02 | поведение не регламентировано решением по BLK-04 |
| X-10 | Поведение при обращении к защищённым страницам без авторизации и при истечении сессии без Remember me во время работы | REQ-30, REQ-35, REQ-37; NB-12, DEP-03, NAS-06 | требования отсутствуют; в TC-45…TC-47 фиксируется только наблюдаемое «авторизован / требуется авторизация» |
| X-11 | Состояние кнопки Login во время выполнения запроса, индикация загрузки, защита от повторной отправки | REQ-04, REQ-07, REQ-11; NB-11 | требования отсутствуют |
| X-12 | Ограничение срока/неактивности сессии без Remember me | REQ-36, REQ-37; NB-09 | проверяемое условие не задано (риск зафиксирован в разделе 8) |
| X-13 | Проверки за пределами формы: восстановление пароля, регистрация, иные связанные страницы | NAS-01, NAS-02 | вне области Artifact; расширение Scope запрещено |
| X-14 | Изменение или удаление существующих сущностей Qase | — | запрещено индивидуальной инструкцией (только READ и CREATE) |

## 13. Маппинг модели в поля Qase

Проект AUTH не содержит custom fields и проектных правил маппинга, поэтому применён явный маппинг без изменения смысла значений:

| Поле модели | Поле Qase | Значения |
|---|---|---|
| `priority` (`HIGH`/`MEDIUM`/`LOW`) | `priority` | `high` (26 кейсов), `medium` (21 кейс); `LOW` не использован — ниже обоснованных MEDIUM проверок нет |
| `test_type` | `tags` | значение передаётся как есть: `POSITIVE`, `NEGATIVE`, `BOUNDARY`, `VALIDATION`, `RISK_BASED` (теги `positive`/`negative` нормализованы Qase в нижний регистр при сохранении) |
| `test_type` `POSITIVE`/`NEGATIVE` | `behavior` | `positive` / `negative` — совпадает с назначением поля Qase |
| — | `type` | `functional` для всех кейсов: справочник Qase не содержит значений `BOUNDARY`/`VALIDATION`/`RISK_BASED`, а `type` не является носителем `test_type` модели |
| — | `automation` | `manual` — автотесты вне Scope |
| `source_requirements` | `tags` + `description` | теги AC/REQ, полная трассировка в `description` |
| `preconditions`, `steps`, `expected_result` | одноимённые поля | ожидаемый результат указан у каждого шага и в завершающем шаге проверки |

Распределение `test_type`: `NEGATIVE` 24, `POSITIVE` 11, `BOUNDARY` 8, `VALIDATION` 3, `RISK_BASED` 1 (всего 47). Распределение `priority`: `HIGH` 26, `MEDIUM` 21, `LOW` 0 (всего 47; `LOW` не назначался, так как все проверки области следуют из подтверждённых правил и не являются второстепенными).

## 14. Ограничения покрытия для Final Quality Gate

1. **NB-14 / REQ-33, REQ-35, AC-16, AC-17, B-07** — срок Remember me (30 дней, отсутствие продления, истечение) не покрыт исполняемыми проверками: TC-48, TC-49 `BLOCKED`, требуется согласованная трактовка срока и управление системным временем.
2. **NB-06 / REQ-20, AC-06, B-01, VR-04** — покрыты только ASCII-значения на границе 254/255; единица измерения и точка применения лимита не проверены.
3. **NB-05 / REQ-15, REQ-16, REQ-18** — позиции точек и дефисов, подряд идущие точки не проверены.
4. **NB-02, NB-03, NB-04 (закрыта), NB-11, NB-13** — серверные/сетевые сбои, NFR (маскирование пароля, антибрутфорс, a11y, кроссбраузерность, локализация), состояние кнопки Login, способы завершения сохранённой авторизации не проверены.
5. **NB-01, RES-02, RES-03** — жизненный цикл серверного сообщения, автозаполнение/программное изменение значения и размещение серверного сообщения не проверены.
6. **NB-12 / NAS-06** — контроль доступа вне формы не проверен; в проверках сессии фиксируется только «авторизован / требуется авторизация».
7. **DEP-01, NAS-04** — тестовые данные зарегистрированных пользователей в требованиях не определены; предусловия ссылаются на тестовые данные среды. Без подготовленных учётных записей кейсы TC-24, TC-27, TC-39, TC-42…TC-47 не выполнимы.
8. **Окружение** — часть кейсов требует наблюдения сетевых запросов (DevTools/Network), перезапуска браузера, двух профилей браузера и подготовки длинных значений (64, 254, 255 символа).
9. **Источник текстов сообщений** — тексты подтверждены страницей требований и решениями владельца (`human decision`), справочник сообщений и правила локализации отсутствуют (DEP-04). При изменении формулировок сообщений тест-кейсы требуют пересмотра.
10. **Расхождение с другим проектом Qase (сведения из раздела 9.2)** — тест-кейс 101 проекта SHARELANE содержит условие «пароль ≤ 4 символов», что противоречит REQ-23 Artifact v2. Существующая сущность не изменялась; расхождение передаётся Orchestrator.
11. **NAS-01…NAS-03, NAS-07** — возможные пропуски требований на дочерних страницах и в связанных документах; тестовая модель ограничена проанализированной страницей 2228225.
