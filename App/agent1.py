import os
import time
import subprocess
from groq import Groq


# Collect kubectl logs for a pod
def get_logs(pod_name, namespace="retail"):
    result = subprocess.run(
        ["kubectl", "logs", pod_name, "-n", namespace, "--tail=100"],
        capture_output=True,
        text=True
    )
    return result.stdout


# Collect pod events and status details
def get_events(pod_name, namespace="retail"):
    result = subprocess.run(
        ["kubectl", "describe", "pod", pod_name, "-n", namespace],
        capture_output=True,
        text=True
    )
    return result.stdout


# Get all pods in namespace
def get_pods(namespace="retail"):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace],
        capture_output=True,
        text=True
    )
    return result.stdout


# Get recent K8s events sorted by time
def get_k8s_events(namespace="retail"):
    result = subprocess.run(
        [
            "kubectl",
            "get",
            "events",
            "-n",
            namespace,
            "--sort-by=.lastTimestamp"
        ],
        capture_output=True,
        text=True
    )
    return result.stdout


# Analyze Kubernetes data using Groq
def analyze_with_groq(logs, events, scenario):
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return (
            "\nERROR: GROQ_API_KEY environment variable is not set.\n"
            "Set it using:\n"
            "export GROQ_API_KEY='your-key'\n"
            "or PowerShell:\n"
            "$env:GROQ_API_KEY='your-key'\n"
        )

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
You are a Senior Kubernetes SRE and Production Incident Response Engineer.

Scenario:
{scenario}

Logs/Data:
{logs}

Events:
{events}

Analyze the issue and provide:

1. Executive Summary
2. Most Likely Root Cause
3. Supporting Evidence
4. Step-by-Step Remediation
5. Validation Commands
6. Preventive Measures
7. Severity Level (Low/Medium/High/Critical)

Provide practical Kubernetes commands wherever applicable.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Kubernetes, DevOps, "
                        "Cloud Native, and SRE troubleshooting assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=2000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq API Error: {e}"


# Scenario 1: Pod continuously restarting
def troubleshoot_pod_restart(pod_name):
    print("\n" + "=" * 80)
    print("SCENARIO 1: POD RESTARTING (CrashLoopBackOff)")
    print("=" * 80)

    logs = get_logs(pod_name)
    events = get_events(pod_name)

    analysis = analyze_with_groq(
        logs,
        events,
        "Pod is continuously restarting / CrashLoopBackOff"
    )

    print(analysis)


# Scenario 2: High latency after deployment
def troubleshoot_high_latency(pod_name):
    print("\n" + "=" * 80)
    print("SCENARIO 2: HIGH LATENCY AFTER DEPLOYMENT")
    print("=" * 80)

    logs = get_logs(pod_name)
    events = get_events(pod_name)

    analysis = analyze_with_groq(
        logs,
        events,
        "Application latency increased after deployment"
    )

    print(analysis)


# Scenario 3: Deployment failure
def troubleshoot_deployment_failure(namespace="retail"):
    print("\n" + "=" * 80)
    print("SCENARIO 3: DEPLOYMENT FAILURE")
    print("=" * 80)

    events = get_k8s_events(namespace)
    pods = get_pods(namespace)

    analysis = analyze_with_groq(
        pods,
        events,
        "Deployment failed in Kubernetes"
    )

    print(analysis)


# Dynamically discover userprofile pod
def get_userprofile_pod(namespace="retail"):
    try:
        result = subprocess.run(
            [
                "kubectl",
                "get",
                "pods",
                "-n",
                namespace,
                "-l",
                "app=userprofile",
                "-o",
                "jsonpath={.items[0].metadata.name}"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        pod = result.stdout.strip()

        if pod:
            print(f"Detected userprofile pod: {pod}")
            return pod

    except Exception as e:
        print(f"Error discovering pod: {e}")

    try:
        result = subprocess.run(
            [
                "kubectl",
                "get",
                "pods",
                "-n",
                namespace,
                "-o",
                "jsonpath={.items[0].metadata.name}"
            ],
            capture_output=True,
            text=True
        )

        pod = result.stdout.strip()

        if pod:
            print(f"Fallback pod detected: {pod}")
            return pod

    except Exception:
        pass

    print("No pod found. Using fallback pod name.")
    return "userprofile-rollout-7c79cc995f-pzlsq"


# Main
if __name__ == "__main__":
    print("\nInitializing AI-Driven Kubernetes Troubleshooting Agent (Groq)...\n")

    pod = get_userprofile_pod()

    troubleshoot_pod_restart(pod)

    print("\nWaiting 2 seconds before next analysis...\n")
    time.sleep(2)

    troubleshoot_high_latency(pod)

    print("\nWaiting 2 seconds before next analysis...\n")
    time.sleep(2)

    troubleshoot_deployment_failure()

    print("\nTroubleshooting completed.\n")