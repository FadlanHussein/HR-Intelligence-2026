
from pathlib import Path
import subprocess
import sys
import csv
import time
import uuid
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPT_DIR = BASE_DIR / "scripts"

LOG_DIR = BASE_DIR / "data" / "processed"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline_execution_log.csv"

PIPELINE_STAGES = [
    {
        "name": "DATA VALIDATION",
        "script": "01_candidate_data_validation.py"
    },
    {
        "name": "DATA CLEANING",
        "script": "03_candidate_data_cleaning.py"
    },
    {
        "name": "WORKFLOW AUTOMATION",
        "script": "04_recruitment_workflow_automation.py"
    }
]

LOG_COLUMNS = [
    "run_id",
    "stage",
    "started_at",
    "finished_at",
    "duration_seconds",
    "status",
    "exit_code",
    "message"
]


def write_log(log_records):
    file_exists = LOG_FILE.exists()

    with open(
        LOG_FILE,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=LOG_COLUMNS
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(log_records)


run_id = str(uuid.uuid4())[:8]

pipeline_started_at = datetime.now().astimezone()
pipeline_start_timer = time.perf_counter()

log_records = []
pipeline_success = True

print("\n=== RECRUITMENT AUTOMATION PIPELINE ===")
print(f"Run ID       : {run_id}")
print(f"Started at   : {pipeline_started_at.isoformat(timespec='seconds')}")

for index, stage in enumerate(PIPELINE_STAGES, start=1):

    script_path = SCRIPT_DIR / stage["script"]

    stage_started_at = datetime.now().astimezone()
    stage_start_timer = time.perf_counter()

    print(f"\n=== STEP {index}: {stage['name']} ===")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR
    )

    stage_finished_at = datetime.now().astimezone()
    stage_duration = round(
        time.perf_counter() - stage_start_timer,
        2
    )

    if result.returncode == 0:

        stage_status = "SUCCESS"
        message = "Stage completed successfully."

        print(f"\nSTEP {index} STATUS: SUCCESS")

    else:

        stage_status = "FAILED"
        message = "Stage failed. Pipeline execution stopped."

        print(f"\nPIPELINE FAILED: {stage['name']}")
        print(f"Exit code: {result.returncode}")

        pipeline_success = False

    log_records.append({
        "run_id": run_id,
        "stage": stage["name"],
        "started_at": stage_started_at.isoformat(timespec="seconds"),
        "finished_at": stage_finished_at.isoformat(timespec="seconds"),
        "duration_seconds": stage_duration,
        "status": stage_status,
        "exit_code": result.returncode,
        "message": message
    })

    if not pipeline_success:

        for skipped_stage in PIPELINE_STAGES[index:]:

            log_records.append({
                "run_id": run_id,
                "stage": skipped_stage["name"],
                "started_at": "",
                "finished_at": "",
                "duration_seconds": 0,
                "status": "SKIPPED",
                "exit_code": "",
                "message": "Skipped because previous stage failed."
            })

        break


pipeline_finished_at = datetime.now().astimezone()

pipeline_duration = round(
    time.perf_counter() - pipeline_start_timer,
    2
)

if pipeline_success:
    overall_status = "COMPLETED"
    pipeline_exit_code = 0
else:
    overall_status = "FAILED"
    pipeline_exit_code = 1

log_records.append({
    "run_id": run_id,
    "stage": "PIPELINE SUMMARY",
    "started_at": pipeline_started_at.isoformat(timespec="seconds"),
    "finished_at": pipeline_finished_at.isoformat(timespec="seconds"),
    "duration_seconds": pipeline_duration,
    "status": overall_status,
    "exit_code": pipeline_exit_code,
    "message": "Overall pipeline execution result."
})

write_log(log_records)

print("\n=== PIPELINE EXECUTION SUMMARY ===")
print(f"Run ID       : {run_id}")
print(f"Started at   : {pipeline_started_at.isoformat(timespec='seconds')}")
print(f"Finished at  : {pipeline_finished_at.isoformat(timespec='seconds')}")
print(f"Duration     : {pipeline_duration} seconds")
print(f"Overall      : {overall_status}")
print(f"Log file     : {LOG_FILE}")

sys.exit(pipeline_exit_code)
