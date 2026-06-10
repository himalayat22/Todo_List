import subprocess
import os
import json
from datetime import datetime
from groq import Groq


NAMESPACE = "fss-clu"


# -----------------------------
# SAFE KUBECTL RUNNER
# -----------------------------
def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"


# -----------------------------
# KUBERNETES DATA COLLECTION
# -----------------------------
def get_pods():
    return run_cmd(["kubectl", "get", "pods", "-n", NAMESPACE, "-o", "wide"])


def get_services():
    return run_cmd(["kubectl", "get", "svc", "-n", NAMESPACE])


def get_deployments():
    return run_cmd(["kubectl", "get", "deployments", "-n", NAMESPACE])


def get_endpoints():
    return run_cmd(["kubectl", "get", "endpoints", "-n", NAMESPACE])


def get_events():
    return run_cmd(["kubectl", "get", "events", "-n", NAMESPACE, "--sort-by=.lastTimestamp"])


def get_top_pods():
    return run_cmd(["kubectl", "top", "pods", "-n", NAMESPACE])


def get_logs(pod):
    return run_cmd(["kubectl", "logs", pod, "-n", NAMESPACE, "--tail=100"])


def get_previous_logs(pod):
    return run_cmd([
        "kubectl", "logs", pod, "-n", NAMESPACE,
        "--previous", "--tail=100"
    ])


# -----------------------------
# POD DETECTION
# -----------------------------
def get_retail_pod():
    pod = run_cmd([
        "kubectl", "get", "pods",
        "-n", NAMESPACE,
        "-l", "app=retail",
        "-o", "jsonpath={.items[0].metadata.name}"
    ])
    return pod if pod else None


# -----------------------------
# INCIDENT DETECTION (REAL ONLY)
# -----------------------------
def detect_issues(pods, endpoints, deployments):
    issues = []

    if "CrashLoopBackOff" in pods:
        issues.append("CrashLoopBackOff detected")

    if "ImagePullBackOff" in pods or "ErrImagePull" in pods:
        issues.append("Image pull failure detected")

    if "0/1" in pods or "0/2" in pods:
        issues.append("Pod not ready")

    if "retail-app-service" in endpoints and "<none>" in endpoints:
        issues.append("Service has no endpoints")

    if "0/1" in deployments:
        issues.append("Deployment not fully available")

    return issues


# -----------------------------
# GROQ ANALYSIS
# -----------------------------
def analyze_with_groq(evidence, issues):
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return "ERROR: GROQ_API_KEY not set"

    client = Groq(api_key=api_key)

    prompt = f"""
You are a Senior Kubernetes SRE.

Analyze ONLY real evidence.
Do NOT assume incidents.

If issues list is empty, respond:
"Cluster is healthy - no active incidents"

If issues exist, provide:

1. Detected Issues
2. Root Cause (only if supported by evidence)
3. Evidence
4. Fix Steps
5. kubectl validation commands
6. Severity (Low/Medium/High/Critical)

ISSUES:
{issues}

EVIDENCE:
{json.dumps(evidence, indent=2)}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a Kubernetes production SRE. Be strict, factual, and never hallucinate."
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=1500,
    )

    return response.choices[0].message.content


# -----------------------------
# MAIN AGENT
# -----------------------------
def main():
    print("\n" + "=" * 80)
    print("KUBERNETES AI SRE AGENT (EVIDENCE-DRIVEN)")
    print("=" * 80)

    pod = get_retail_pod()

    pods = get_pods()
    services = get_services()
    deployments = get_deployments()
    endpoints = get_endpoints()
    events = get_events()
    metrics = get_top_pods()

    logs = get_logs(pod) if pod else "No pod found"
    prev_logs = get_previous_logs(pod) if pod else "No pod found"

    issues = detect_issues(pods, endpoints, deployments)

    evidence = {
        "pods": pods,
        "services": services,
        "deployments": deployments,
        "endpoints": endpoints,
        "events": events[-2000:],  # limit size
        "metrics": metrics,
        "logs": logs,
        "previous_logs": prev_logs,
    }

    print("\nDetected Issues:", issues)

    print("\n" + "=" * 80)
    print(analyze_with_groq(evidence, issues))
    print("=" * 80)


if __name__ == "__main__":
    main()