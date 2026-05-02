# KubernetesPodOperator — DAG с использованием "секрета".

## Полный пример оператора

```python
KubernetesPodOperator(
        task_id="read_secret",
        name="secret-test-pod",
        namespace="airflow",
        image="python:3.11-slim",
        cmds=["python", "-c"],
        arguments=[
            "import os; "
            "print('SECRET VALUE:', os.getenv('MY_API_KEY'))"  # (ТОЛЬКО В ДЕМОНСТРАЦИОННЫХ ЦЕЛЯХ. В ПРОДЕ ТАК НЕ ДЕЛАТЬ!)
        ],
        env_vars=[
            V1EnvVar(
                name="MY_API_KEY",
                value_from=V1EnvVarSource(
                    secret_key_ref=V1SecretKeySelector(
                        name="demo-secret",
                        key="MY_API_KEY",
                    )
                ),
            )
        ],
        get_logs=True,
        is_delete_operator_pod=False,
    )
```

## 📌 Что делает этот DAG
Даг демонстрирует работу KubernetesPodOperator с использованием Kubernetes Secret. Он запускает pod в Kubernetes и передаёт "секрет" в контейнер как переменную окружения.

---

# ⚙️ Общая логика выполнения DAG

## 1. Airflow запускает DAG
Airflow Scheduler видит задачу и отправляет её на выполнение.

## 2. KubernetesPodOperator создаёт Pod
Оператор формирует описание pod (PodSpec) и отправляет его в Kubernetes API.

## 3. Kubernetes создаёт Pod
Pod появляется в namespace `airflow` в состоянии Pending → Running.

## 4. Kubernetes подготавливает контейнер
- скачивается Docker image
- создаётся runtime среда
- монтируются переменные окружения

## 5. Injection Secret → Env Var
Kubernetes берёт значение из Secret:

- Secret name: `demo-secret`
- Key: `MY_API_KEY`

и вставляет его в контейнер как:

```
MY_API_KEY=actual_secret_value
```

## 6. Запуск команды внутри контейнера
Контейнер выполняет команду Python:

```
python -c "print(os.getenv('MY_API_KEY'))"    (ТОЛЬКО В ДЕМОНСТРАЦИОННЫХ ЦЕЛЯХ. В ПРОДЕ ТАК НЕ ДЕЛАТЬ!)
```

## 7. Логи отправляются в Airflow
Если `get_logs=True`, Airflow читает stdout контейнера и показывает результат в UI.

## 8. Завершение Pod
- если `is_delete_operator_pod=True` → pod удаляется
- если False → pod остаётся для дебага

---

# 🔐 Как работает Secret Injection

## Структура:

```python
V1EnvVar(
    name="MY_API_KEY",
    value_from=V1EnvVarSource(
        secret_key_ref=V1SecretKeySelector(
            name="demo-secret",
            key="MY_API_KEY"
        )
    )
)
```

## Что это значит простыми словами:

- Создай переменную окружения `MY_API_KEY`
- Не задавай её вручную
- Возьми значение из Kubernetes Secret `demo-secret`
- Используй ключ `MY_API_KEY` внутри этого Secret

---

Airflow НЕ хранит секрет.
Kubernetes НЕ хранит секрет в коде.
