import subprocess
import os
from google import genai

# Automatically find the pod name matching label 'app=retail'
def get_retail_pod_name(namespace="fss-clu"):
    try:
        # Run kubectl to get pods with label app=retail
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", namespace, "-l", "app=retail", "-o", "jsonpath={.items[0].metadata.name}"],
            capture_output=True, text=True, check=True
        )
        pod_name = result.stdout.strip()
        if pod_name:
            print(f"Detected active retail pod: {pod_name}")
            return pod_name
    except Exception as e:
        print(f"Error dynamically detecting pod via kubectl: {e}")
    
    # Fallback to search any pod in case label didn't match or failed
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", namespace, "-o", "jsonpath={.items[0].metadata.name}"],
            capture_output=True, text=True
        )
        pod_name = result.stdout.strip()
        if pod_name:
            print(f"Fallback detected pod: {pod_name}")
            return pod_name
    except Exception:
        pass
        
    print("Could not detect any pods. Using placeholder pod name.")
    return "retail-app-deployment-dynamic-fallback"

# Collect pod logs from Kubernetes
def get_logs(pod_name, namespace="fss-clu"):
    result = subprocess.run(
        ["kubectl", "logs", pod_name, "-n", namespace, "--tail=100"],
        capture_output=True, text=True
    )
    return result.stdout

# Collect pod events and describe output
def get_events(pod_name, namespace="fss-clu"):
    result = subprocess.run(
        ["kubectl", "describe", "pod", pod_name, "-n", namespace],
        capture_output=True, text=True
    )
    return result.stdout

# Get all pods status in namespace
def get_pods(namespace="fss-clu"):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace],
        capture_output=True, text=True
    )
    return result.stdout

# Get K8s events sorted by time
def get_k8s_events(namespace="fss-clu"):
    result = subprocess.run(
        ["kubectl", "get", "events", "-n", namespace, "--sort-by=.lastTimestamp"],
        capture_output=True, text=True
    )
    return result.stdout

# Get deployment rollout history
def get_rollout_history(namespace="fss-clu"):
    result = subprocess.run(
        ["kubectl", "rollout", "history", "deployment/retail-app-deployment", "-n", namespace],
        capture_output=True, text=True
    )
    return result.stdout

# Send data to Gemini AI for analysis
def analyze_with_gemini(data, scenario):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        msg = (
            "ERROR: GEMINI_API_KEY environment variable is not set.\n"
            "Please set it in PowerShell using:\n"
            "  $env:GEMINI_API_KEY=\"your-api-key-here\"\n"
            "Or get one for free from Google AI Studio: https://aistudio.google.com/"
        )
        return msg

    try:
        # Initialize client with specified key or let it pick from environment
        client = genai.Client(api_key=api_key)
        prompt = f"Kubernetes issue: {scenario}\n\nData:\n{data}\n\nFind root cause and provide step-by-step fix."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini API Error: {e}"

# Scenario 1: Retail App unavailable after deployment
def scenario1_app_unavailable(pod_name):
    print("\n--- Scenario 1: App unavailable after deployment ---")
    pods = get_pods()
    logs = get_logs(pod_name)
    events = get_k8s_events()
    data = f"Pods:\n{pods}\nLogs:\n{logs}\nEvents:\n{events}"
    print(analyze_with_gemini(data, "retail app is unavailable after deployment"))

# Scenario 2: Slow checkout response
def scenario2_slow_checkout(pod_name):
    print("\n--- Scenario 2: Customers report slow checkout ---")
    logs = get_logs(pod_name)
    events = get_events(pod_name)
    data = f"Logs:\n{logs}\nEvents:\n{events}"
    print(analyze_with_gemini(data, "slow checkout response, high latency reported by customers"))

# Scenario 3: Pods continuously restarting
def scenario3_pod_restart(pod_name):
    print("\n--- Scenario 3: Pods continuously restarting (CrashLoopBackOff) ---")
    logs = get_logs(pod_name)
    events = get_events(pod_name)
    data = f"Logs:\n{logs}\nEvents:\n{events}"
    print(analyze_with_gemini(data, "pods restarting CrashLoopBackOff - check resource limits and config"))

# Scenario 4: Production errors increase after new release
def scenario4_errors_after_release(pod_name):
    print("\n--- Scenario 4: Production errors increased after new release ---")
    logs = get_logs(pod_name)
    history = get_rollout_history()
    events = get_k8s_events()
    data = f"Deployment history:\n{history}\nError logs:\n{logs}\nEvents:\n{events}"
    print(analyze_with_gemini(data, "production errors increased after new release, possible regression"))

# Main
if __name__ == "__main__":
    print("Initializing FSS Retail AI-Driven Troubleshooting Agent...")
    pod = get_retail_pod_name()
    scenario1_app_unavailable(pod)
    scenario2_slow_checkout(pod)
    scenario3_pod_restart(pod)
    scenario4_errors_after_release(pod)