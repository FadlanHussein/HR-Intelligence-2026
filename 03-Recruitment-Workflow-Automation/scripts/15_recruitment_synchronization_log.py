
import pandas as pd
from pathlib import Path
from datetime import datetime
import uuid

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "data" / "processed"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_PATH = LOG_DIR / "recruitment_synchronization_log.csv"


def create_sync_log(
    source_file,
    incoming_records,
    database_records,
    new_records,
    inserted_records,
    skipped_records,
    sync_status
):
    sync_log = {
        "sync_id": str(uuid.uuid4()),
        "sync_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_file": source_file,
        "incoming_records": incoming_records,
        "database_records": database_records,
        "new_records": new_records,
        "inserted_records": inserted_records,
        "skipped_records": skipped_records,
        "sync_status": sync_status
    }

    log_df = pd.DataFrame([sync_log])

    if LOG_PATH.exists():
        log_df.to_csv(
            LOG_PATH,
            mode="a",
            header=False,
            index=False
        )
    else:
        log_df.to_csv(LOG_PATH, index=False)

    print("\nSYNCHRONIZATION LOG")
    print("-------------------------")
    print(f"Sync ID          : {sync_log['sync_id']}")
    print(f"Timestamp        : {sync_log['sync_timestamp']}")
    print(f"Source file      : {sync_log['source_file']}")
    print(f"Incoming records : {sync_log['incoming_records']}")
    print(f"Database records : {sync_log['database_records']}")
    print(f"New records      : {sync_log['new_records']}")
    print(f"Inserted records : {sync_log['inserted_records']}")
    print(f"Skipped records  : {sync_log['skipped_records']}")
    print(f"Status           : {sync_log['sync_status']}")

    return sync_log


if __name__ == "__main__":
    print("Synchronization logging module is ready.")
    print(f"Log destination: {LOG_PATH}")
