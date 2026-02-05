import boto3
from datetime import datetime, timezone


# BUCKET_NAME = SECRET! 
# CUTOFF_DATE_STRING = SECRET!

s3 = boto3.client("s3")

cutoff_date = datetime.strptime(
    CUTOFF_DATE_STRING, "%Y-%m-%dT%H:%M:%SZ"
).replace(tzinfo=timezone.utc)

def delete_versions_after_date(bucket_name, cutoff):
    paginator = s3.get_paginator("list_object_versions")
    for page in paginator.paginate(Bucket=bucket_name):
        versions = page.get("Versions", [])
        for version in versions:
            last_modified = version["LastModified"]

            if last_modified > cutoff:
                key = version["Key"]
                version_id = version["VersionId"]

                print(
                    f"Deleting {key} "
                    f"(VersionId: {version_id}, date: {last_modified})"
                )

                try:
                    s3.delete_object(
                        Bucket=bucket_name,
                        Key=key,
                        VersionId=version_id
                    )
                except Exception as e:
                    print(f"ERROR, deleting {key}: {e}")


if __name__ == "__main__":
    delete_versions_after_date(BUCKET_NAME, cutoff_date)
    print("Process has been done :)")
