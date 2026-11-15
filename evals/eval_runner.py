import json
from pathlib import Path

from evaluator import evaluate_response
from opencode_cli import start_opencode


# =============================================================
# PATHS
# =============================================================

project_path = Path(__file__).resolve().parent.parent

dataset_path = (
    Path(__file__).parent
    / "dataset"
    / "golden_dataset.json"
)


# =============================================================
# QUALITY GATE THRESHOLDS
# =============================================================

# Минимально допустимый процент успешно пройденных Eval Cases.
MIN_PASS_RATE = 95.0

# Минимально допустимый процент выполненных Expected Properties.
MIN_EXPECTED_PROPERTIES_PASS_RATE = 95.0

# Максимально допустимый процент нарушенных Forbidden Behavior.
MAX_FORBIDDEN_BEHAVIOR_VIOLATION_RATE = 0.0

# Допустимое количество технических ошибок.
MAX_ERRORS = 0


# =============================================================
# ЗАГРУЗКА GOLDEN DATASET
# =============================================================

with open(
    dataset_path,
    "r",
    encoding="utf-8"
) as file:

    eval_cases = json.load(file)


eval_results = []


# =============================================================
# PROMPT ДЛЯ QA AGENT
# =============================================================

# Каждый Eval Case содержит собственный eval_prompt —
# формулировку задачи, которая передаётся QA Agent.
#
# В eval_prompt допускается плейсхолдер {page_id}:
# Runner подставляет вместо него значение
# eval_case["input"]["page_id"].
#
# Expected Properties и Forbidden Behavior
# агенту не передаются.


def build_agent_prompt(eval_case):

    eval_input = eval_case["input"]

    source = eval_input.get("source")


    if source != "confluence":

        raise RuntimeError(
            f"Eval Case {eval_case['id']} использует "
            f"неподдерживаемый источник: {source}"
        )


    eval_prompt = eval_case.get("eval_prompt")


    if not isinstance(eval_prompt, str) or not eval_prompt.strip():

        raise RuntimeError(
            f"Eval Case {eval_case['id']} не содержит "
            f"непустое строковое поле eval_prompt"
        )


    page_id = eval_input.get("page_id")


    if "{page_id}" in eval_prompt:

        if page_id is None:

            raise RuntimeError(
                f"Eval Case {eval_case['id']} использует "
                f"плейсхолдер {{page_id}}, "
                f"но page_id не задан"
            )


        eval_prompt = eval_prompt.replace(
            "{page_id}",
            str(page_id)
        )


    return eval_prompt


# =============================================================
# ГРУППИРОВКА EVAL CASES ПО PROMPT
# =============================================================

# Один запуск QA Agent выполняется на один уникальный Prompt.
# Eval Cases с идентичным Prompt переиспользуют
# один и тот же фактический ответ агента.

cases_by_prompt = {}


for eval_case in eval_cases:

    agent_prompt = build_agent_prompt(
        eval_case
    )


    if agent_prompt not in cases_by_prompt:

        cases_by_prompt[agent_prompt] = []


    cases_by_prompt[agent_prompt].append(
        eval_case
    )


# =============================================================
# ЗАПУСК QA AGENT
# =============================================================

for agent_prompt, prompt_eval_cases in cases_by_prompt.items():

    print()
    print("=" * 80)
    print("ЗАПУСК QA AGENT")
    print("=" * 80)

    print()
    print("Источник требований: Confluence")

    print(
        "Eval Cases в этом запуске: "
        + ", ".join(
            eval_case["id"]
            for eval_case in prompt_eval_cases
        )
    )

    print(
        f"Количество Eval Cases для этого Prompt: "
        f"{len(prompt_eval_cases)}"
    )

    print()


    # =========================================================
    # PROMPT ДЛЯ QA AGENT
    # =========================================================

    # Runner передаёт агенту только исходную задачу.
    #
    # Expected Properties и Forbidden Behavior
    # агенту не передаются.

    print("PROMPT ДЛЯ QA AGENT:")

    print(agent_prompt)

    print()


    # =========================================================
    # ЗАПУСК OPENCODE
    # =========================================================

    process = start_opencode(
        agent_prompt,
        project_path
    )


    text_parts = []


    print("QA Agent запущен...")


    # =========================================================
    # ЧТЕНИЕ JSON EVENTS
    # =========================================================

    if process.stdout:

        for line in process.stdout:

            line = line.strip()


            if not line:
                continue


            try:

                event = json.loads(line)

                event_type = event.get("type")


                print(
                    "AGENT EVENT:",
                    event_type,
                    flush=True
                )


                if event_type == "text":

                    part = event.get(
                        "part",
                        {}
                    )

                    text = part.get(
                        "text"
                    )


                    if text:

                        text_parts.append(
                            text
                        )


            except json.JSONDecodeError:

                print(
                    "Не удалось разобрать "
                    "событие OpenCode",
                    flush=True
                )


    # =========================================================
    # ЗАВЕРШЕНИЕ QA AGENT
    # =========================================================

    return_code = process.wait()


    agent_response = "\n".join(
        text_parts
    ).strip()


    print()

    print(
        "QA AGENT RETURN CODE:",
        return_code
    )


    # =========================================================
    # ОБРАБОТКА ОШИБКИ QA AGENT
    # =========================================================

    if return_code != 0:

        print(
            "QA Agent завершился с ошибкой."
        )


        stderr = ""


        if process.stderr:

            stderr = process.stderr.read()


        if stderr:

            print(stderr)


        for eval_case in prompt_eval_cases:

            eval_results.append(
                {
                    "id": eval_case["id"],
                    "name": eval_case["name"],
                    "prompt": agent_prompt,
                    "status": "ERROR",
                    "score": 0.0,
                    "expected_properties": [],
                    "forbidden_behavior": []
                }
            )


        continue


    # =========================================================
    # ПРОВЕРКА ПУСТОГО ОТВЕТА
    # =========================================================

    if not agent_response:

        print(
            "QA Agent не вернул "
            "текстовый ответ."
        )


        for eval_case in prompt_eval_cases:

            eval_results.append(
                {
                    "id": eval_case["id"],
                    "name": eval_case["name"],
                    "prompt": agent_prompt,
                    "status": "ERROR",
                    "score": 0.0,
                    "expected_properties": [],
                    "forbidden_behavior": []
                }
            )


        continue


    # =========================================================
    # ВЫВОД ОТВЕТА QA AGENT
    # =========================================================

    print()
    print("=" * 80)
    print("ОТВЕТ QA AGENT")
    print("=" * 80)

    print(agent_response)

    print("=" * 80)


    # =========================================================
    # EVALUATION
    # =========================================================

    # Один фактический Agent Response
    # проверяется всеми Eval Cases этого Prompt.

    for eval_case in prompt_eval_cases:

        print()
        print()

        print("-" * 80)

        print(
            f"Evaluation: "
            f"{eval_case['id']}"
        )

        print(
            f"Название: "
            f"{eval_case['name']}"
        )

        print("-" * 80)

        print()
        print("Запускаем Evaluator...")


        try:

            evaluation_result = evaluate_response(
                eval_case,
                agent_response
            )


            print()
            print("=" * 80)
            print("РЕЗУЛЬТАТ EVALUATION")
            print("=" * 80)


            print(
                json.dumps(
                    evaluation_result,
                    ensure_ascii=False,
                    indent=2
                )
            )


            print("=" * 80)


            status = evaluation_result[
                "status"
            ]

            score = evaluation_result[
                "score"
            ]


            eval_results.append(
                {
                    "id": eval_case["id"],
                    "name": eval_case["name"],
                    "prompt": agent_prompt,
                    "status": status,
                    "score": score,

                    "expected_properties":
                        evaluation_result[
                            "expected_properties"
                        ],

                    "forbidden_behavior":
                        evaluation_result[
                            "forbidden_behavior"
                        ]
                }
            )


            print()

            print(
                "EVAL CASE:",
                eval_case["id"]
            )

            print(
                "STATUS:",
                status
            )

            print(
                "SCORE:",
                score
            )


        except Exception as error:

            print()
            print("Ошибка Evaluator:")
            print(error)


            eval_results.append(
                {
                    "id": eval_case["id"],
                    "name": eval_case["name"],
                    "prompt": agent_prompt,
                    "status": "ERROR",
                    "score": 0.0,
                    "expected_properties": [],
                    "forbidden_behavior": []
                }
            )


# =============================================================
# EVALUATION SUMMARY
# =============================================================

print()
print()

print("=" * 80)
print("EVALUATION SUMMARY")
print("=" * 80)


# =============================================================
# BASIC METRICS
# =============================================================

total = len(eval_results)


passed = sum(
    1
    for result in eval_results
    if result["status"] == "PASS"
)


failed = sum(
    1
    for result in eval_results
    if result["status"] == "FAIL"
)


errors = sum(
    1
    for result in eval_results
    if result["status"] == "ERROR"
)


# =============================================================
# PASS RATE
# =============================================================

if total > 0:

    pass_rate = (
        passed / total
    ) * 100

else:

    pass_rate = 0.0


# =============================================================
# AVERAGE SCORE
# =============================================================

if total > 0:

    average_score = (
        sum(
            result["score"]
            for result in eval_results
        )
        / total
    )

else:

    average_score = 0.0


# =============================================================
# EXPECTED PROPERTIES PASS RATE
# =============================================================

total_expected_properties = 0

passed_expected_properties = 0


for result in eval_results:

    expected_properties = result.get(
        "expected_properties",
        []
    )


    for expected_property in expected_properties:

        total_expected_properties += 1


        if expected_property.get(
            "passed"
        ) is True:

            passed_expected_properties += 1


if total_expected_properties > 0:

    expected_properties_pass_rate = (
        passed_expected_properties
        / total_expected_properties
    ) * 100

else:

    expected_properties_pass_rate = 0.0


# =============================================================
# FORBIDDEN BEHAVIOR VIOLATION RATE
# =============================================================

total_forbidden_behaviors = 0

violated_forbidden_behaviors = 0


for result in eval_results:

    forbidden_behaviors = result.get(
        "forbidden_behavior",
        []
    )


    for forbidden_behavior in forbidden_behaviors:

        total_forbidden_behaviors += 1


        if forbidden_behavior.get(
            "violated"
        ) is True:

            violated_forbidden_behaviors += 1


if total_forbidden_behaviors > 0:

    forbidden_behavior_violation_rate = (
        violated_forbidden_behaviors
        / total_forbidden_behaviors
    ) * 100

else:

    forbidden_behavior_violation_rate = 0.0


# =============================================================
# BASIC METRICS OUTPUT
# =============================================================

print()

print(
    f"Total:         {total}"
)

print(
    f"Passed:        {passed}"
)

print(
    f"Failed:        {failed}"
)

print(
    f"Errors:        {errors}"
)

print(
    f"Pass Rate:     "
    f"{pass_rate:.1f}%"
)

print(
    f"Average Score: "
    f"{average_score:.2f}"
)


# =============================================================
# QUALITY METRICS OUTPUT
# =============================================================

print()

print("QUALITY METRICS")

print("-" * 80)


print(
    f"Expected Properties:                 "
    f"{passed_expected_properties}/"
    f"{total_expected_properties}"
)


print(
    f"Expected Properties Pass Rate:       "
    f"{expected_properties_pass_rate:.1f}%"
)


print(
    f"Forbidden Behaviors Violated:        "
    f"{violated_forbidden_behaviors}/"
    f"{total_forbidden_behaviors}"
)


print(
    f"Forbidden Behavior Violation Rate:   "
    f"{forbidden_behavior_violation_rate:.1f}%"
)


# =============================================================
# РЕЗУЛЬТАТЫ ПО КАЖДОМУ EVAL CASE
# =============================================================

print()

print("-" * 80)


for result in eval_results:

    print(
        f"{result['id']:<10}"
        f"{result['status']:<10}"
        f"Score: {result['score']}"
    )


print("-" * 80)


# =============================================================
# QUALITY GATE
# =============================================================

# Теперь решение о допуске принимается
# на основании измеримых метрик.


# -------------------------------------------------------------
# ПРОВЕРКА PASS RATE
# -------------------------------------------------------------

pass_rate_gate = (
    pass_rate
    >= MIN_PASS_RATE
)


# -------------------------------------------------------------
# ПРОВЕРКА EXPECTED PROPERTIES
# -------------------------------------------------------------

expected_properties_gate = (
    expected_properties_pass_rate
    >= MIN_EXPECTED_PROPERTIES_PASS_RATE
)


# -------------------------------------------------------------
# ПРОВЕРКА FORBIDDEN BEHAVIOR
# -------------------------------------------------------------

forbidden_behavior_gate = (
    forbidden_behavior_violation_rate
    <= MAX_FORBIDDEN_BEHAVIOR_VIOLATION_RATE
)


# -------------------------------------------------------------
# ПРОВЕРКА ERRORS
# -------------------------------------------------------------

errors_gate = (
    errors
    <= MAX_ERRORS
)


# =============================================================
# OVERALL QUALITY GATE
# =============================================================

quality_gate_passed = all(
    [
        pass_rate_gate,
        expected_properties_gate,
        forbidden_behavior_gate,
        errors_gate
    ]
)


if quality_gate_passed:

    overall_status = "PASS"

else:

    overall_status = "FAIL"


# =============================================================
# QUALITY GATE OUTPUT
# =============================================================

print()
print("=" * 80)
print("QUALITY GATE")
print("=" * 80)


print()

print(
    f"Pass Rate >= {MIN_PASS_RATE:.1f}%: "
    f"{'PASS' if pass_rate_gate else 'FAIL'} "
    f"(actual: {pass_rate:.1f}%)"
)


print(
    f"Expected Properties >= "
    f"{MIN_EXPECTED_PROPERTIES_PASS_RATE:.1f}%: "
    f"{'PASS' if expected_properties_gate else 'FAIL'} "
    f"(actual: {expected_properties_pass_rate:.1f}%)"
)


print(
    f"Forbidden Behavior <= "
    f"{MAX_FORBIDDEN_BEHAVIOR_VIOLATION_RATE:.1f}%: "
    f"{'PASS' if forbidden_behavior_gate else 'FAIL'} "
    f"(actual: {forbidden_behavior_violation_rate:.1f}%)"
)


print(
    f"Errors <= {MAX_ERRORS}: "
    f"{'PASS' if errors_gate else 'FAIL'} "
    f"(actual: {errors})"
)


print()
print(
    "QUALITY GATE STATUS:",
    overall_status
)

print("=" * 80)


# =============================================================
# СОХРАНЕНИЕ РЕЗУЛЬТАТОВ
# =============================================================

results_dir = (
    Path(__file__).parent
    / "results"
)


results_dir.mkdir(
    parents=True,
    exist_ok=True
)


results_file = (
    results_dir
    / "eval_results.json"
)


# =============================================================
# JSON REPORT
# =============================================================

report = {

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    "summary": {

        "total": total,

        "passed": passed,

        "failed": failed,

        "errors": errors,

        "pass_rate": round(
            pass_rate,
            1
        ),

        "average_score": round(
            average_score,
            2
        ),

        "expected_properties_pass_rate": round(
            expected_properties_pass_rate,
            1
        ),

        "forbidden_behavior_violation_rate": round(
            forbidden_behavior_violation_rate,
            1
        ),

        "overall_status": overall_status
    },


    # ---------------------------------------------------------
    # METRICS
    # ---------------------------------------------------------

    "metrics": {

        "expected_properties": {

            "total":
                total_expected_properties,

            "passed":
                passed_expected_properties,

            "pass_rate": round(
                expected_properties_pass_rate,
                1
            )
        },


        "forbidden_behavior": {

            "total":
                total_forbidden_behaviors,

            "violated":
                violated_forbidden_behaviors,

            "violation_rate": round(
                forbidden_behavior_violation_rate,
                1
            )
        }
    },


    # ---------------------------------------------------------
    # QUALITY GATE
    # ---------------------------------------------------------

    "quality_gate": {

        "status": overall_status,

        "criteria": {

            "pass_rate": {
                "threshold": MIN_PASS_RATE,
                "actual": round(
                    pass_rate,
                    1
                ),
                "passed": pass_rate_gate
            },

            "expected_properties_pass_rate": {
                "threshold":
                    MIN_EXPECTED_PROPERTIES_PASS_RATE,

                "actual": round(
                    expected_properties_pass_rate,
                    1
                ),

                "passed":
                    expected_properties_gate
            },

            "forbidden_behavior_violation_rate": {
                "threshold":
                    MAX_FORBIDDEN_BEHAVIOR_VIOLATION_RATE,

                "actual": round(
                    forbidden_behavior_violation_rate,
                    1
                ),

                "passed":
                    forbidden_behavior_gate
            },

            "errors": {
                "threshold": MAX_ERRORS,
                "actual": errors,
                "passed": errors_gate
            }
        }
    },


    # ---------------------------------------------------------
    # EVAL CASE RESULTS
    # ---------------------------------------------------------

    "results": eval_results
}


# =============================================================
# ЗАПИСЬ JSON
# =============================================================

with open(
    results_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        report,
        file,
        ensure_ascii=False,
        indent=2
    )


print()

print(
    f"Результаты сохранены: "
    f"{results_file}"
)