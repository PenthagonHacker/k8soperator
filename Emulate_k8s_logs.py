import time
import random
import json
from datetime import datetime

def log(event, **data):
    payload = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": event,
        **data
    }
    print(json.dumps(payload), flush=True)

def simulate_metrics():
    return {
        "cpu": round(random.uniform(10, 90), 2),
        "memory": round(random.uniform(100, 900), 2),
        "latency_ms": round(random.uniform(5, 250), 2),
        "errors": random.randint(0, 3)
    }

def main():
    log("job_start", message="K8s pod initialized 🧭")

    stages = ["ingest", "transform", "validate", "publish"]

    for stage in stages:
        log("stage_start", stage=stage)

        for i in range(3):
            metrics = simulate_metrics()
            log("metrics", stage=stage, step=i, **metrics)
            time.sleep(1)

        if random.random() < 0.25:
            log("warning", stage=stage, message="non-critical anomaly detected ⚠️")

        log("stage_end", stage=stage)

    log("job_complete", message="Pipeline finished successfully 🎯")

if __name__ == "__main__":
    main()#