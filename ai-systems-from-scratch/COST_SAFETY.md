# Cloud & GPU Cost Safety Policy

> **Golden Rule:** Never assume cloud or accelerator resources are free. Never leave instances, GPUs, or unbudgeted agent loops running unattended.

---

## 1. Execution Tier Cost Estimates

| Tier | Typical Hardware | Target Workloads | Estimated Cost (Cloud / Self-Hosted) |
| :--- | :--- | :--- | :--- |
| **Tier 1 (CPU)** | Local Laptop / Workstation (Mac/Linux/Win) | Graph IRs, tiny transformers, manual loops, agents, evals | **$0.00** (Local execution) |
| **Tier 2 (Single GPU)** | NVIDIA RTX 3060/4090 or Cloud A10G / L4 | Fine-tuning (LoRA 7B), Triton kernels, vLLM single-node | **~$0.60 – $1.20 / hour** (Spot/On-Demand) |
| **Tier 3 (Multi-GPU)** | 4x A100 / 8x H100 (Optional advanced labs) | Tensor parallelism (TP=4), pipeline parallelism | **~$8.00 – $24.00 / hour** |

---

## 2. Resource Allocation, Shutdown & Verification Checklist

Whenever launching cloud compute (AWS EC2, Lambda Labs, RunPod, GCP, Vast.ai):

### Step 1: Pre-Job Budget Cap
- Always set a hard billing alert and max hourly budget cap on your cloud provider dashboard.
- For agent experiments, set a token/turn hard limit (`MAX_AGENT_TURNS=10`, `DEFAULT_BUDGET_USD=0.50`).

### Step 2: Immediate Auto-Stop Configuration
Configure instances to terminate on idle or upon job completion:
```bash
# Example: Self-terminating run script on AWS/RunPod
python training/train_lora.py && sudo shutdown -h now
```

### Step 3: Verification of Resource Teardown
Never trust that closing your browser tab stopped a GPU. Run the verification CLI commands:

#### AWS EC2 Verification
```bash
# List all running or pending GPU instances
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running,pending" \
    --query "Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name]" \
    --output table

# Stop or terminate explicitly
aws ec2 terminate-instances --instance-ids <INSTANCE_ID>
```

#### RunPod / Lambda Labs Verification
```bash
# Check active pods
runpodctl get pods
# Terminate pod
runpodctl remove pod <POD_ID>
```

#### GCP Compute Verification
```bash
gcloud compute instances list --filter="status=RUNNING"
gcloud compute instances stop <INSTANCE_NAME> --zone=<ZONE>
```

---

## 3. Storage & Residual Cost Traps

Stopping a compute instance does **NOT** stop billing for:
1. **Elastic Block Storage (EBS / Persistent Disks):** A 500GB SSD costs ~$40–50/month even if the GPU instance is stopped! Always delete detached disks or take a snapshot and delete the volume.
2. **Elastic / Public IPs:** Cloud providers charge ~$0.005/hour for idle unattached static public IPv4 addresses.
3. **Artifact / Model Registries:** Delete temporary checkpoints (`outputs/checkpoints/`) after logging evaluation metrics.

---

## 4. Local Cleanup Command
Inside this repository, always run:
```bash
make clean
```
to purge local temporary checkpoints, disk-heavy `.pt` cache files, and diagnostic artifacts before pushing code.
