# Connect to the compute instance currently running my sims:
PROJECT="droc-199608"
ZONE="us-east1-b"
INSTANCE="psodroc-ce-4"
gcloud compute --project "$PROJECT" ssh --zone "$ZONE" "$INSTANCE"
