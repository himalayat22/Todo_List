import subprocess
import os
from groq import Groq


# Automatically find the pod name matching label 'app=retail'
def get_retail_pod_name(namespace="fss-clu"):
    try:
        result = subprocess.run(
            [
                "kubectl",
                "get",
                "pods",
                "-n",
                namespace,
                "-l",
                "app=retail",
                "-o",
                "jsonpath={.items[0].metadata.name}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        pod_name = result.stdout.strip()

        if pod_name:
            print(f"Detected active retail pod: {pod_name}")
            return pod_name

    except Exception as e:
        print(f"Error dynamically detecting pod via kubectl: {e}")

    # Fallback: first pod in namespace
    try:
        result = subprocess.run(
            [
                "kubectl",
                "get",
                "pods",
                "-n",
                namespace,
                "-o",
                "jsonpath={.items[0].metadata.name}",
            ],
            capture_output=True,
            text=True,
        )

        pod_name = result.stdout.strip()

        if pod_name:
            print(f"Fallback detected pod: {pod_name}")
            return pod_name

    except Exception:
        pass

    print("Could not detect any pods.")
    return "retail-app-deployment-dynamic-fallback"


# Collect pod logs
def get_logs(pod_name, namespace="fss-clu"):
    result = subprocess.run(
        ["kubectl", "logs", pod_name, "-n", namespace, "--tail=100"],
        capture_output=True,
        text=True,
    )
    return result.stdout


# Collect pod describe output
def get_events(pod_name, namespace="fss-clu"):
    result = subprocess.run(
        ["kubectl", "describe", "pod", pod_name, "-n", namespace],
        capture_output=True,
        text=True,
    )
    return result.stdout


# Get all pods
def get_pods(namespace="fss-clu"):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace],
        capture_output=True,
        text=True,
    )
    return result.stdout


# Get cluster events
def get_k8s_events(namespace="fss-clu"):
    result = subprocess.run(
        [
            "kubectl",
            "get",
            "events",
            "-n",
            namespace,
            "--sort-by=.lastTimestamp",
        ],
        capture_output=True,
        text=True,
    )
    return result.stdout


# Deployment rollout history
def get_rollout_history(namespace="fss-clu"):
    result = subprocess.run(
        [
            "kubectl",
            "rollout",
            "history",
            "deployment/retail-app-deployment",
            "-n",
            namespace,
        ],
        capture_output=True,
        text=True,
    )
    return result.stdout


# Analyze using Groq
def analyze_with_groq(data, scenario):
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return (
            "\nERROR: GROQ_API_KEY environment variable not found.\n"
            "Set it using:\n"
            "export GROQ_API_KEY='your-key'\n"
            "or\n"
            "$env:GROQ_API_KEY='your-key'\n"
        )

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
You are a Senior Kubernetes SRE and Production Troubleshooting Expert.

Scenario:
{scenario}

Kubernetes Diagnostic Data:
{data}

Provide:

1. Executive Summary
2. Most Likely Root Cause
3. Supporting Evidence
4. Step-by-Step Fix
5. kubectl Commands to Validate
6. Preventive Measures
7. Severity Level (Low/Medium/High/Critical)
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Kubernetes production "
                        "troubleshooter specializing in EKS, AKS, "
                        "GKE, OpenShift, and cloud-native systems."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=2000,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq API Error: {e}"


# Scenario 1
def scenario1_app_unavailable(pod_name):
    print("\n" + "=" * 80)
    print("SCENARIO 1: Retail App Unavailable After Deployment")
    print("=" * 80)

    pods = get_pods()
    logs = get_logs(pod_name)
    events = get_k8s_events()

    data = f"""
Pods:
{pods}

Logs:
{logs}

Events:
{events}
"""

    print(
        analyze_with_groq(
            data,
            "Retail application unavailable after deployment",
        )
    )


# Scenario 2
def scenario2_slow_checkout(pod_name):
    print("\n" + "=" * 80)
    print("SCENARIO 2: Slow Checkout Response")
    print("=" * 80)

    logs = get_logs(pod_name)
    events = get_events(pod_name)

    data = f"""
Logs:
{logs}

Pod Details:
{events}
"""

    print(
        analyze_with_groq(
            data,
            "Customers report slow checkout response and high latency",
        )
    )


# Scenario 3
def scenario3_pod_restart(pod_name):
    print("\n" + "=" * 80)
    print("SCENARIO 3: CrashLoopBackOff")
    print("=" * 80)

    logs = get_logs(pod_name)
    events = get_events(pod_name)

    data = f"""
Logs:
{logs}

Pod Events:
{events}
"""

    print(
        analyze_with_groq(
            data,
            "Pods continuously restarting with CrashLoopBackOff",
        )
    )


# Scenario 4
def scenario4_errors_after_release(pod_name):
    print("\n" + "=" * 80)
    print("SCENARIO 4: Errors Increased After New Release")
    print("=" * 80)

    logs = get_logs(pod_name)
    history = get_rollout_history()
    events = get_k8s_events()

    data = f"""
Deployment History:
{history}

Error Logs:
{logs}

Cluster Events:
{events}
"""

    print(
        analyze_with_groq(
            data,
            "Production errors increased after a new release. "
            "Possible regression or deployment issue.",
        )
    )


# Main
if __name__ == "__main__":
    print("\nInitializing FSS Retail AI-Driven Troubleshooting Agent (Groq)...\n")

    pod = get_retail_pod_name()

    scenario1_app_unavailable(pod)
    scenario2_slow_checkout(pod)
    scenario3_pod_restart(pod)
    scenario4_errors_after_release(pod)