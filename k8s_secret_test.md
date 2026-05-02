# KubernetesPodOperator — DAG с Secret Injection (объяснение)

## 📌 Что делает этот DAG
Этот DAG в Apache Airflow проверяет работу KubernetesPodOperator с использованием Kubernetes Secret. Он запускает pod в Kubernetes и передаёт секретное значение внутрь контейнера как переменную окружения.

---

# ⚙️ Общая логика выполнения DAG

## 1. Airflow запускает DAG
Airflow Scheduler видит задачу и отправляет её на выполнение.

## 2. KubernetesPodOperator создаёт Pod
Operator формирует описание pod (PodSpec) и отправляет его в Kubernetes API.

## 3. Kubernetes создаёт Pod
Pod появляется в namespace `airflow` в состоянии Pending → Running.

## 4. Kubernetes подготавливает контейнер
- скачивается Docker image (если нужно)
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
python -c "print(os.getenv('MY_API_KEY'))"
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

👉 Создай переменную окружения `MY_API_KEY`
👉 Не задавай её вручную
👉 Возьми значение из Kubernetes Secret `demo-secret`
👉 Используй ключ `MY_API_KEY` внутри этого Secret

---

# 🧠 Важная идея

Airflow НЕ хранит секрет.
Kubernetes НЕ хранит секрет в коде.

👉 Секрет живёт отдельно и "вкалывается" в pod только при запуске.

---

# 🔍 Что можно наблюдать в реальности

## Через Airflow UI:
- статус task
- логи выполнения

## Через Kubernetes:
```bash
kubectl get pods -n airflow
kubectl logs <pod>
```

---

# 🎯 Итог

Этот DAG демонстрирует:
- создание Kubernetes pod из Airflow
- безопасную передачу секретов
- выполнение кода внутри контейнера
- сбор логов обратно в Airflow

---

# 🚀 Следующий шаг (рекомендуется)

Можно расширить этот DAG и проверить:
- mount Secret как файл (`/etc/secrets/...`)
- multiple secrets injection
- RBAC permissions for secrets access
- shared volumes between pods

