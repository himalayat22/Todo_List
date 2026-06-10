import subprocess
import os
import json
from groq import Groq

NAMESPACE = "retail"


# -----------------------------
# SAFE COMMAND RUNNER
# -----------------------------
def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"


def run_json(cmd):
    output = run_cmd(cmd)
    try:
        return json.loads(output)
    except:
        return {}


# -----------------------------
# K8S DATA (JSON BASED)
# -----------------------------
def get_pods():
    return run_json(["kubectl", "get", "pods", "-n", NAMESPACE, "-o", "json"])


def get_services():
    return run_json(["kubectl", "get", "svc", "-n", NAMESPACE, "-o", "json"])


def get_deployments():
    return run_json(["kubectl", "get", "deployments", "-n", NAMESPACE, "-o", "json"])


def get_endpoints():
    return run_json(["kubectl", "get", "endpoints", "-n", NAMESPACE, "-o", "json"])


def get_events():
    return run_cmd([
        "kubectl", "get", "events",
        "-n", NAMESPACE,
        "--sort-by=.lastTimestamp"
    ])


def get_metrics():
    return run_cmd(["kubectl", "top", "pods", "-n", NAMESPACE])


# -----------------------------
# POD UTILITIES
# -----------------------------
def get_first_pod_name(pods_json):
    items = pods_json.get("items", [])
    if not items:
        return None
    return items[0]["metadata"]["name"]


def get_logs(pod):
    if not pod:
        return "No pod found"
    return run_cmd(["kubectl", "logs", pod, "-n", NAMESPACE, "--tail=100"])


def get_previous_logs(pod):
    if not pod:
        return "No pod found"
    return run_cmd([
        "kubectl", "logs", pod,
        "-n", NAMESPACE,
        "--previous",
        "--tail=100"
    ])


# -----------------------------
# ISSUE DETECTION (REAL LOGIC)
# -----------------------------
def detect_issues(pods, deployments, endpoints):
    issues = []

    # ---- POD HEALTH ----
    for pod in pods.get("items", []):
        name = pod["metadata"]["name"]
        phase = pod["status"].get("phase")

        if phase != "Running":
            issues.append(f"Pod {name} not running (phase={phase})")

        for cs in pod["status"].get("containerStatuses", []):
            if not cs.get("ready"):
                issues.append(f"Container not ready in pod {name}")

            state = cs.get("state", {})
            if "waiting" in state:
                reason = state["waiting"].get("reason", "")
                if reason:
                    issues.append(f"{name} waiting: {reason}")

    # ---- DEPLOYMENTS ----
    dep_items = deployments.get("items", [])
    if not dep_items:
        issues.append("No deployments found in namespace")

    for dep in dep_items:
        name = dep["metadata"]["name"]
        desired = dep["spec"]["replicas"]
        available = dep["status"].get("availableReplicas", 0)

        if available < desired:
            issues.append(
                f"Deployment {name} not fully available ({available}/{desired})"
            )

    # ---- ENDPOINTS ----
    for ep in endpoints.get("items", []):
        name = ep["metadata"]["name"]
        subsets = ep.get("subsets")

        if not subsets:
            issues.append(f"Service {name} has no active endpoints")

    return list(set(issues))


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
2. Root Cause (ONLY if evidence supports it)
3. Evidence
4. Fix Steps
5. kubectl validation commands
6. Severity

ISSUES:
{issues}

EVIDENCE:
{json.dumps(evidence, indent=2)[:12000]}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a strict Kubernetes SRE. No guessing."
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=1200,
    )

    return response.choices[0].message.content


# -----------------------------
# MAIN
# -----------------------------
def main():
    print("\n" + "=" * 80)
    print("KUBERNETES AI SRE AGENT (PRODUCTION)")
    print("=" * 80)

    pods = get_pods()
    services = get_services()
    deployments = get_deployments()
    endpoints = get_endpoints()
    events = get_events()
    metrics = get_metrics()

    pod_name = get_first_pod_name(pods)

    logs = get_logs(pod_name)
    prev_logs = get_previous_logs(pod_name)

    issues = detect_issues(pods, deployments, endpoints)

    evidence = {
        "pods": pods,
        "services": services,
        "deployments": deployments,
        "endpoints": endpoints,
        "events": events[-2000:],
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
