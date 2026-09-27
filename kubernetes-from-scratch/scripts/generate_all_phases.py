#!/usr/bin/env python3
"""
generate_all_phases.py - Builds the complete 121-Phase curriculum for kubernetes-from-scratch.

Generates:
  phases/<phase_num>-<phase_slug>/
    docs/en.md
    manifests/ (where applicable)
    code/ (where applicable)
    experiments/run_experiment.sh (where applicable)
    outputs/evidence-template.md
"""

import os
import sys

PHASES_META = [
    (0, "local-kubernetes-lab", "Local Kubernetes Lab",
     "kubectl is an API client speaking HTTPS to kube-apiserver, not a local container runner.",
     "How do we create a reproducible, multi-node Kubernetes development environment without burning cloud credits or masking distributed systems realities?",
     "Local single-node or multi-node kind cluster setup, client vs server split, kubectl cluster-info.",
     "kubectl cluster-info\nkubectl get nodes -o wide\nkubectl version"),
    (1, "why-kubernetes-exists", "Why Kubernetes Exists",
     "Running containers is easy; coordinating hundreds of them across failing machines is the real problem.",
     "You have 3 physical servers and 20 Docker containers. Server B catches fire at 3 AM. Who detects the failure, chooses new hosts, routes traffic, and reattaches storage?",
     "The distributed orchestration problem: process scheduling, failure detection, service identity, and automated healing.",
     "docker run -d --name web-1 nginx\ndocker run -d --name web-2 nginx"),
    (2, "desired-state", "Desired State",
     "Stop telling the computer what steps to take; tell it what reality must look like.",
     "Imperative scripts ('start container X', 'restart container Y') accumulate state drift, fail midway, and cannot self-heal after reboots.",
     "Declarative desired state vs imperative execution. Desired: replicas = 3. Actual: replicas = 2.",
     "python3 phases/02-desired-state/01-mini-controller/code/mini_controller.py --test"),
    (3, "reconciliation-loops", "Reconciliation Loops",
     "The control loop never sleeps: Observe, Compare, Act, Repeat.",
     "If a process dies after an imperative script exits, nothing restarts it. How does a system continuously ensure reality matches intention?",
     "Control theory, level-triggered feedback loops, Delta = Desired - Actual.",
     "python3 phases/02-desired-state/01-mini-controller/code/mini_controller.py"),
    (4, "kubernetes-api", "Kubernetes API",
     "YAML is not Kubernetes; YAML is merely serialized JSON sent over an HTTP REST API.",
     "Engineers memorize YAML indentation without understanding that every manifest is an HTTP request payload evaluated by a REST server.",
     "Resource schemas, OpenAPI validation, JSON representation, and kube-apiserver endpoints.",
     "kubectl get pods -o json\nkubectl get --raw /api/v1/namespaces/default/pods"),
    (5, "etcd-concept", "etcd Concept",
     "The cluster state lives in etcd; the API server is its sole guardian.",
     "Where does cluster truth live? What happens if two controllers write conflicting updates simultaneously?",
     "Distributed consensus (Raft), atomic compare-and-swap, watches, and single source of truth.",
     "kubectl get pods -n kube-system -l component=etcd"),
    (6, "pods-from-first-principles", "Pods From First Principles",
     "A Pod is not a container; a Pod is a shared Linux execution context containing one or more containers.",
     "Containers need to share localhost networking and shared storage volumes without merging into a giant monolithic image.",
     "Linux namespaces (Network, IPC, UTS), cgroups, pause container, and shared localhost.",
     "kubectl apply -f manifests/pod.yaml\nkubectl get pod demo-pod -o wide"),
    (7, "pod-lifecycle", "Pod Lifecycle",
     "A container process running in the kernel does not mean the Pod is ready to serve users.",
     "Distinguishing Pending, Running, Succeeded, Failed, and CrashLoopBackOff states.",
     "Pod phases, container state transitions, exit codes (137 vs 1 vs 0), and restart policies.",
     "kubectl describe pod demo-pod\nkubectl get pod demo-pod -o jsonpath='{.status.conditions[*]}'"),
    (8, "multi-container-pods", "Multi-Container Pods",
     "Sidecars share network identity and storage volumes with the main application container.",
     "An application needs log shipping or local caching proxying without contaminating the main codebase.",
     "Shared network namespace, shared emptyDir volumes, localhost loopback communication.",
     "kubectl apply -f manifests/multi-container-pod.yaml"),
    (9, "nodes", "Nodes",
     "A worker node is a Linux host running kubelet, a container runtime, and a network proxy.",
     "How does the control plane know a machine has capacity, is alive, and can run workloads?",
     "Node heartbeats, NodeLeases, allocatable capacity vs total capacity, kubelet responsibilities.",
     "kubectl describe node k8s-scratch-cluster-worker"),
    (10, "scheduling-from-scratch", "Scheduling From Scratch",
     "Scheduling is filtering candidate nodes then scoring the survivors.",
     "Given 100 nodes with varying CPU, memory, and hardware constraints, which node should run an incoming Pod?",
     "The 3-stage scheduler pipeline: Pre-filter, Filter (predicates), Score (priorities), and Reserve/Bind.",
     "python3 phases/10-scheduling-from-scratch/01-scheduling-simulator/code/scheduler_sim.py"),
    (11, "kube-scheduler", "kube-scheduler",
     "The scheduler binds unscheduled pods to nodes; it does not start containers.",
     "Watching Pods where spec.nodeName is empty and writing a Binding object to the API server.",
     "Scheduler watch loop, binding subresource, two-phase scheduling.",
     "kubectl get pods -A -o wide --watch"),
    (12, "requests-and-limits", "Requests and Limits",
     "Requests govern scheduling decisions; limits govern kernel runtime enforcement.",
     "Workloads starve neighbor processes of memory or monopolize CPU cores without resource boundaries.",
     "Scheduling accounting vs Linux cgroups (cpu.shares/cpu.cfs_quota_us and memory.max).",
     "kubectl apply -f manifests/resource-requests.yaml"),
    (13, "oom-and-cpu-throttling", "OOM and CPU Throttling",
     "CPU exhaustion causes latency throttling; memory exhaustion causes instant termination.",
     "Developers confuse CPU throttling with OOM kills. CPU is compressible; memory is non-compressible.",
     "Linux kernel CFS throttling, OOM-killer invocation (Exit Code 137), dmesg inspection.",
     "kubectl describe pod oom-workload | grep -i oom"),
    (14, "labels", "Labels",
     "Labels are the multidimensional metadata substrate connecting independent cluster objects.",
     "In a cluster with 10,000 pods, hardcoded hierarchical trees break. How do controllers group related pods?",
     "Key-value metadata, loose coupling, non-hierarchical tagging.",
     "kubectl get pods --show-labels\nkubectl label pod demo-pod tier=backend"),
    (15, "selectors", "Selectors",
     "Selectors query the cluster state to form dynamic sets.",
     "Controllers and Services need to target specific groups of workloads without knowing their individual names.",
     "Equality-based selectors vs set-based selectors (matchLabels vs matchExpressions).",
     "kubectl get pods -l tier=frontend\nkubectl get pods -l 'app in (web, demo)'"),
    (16, "replicaset-from-first-principles", "ReplicaSet From First Principles",
     "A ReplicaSet guarantees that a specific number of pod replicas are running at any given moment.",
     "If you run 3 pods manually and one node dies, those pods are gone forever. Who restores the count?",
     "ReplicaSet controller reconciliation, selector ownership, orphan adoption.",
     "kubectl apply -f manifests/replicaset.yaml\nkubectl delete pod -l app=web-server"),
    (17, "controllers", "Controllers",
     "Controllers are autonomous control loops compiled into kube-controller-manager.",
     "How are Deployments, Nodes, Namespaces, and Endpoints managed without human operators?",
     "Informers, Lister indexers, workqueues, level-triggered reconciliation.",
     "kubectl get pods -n kube-system -l component=kube-controller-manager"),
    (18, "deployments", "Deployments",
     "Deployments manage ReplicaSets; ReplicaSets manage Pods.",
     "ReplicaSets maintain a fixed pod count but cannot perform zero-downtime rolling software upgrades.",
     "Declarative rolling updates, ownerReferences, deployment revision history.",
     "kubectl apply -f manifests/deployment.yaml\nkubectl get rs -l app=web-server"),
    (19, "rollouts", "Rollouts",
     "Rollouts incrementally replace old pods with new pods while maintaining capacity.",
     "Deploying a new software version without dropping active user connections or overloading servers.",
     "maxSurge and maxUnavailable algorithms, two-ReplicaSet coordination.",
     "kubectl set image deployment/web-deployment web=nginx:1.27.1-alpine\nkubectl rollout status deployment/web-deployment"),
    (20, "rollback", "Rollback",
     "Rollback reverts the deployment to a previous known-good ReplicaSet specification.",
     "A buggy release was deployed to production and error rates spiked. How do you recover within seconds?",
     "Deployment revision history, annotations, rollout undo.",
     "kubectl rollout history deployment/web-deployment\nkubectl rollout undo deployment/web-deployment"),
    (21, "readiness", "Readiness Probes",
     "Running does not mean ready to serve traffic.",
     "A container process boots in 1 second, but its database connection pool takes 25 seconds to initialize. Traffic sent immediately fails.",
     "Readiness probe feedback, EndpointSlice removal, traffic isolation.",
     "kubectl describe pod demo-pod | grep Readiness"),
    (22, "liveness", "Liveness Probes",
     "A process can be alive in the OS while completely deadlocked internally.",
     "A thread deadlock or memory leak freezes the HTTP loop. The process is alive, so the OS never restarts it.",
     "Liveness probe evaluation, kubelet container restart, restart count increment.",
     "kubectl describe pod demo-pod | grep Liveness"),
    (23, "startup-probes", "Startup Probes",
     "Startup probes protect legacy slow-starting applications from aggressive liveness probes.",
     "A slow-starting application takes 2 minutes to boot. Liveness probes kill it at 30 seconds in an infinite restart loop.",
     "Startup probe gating, disabling liveness/readiness until initial boot succeeds.",
     "kubectl apply -f manifests/startup-probe.yaml"),
    (24, "pod-ips-and-ephemeral-identity", "Pod IPs and Ephemeral Identity",
     "Pods are mortal; their IP addresses change every time they are replaced.",
     "If clients hardcode Pod IP addresses, every rollout, node reboot, or crash permanently severs connectivity.",
     "Ephemeral networking, dynamic IP assignment, IP address churn.",
     "kubectl get pods -o wide\nkubectl delete pod demo-pod\nkubectl get pods -o wide"),
    (25, "service-from-first-principles", "Service From First Principles",
     "A Service is a stable virtual IP and DNS name representing a dynamic set of Pod endpoints.",
     "Decoupling consumers from volatile Pod IP addresses with a permanent front-end identity.",
     "Virtual IPs (VIPs), label selection, Endpoints / EndpointSlices decoupling.",
     "kubectl apply -f manifests/service-clusterip.yaml\nkubectl get endpoints web-service"),
    (26, "clusterip", "ClusterIP",
     "ClusterIP provides internal-only load balancing across pod endpoints.",
     "Internal microservices need reliable communication without exposing ports to the public internet.",
     "Kernel packet translation (DNAT), service CIDR block, internal VIPs.",
     "kubectl get svc web-service -o wide"),
    (27, "kubernetes-dns", "Kubernetes DNS",
     "CoreDNS translates service names into virtual cluster IPs.",
     "Instead of IP addresses, applications connect to stable DNS hostnames like 'payments' or 'postgres'.",
     "CoreDNS, /etc/resolv.conf in Pods, ndots:5 resolution search path.",
     "kubectl exec -it demo-pod -- nslookup web-service"),
    (28, "service-discovery", "Service Discovery",
     "Namespaces determine DNS qualification scope: short name vs FQDN.",
     "Resolving services across different teams and environments without naming collisions.",
     "FQDN structure: <service>.<namespace>.svc.cluster.local.",
     "kubectl exec -it demo-pod -- nslookup web-service.default.svc.cluster.local"),
    (29, "nodeport", "NodePort",
     "NodePort exposes a service on a dedicated port across every worker node's external IP.",
     "Accessing services from outside the cluster before an external load balancer or ingress is configured.",
     "NodePort range (30000-32767), packet forwarding across nodes, kube-proxy routing.",
     "kubectl apply -f manifests/service-nodeport.yaml\ncurl http://127.0.0.1:30080"),
    (30, "loadbalancer-service", "LoadBalancer Service",
     "LoadBalancer provisions an external cloud load balancer directing traffic into NodePorts.",
     "Public internet users need a single public IP routing directly into cluster services.",
     "Cloud Controller Manager, external IP allocation, health checking.",
     "kubectl get svc -A -o wide"),
    (31, "ingress-gateway-concepts", "Ingress and Gateway Concepts",
     "NodePorts and LoadBalancers waste IPs; Ingress provides Layer 7 HTTP routing.",
     "Routing api.example.com and shop.example.com to different internal services using a single public IP.",
     "Layer 7 HTTP reverse proxying, path routing, host routing, Gateway API evolution.",
     "kubectl apply -f manifests/ingress.yaml\nkubectl get ingress"),
    (32, "traffic-path", "Traffic Path",
     "Tracing every packet hop from external browser to the listening container socket.",
     "When an HTTP request fails with 502 or 504, which component dropped the packet?",
     "Hop-by-hop trace: Client -> LB -> Ingress -> Service VIP -> iptables DNAT -> veth -> Container socket.",
     "traceroute / tcpdump / curl diagnostic trace"),
    (33, "k8s-networking-mental-model", "Kubernetes Networking Mental Model",
     "All Pods can communicate with all other Pods on all nodes without NAT.",
     "The fundamental networking invariant of Kubernetes that simplifies distributed system design.",
     "Pod network addressability, flat IP routing, node-to-node overlay/underlay.",
     "ip route / iptables -t nat -L -n -v"),
    (34, "cni-concept", "CNI Concept",
     "Kubernetes specifies the networking requirements; CNI plugins implement them.",
     "How does an IP actually get allocated and assigned to a network namespace when a container starts?",
     "Container Network Interface specification, ADD/DEL verbs, kindnet, Calico, Cilium.",
     "ls -la /etc/cni/net.d/"),
    (35, "network-debugging", "Network Debugging",
     "Systematic isolation of DNS, routing, port binding, and firewall issues.",
     "A service returns 'Connection refused'. Is it DNS, selector mismatch, wrong port, or down pod?",
     "Network triage tree: ping -> nslookup -> curl -> endpoints check -> socket inspection.",
     "kubectl run net-debug --rm -it --image=busybox:1.36 -- sh"),
    (36, "configmap", "ConfigMap",
     "Separate configuration from container images; build once, configure anywhere.",
     "Rebuilding container images just to change an API URL or environment flag is a major anti-pattern.",
     "Decoupled plaintext configuration, env injection, volume directory mounting, atomic updates.",
     "kubectl apply -f manifests/configmap.yaml\nkubectl describe configmap app-config"),
    (37, "secrets", "Secrets",
     "Base64 encoding is not encryption; Secrets provide controlled API access to sensitive data.",
     "Developers commit API tokens and database passwords to Git repositories or plaintext images.",
     "Secret objects, tmpfs memory mounts, RBAC access control, encryption-at-rest semantics.",
     "kubectl apply -f manifests/secret.yaml\nkubectl get secret app-secrets -o yaml"),
    (38, "environment-configuration", "Environment Configuration",
     "Promoting the same image across dev, staging, and production using configuration layers.",
     "Maintaining distinct code branches or images per deployment environment causes configuration drift.",
     "12-Factor App config principle, envFrom, downward API (metadata injection).",
     "kubectl apply -f manifests/env-config.yaml"),
    (39, "volumes", "Volumes",
     "Files written to a container layer are lost forever when the container process restarts.",
     "Applications need temporary scratch space or shared storage across containers in the same Pod.",
     "Pod-level storage abstraction, lifecycle binding, container mount points.",
     "kubectl apply -f manifests/volume-pod.yaml"),
    (40, "emptydir", "emptyDir",
     "emptyDir provides fast scratch storage that lives as long as the Pod.",
     "Sharing assets between a git-sync sidecar and a web application container.",
     "RAM-backed vs disk-backed emptyDir, shared directory mounting.",
     "kubectl apply -f manifests/emptydir-pod.yaml"),
    (41, "persistent-volume-concept", "PersistentVolume Concept",
     "Storage must outlive Pods, nodes, and deployments.",
     "Database state must survive even if its Pod is scheduled onto a completely different node.",
     "PersistentVolume (PV) vs PersistentVolumeClaim (PVC), storage lifecycle decoupling.",
     "kubectl apply -f manifests/pvc.yaml\nkubectl get pvc,pv"),
    (42, "storageclass", "StorageClass",
     "StorageClass enables automated, dynamic volume provisioning on demand.",
     "Cluster administrators cannot manually pre-provision every disk for every developer claim.",
     "Dynamic provisioning, reclaim policies (Delete vs Retain), volume binding modes.",
     "kubectl get storageclass"),
    (43, "stateful-applications", "Stateful Applications",
     "Stateful systems require stable identities, persistent storage, and ordered lifecycles.",
     "Running a clustered database on a stateless Deployment causes split-brain and data corruption.",
     "Stateful distributed systems requirements: identity, consensus, ordered deployment.",
     "kubectl apply -f projects/05-stateful-application/manifests/all-in-one.yaml"),
    (44, "statefulset", "StatefulSet",
     "StatefulSet assigns deterministic ordinal identities and binds dedicated PVCs per replica.",
     "Managing multi-node databases (PostgreSQL, Cassandra, Redis) with predictable hostnames.",
     "Ordinal indexing (app-0, app-1), volumeClaimTemplates, OrderedReady vs Parallel.",
     "kubectl get statefulset\nkubectl get pods -l app=vault"),
    (45, "headless-services", "Headless Services",
     "Headless services return direct pod IP addresses instead of a single virtual IP.",
     "Clustered databases need peer-to-peer gossip discovery without load-balancing intermediaries.",
     "clusterIP: None, DNS SRV and A records for direct pod addressing.",
     "kubectl describe svc datastore-headless"),
    (46, "daemonset", "DaemonSet",
     "A DaemonSet runs exactly one copy of a Pod on every worker node.",
     "Collecting host logs, host metrics, and running CNI routing daemons on every machine.",
     "DaemonSet controller, node scheduling, automatic scaling as nodes join/leave.",
     "kubectl apply -f manifests/daemonset.yaml\nkubectl get pods -l app=node-monitor -o wide"),
    (47, "jobs", "Jobs",
     "Jobs manage batch tasks that must run to successful completion (exit 0) and stop.",
     "Running database schema migrations or batch image processing with a continuous deployment.",
     "Run-to-completion semantics, backoffLimit, completions, parallelism.",
     "kubectl apply -f manifests/job.yaml\nkubectl get jobs"),
    (48, "cronjobs", "CronJobs",
     "CronJobs schedule recurring batch Jobs using standard 5-field cron syntax.",
     "Automating nightly backups, cleanup scripts, and scheduled billing reports.",
     "CronJob controller, concurrencyPolicy (Allow, Forbid, Replace), startingDeadlineSeconds.",
     "kubectl apply -f manifests/cronjob.yaml\nkubectl get cronjob"),
    (49, "namespaces", "Namespaces",
     "Namespaces provide logical scoping and administrative isolation within a shared cluster.",
     "Multiple teams, projects, and environments sharing one physical cluster without naming collisions.",
     "Logical boundaries, resource naming scopes, multi-tenancy limits.",
     "kubectl create namespace staging\nkubectl get namespaces"),
    (50, "resourcequota", "ResourceQuota",
     "ResourceQuota enforces hard aggregate capacity limits on a namespace.",
     "A rogue team schedules 500 pods and exhausts all cluster CPU and memory, starving other teams.",
     "Hard limits on total CPU, Memory, Pod counts, and storage claims per namespace.",
     "kubectl apply -f manifests/quota.yaml\nkubectl describe quota compute-quota"),
    (51, "limitrange", "LimitRange",
     "LimitRange sets default, minimum, and maximum resource constraints on individual containers.",
     "Developers forget to define resource requests, causing unconstrained pods to monopolize nodes.",
     "Container request/limit defaults, max/min validation, ratio enforcement.",
     "kubectl describe limitrange cpu-mem-limits"),
    (52, "rbac-from-first-principles", "RBAC From First Principles",
     "Who (Subject) can do What (Verb) on Which (Resource) Where (Namespace)?",
     "Giving every developer or automated tool full cluster-admin permissions leads to catastrophic accidental deletion.",
     "Role-Based Access Control matrix: Subject -> RoleBinding -> Role (verbs + resources).",
     "kubectl apply -f manifests/rbac.yaml\nkubectl auth can-i create pods --as=system:serviceaccount:default:pod-reader-sa"),
    (53, "serviceaccounts", "ServiceAccounts",
     "ServiceAccounts provide in-cluster workload identities for API communication.",
     "Processes inside Pods need to query the Kubernetes API securely without hardcoded user passwords.",
     "Projected service account tokens, JWT authentication, /var/run/secrets/kubernetes.io/serviceaccount.",
     "kubectl get sa\nkubectl describe sa pod-reader-sa"),
    (54, "admission-control", "Admission Control",
     "Admission webhooks intercept, mutate, and validate API requests before persistence.",
     "Enforcing cluster security policies (e.g. rejecting root containers) before objects enter etcd.",
     "Mutating admission, Validating admission, Pod Security Standards admission.",
     "kubectl get mutatingwebhookconfigurations,validatingwebhookconfigurations"),
    (55, "networkpolicy", "NetworkPolicy",
     "By default, all pods can talk to all pods. NetworkPolicy acts as a pod-level firewall.",
     "A compromised frontend web pod can freely connect to internal database and telemetry ports.",
     "East-west traffic isolation, ingress and egress packet filtering, podSelector rules.",
     "kubectl apply -f manifests/networkpolicy.yaml\nkubectl describe networkpolicy isolate-database"),
    (56, "scheduling-constraints", "Scheduling Constraints",
     "Guiding workload placement with nodeSelector, affinity, and anti-affinity.",
     "Workloads require specific hardware (ARM vs x86, SSD vs HDD, GPU) or physical locality.",
     "nodeSelector, nodeAffinity (required vs preferred), podAffinity, podAntiAffinity.",
     "kubectl apply -f manifests/scheduling-affinity.yaml"),
    (57, "taints-and-tolerations", "Taints and Tolerations",
     "Nodes taint to repel pods; pods tolerate to be scheduled on tainted nodes.",
     "Reserving dedicated nodes for batch processing or GPU workloads without regular pods landing on them.",
     "Taint effects: NoSchedule, PreferNoSchedule, NoExecute; matching tolerations.",
     "kubectl taint nodes k8s-scratch-cluster-worker dedicated=gpu:NoSchedule\nkubectl describe nodes | grep Taints"),
    (58, "topology-spread", "Topology Spread Constraints",
     "Evenly distributing replicas across failure domains (nodes, zones, regions).",
     "All 3 replicas accidentally land on the same physical host; host fails, causing a complete outage.",
     "topologySpreadConstraints, maxSkew, topologyKey (zone, hostname), whenUnsatisfiable.",
     "kubectl apply -f manifests/topology-spread.yaml"),
    (59, "poddisruptionbudget", "PodDisruptionBudget",
     "PDB limits the number of pods concurrently unavailable during voluntary disruptions.",
     "Cluster administrator drains a node for OS upgrades, accidentally evicting all replicas simultaneously.",
     "Voluntary vs involuntary disruptions, minAvailable vs maxUnavailable.",
     "kubectl apply -f manifests/pdb.yaml\nkubectl get pdb"),
    (60, "horizontal-pod-autoscaler", "Horizontal Pod Autoscaler",
     "HPA automatically scales replica counts in response to workload metrics.",
     "Traffic spikes at 9 AM overload fixed replicas, causing latency and request timeouts.",
     "HPA feedback formula: desiredReplicas = ceil[currentReplicas * (currentMetric / targetMetric)].",
     "kubectl apply -f manifests/hpa.yaml\nkubectl get hpa"),
    (61, "metrics-server", "Metrics Server",
     "Metrics Server aggregates container CPU and memory metrics from kubelet Summary APIs.",
     "HPA cannot make autoscaling decisions without real-time CPU/memory utilization telemetry.",
     "Metrics Server architecture, metrics.k8s.io API, kubectl top.",
     "kubectl top nodes\nkubectl top pods"),
    (62, "vertical-scaling-concepts", "Vertical Scaling Concepts",
     "Adjusting CPU and memory requests and limits based on observed historical consumption.",
     "Over-provisioning wastes money; under-provisioning leads to CPU throttling and OOMKilled crashes.",
     "Vertical Pod Autoscaler (VPA) concepts, right-sizing algorithms, in-place pod resize.",
     "kubectl describe pod -l app=web-server | grep Requests -A 5"),
    (63, "cluster-autoscaling-concept", "Cluster Autoscaling Concept",
     "When nodes run out of capacity, Pod autoscaling stalls in Pending until nodes are added.",
     "Pod autoscaling without cluster autoscaling causes pods to queue indefinitely.",
     "Cluster Autoscaler, cloud node pools, pending pod triggers, scale-down eviction.",
     "kubectl describe nodes | grep -A 8 Allocatable"),
    (64, "deployment-strategies", "Deployment Strategies",
     "Comparing RollingUpdate, Recreate, Blue/Green, and Canary rollout strategies.",
     "Deploying breaking changes with the wrong strategy causes downtime or data schema corruption.",
     "RollingUpdate vs Recreate tradeoffs, capacity overhead, database migration coordination.",
     "kubectl explain deployment.spec.strategy"),
    (65, "canary-deployment", "Canary Deployment",
     "Routing a small fraction of real traffic to a new version before full rollout.",
     "Catching critical production bugs on 5% of users rather than impacting 100% of traffic.",
     "Traffic splitting, label weight distribution, error budget evaluation.",
     "kubectl apply -f manifests/canary-deployment.yaml"),
    (66, "graceful-shutdown", "Graceful Shutdown",
     "Allowing in-flight HTTP requests to complete before terminating container processes.",
     "Abruptly terminating containers causes dropped TCP connections and 502 Bad Gateway errors.",
     "SIGTERM signal propagation, terminationGracePeriodSeconds, endpoint deregistration timing.",
     "kubectl apply -f projects/04-background-worker-system/manifests/all-in-one.yaml"),
    (67, "prestop-and-termination-grace", "PreStop and Termination Grace",
     "preStop hooks synchronize application shutdown with iptables endpoint removal.",
     "Race condition: kubelet sends SIGTERM before kube-proxy removes the Pod IP from routing tables.",
     "preStop sleep trick, zero-downtime connection draining, termination sequence.",
     "kubectl apply -f manifests/prestop-hook.yaml"),
    (68, "kubernetes-events", "Kubernetes Events",
     "Events are the chronological black-box recorder of the cluster control plane.",
     "Pod is stuck in Pending or CrashLoopBackOff and logs are empty. Events reveal the root cause.",
     "Event API object, reason, message, source component, sorting events.",
     "kubectl get events --sort-by='.metadata.creationTimestamp'"),
    (69, "logs", "Logs",
     "Container logs capture stdout and stderr streams directly from the runtime.",
     "Diagnosing application startup exceptions, stack traces, and request errors.",
     "kubectl logs, --previous flag for crashed containers, multi-container log inspection.",
     "kubectl logs -l app=web-server --tail=50\nkubectl logs <crashed-pod> --previous"),
    (70, "exec-and-port-forward", "exec and port-forward",
     "Interactive shell inspection and localhost tunneling for developer debugging.",
     "Inspecting files, testing localhost socket bindings, and querying private services.",
     "kubectl exec (TTY/stdin SPDY/WebSocket streams), kubectl port-forward tunnel.",
     "kubectl exec -it demo-pod -- sh\nkubectl port-forward svc/web-service 8080:80"),
    (71, "debugging-workflow", "Debugging Workflow",
     "The systematic 11-step diagnostic sequence from symptom to root cause.",
     "Guessing and randomly restarting pods prolongs outages and masks underlying bugs.",
     "OBJECT -> STATUS -> CONDITIONS -> EVENTS -> OWNER -> POD -> CONTAINER -> LOGS -> NETWORK -> CONFIG -> STORAGE.",
     "cat docs/kubectl-debugging.md"),
    (72, "broken-pod-labs", "Broken Pod Labs",
     "7 deliberate container failures: diagnose ImagePullBackOff, CrashLoop, OOM, and missing configs.",
     "Real-world incident simulation: finding root causes without looking at the solution.",
     "Pod failure patterns, exit code analysis, container status inspection.",
     "kubectl apply -f phases/72-broken-pod-labs/manifests/broken-pods.yaml"),
    (73, "broken-networking-labs", "Broken Networking Labs",
     "6 deliberate networking failures: diagnose selector mismatches, wrong ports, and DNS drops.",
     "Traffic fails to reach healthy pods; diagnosing virtual IP and endpoint discrepancies.",
     "Service selector triage, targetPort alignment, localhost binding traps.",
     "kubectl apply -f phases/73-broken-networking-labs/manifests/broken-networking.yaml"),
    (74, "broken-storage-labs", "Broken Storage Labs",
     "4 deliberate storage failures: diagnose PVC Pending, permission errors, and mount collisions.",
     "Databases fail to boot because storage claims cannot bind or permissions are denied.",
     "PVC/PV binding criteria, fsGroup permissions, ReadWriteOnce node locks.",
     "kubectl apply -f phases/74-broken-storage-labs/manifests/broken-storage.yaml"),
    (75, "control-plane-components", "Control Plane Components",
     "The 4 pillars of the control plane: API Server, Scheduler, Controller Manager, and etcd.",
     "Understanding how the brain coordinates before inspecting individual internals.",
     "Control plane architecture, leader election, control plane network topology.",
     "kubectl get pods -n kube-system"),
    (76, "kube-apiserver", "kube-apiserver",
     "The stateless HTTPS REST brain that validates, authorizes, and persists all declarations.",
     "All communication in Kubernetes goes through the API server; no component talks directly to etcd.",
     "REST handlers, OpenAPI schema generator, etcd storage serializer, admission controllers.",
     "curl -k -H 'Authorization: Bearer ...' https://127.0.0.1:6443/api/v1/nodes"),
    (77, "controller-manager", "Controller Manager",
     "A single binary multiplexing dozens of independent reconciliation loops.",
     "Who creates ReplicaSets? Who deletes pods when a node dies? Who creates Endpoints?",
     "DeploymentController, ReplicaSetController, NodeController, RouteController.",
     "kubectl logs -n kube-system -l component=kube-controller-manager --tail=50"),
    (78, "scheduler-internals", "Scheduler Internals Conceptually",
     "Deep dive into the scheduling queue, filtering predicates, priority scoring, and binding.",
     "How does Kubernetes schedule 1,000 pods per second across 5,000 nodes without lock contention?",
     "Scheduling queue, activeQ, backoffQ, unschedulablePods, scheduling cycle vs binding cycle.",
     "kubectl logs -n kube-system -l component=kube-scheduler --tail=50"),
    (79, "kubelet", "kubelet",
     "The node agent that bridges declarative API manifests with local Linux container runtimes.",
     "The control plane declares a Pod should run on Node A. Kubelet makes it a physical reality.",
     "PLEG (Pod Lifecycle Event Generator), cgroup driver, syncLoop, status reporting.",
     "docker exec -it k8s-scratch-cluster-worker systemctl status kubelet || true"),
    (80, "container-runtime-and-cri", "Container Runtime and CRI",
     "Container Runtime Interface (CRI) decouples Kubernetes from specific container engines.",
     "Why dockershim was removed and how containerd / runc execute containers.",
     "CRI gRPC API (RuntimeService, ImageService), containerd, runc, OCI specification.",
     "docker exec -it k8s-scratch-cluster-worker crictl info"),
    (81, "kube-proxy-service-dataplane", "kube-proxy / Service Dataplane",
     "How virtual ClusterIPs are translated into real Pod IPs inside the Linux kernel.",
     "A Service IP does not have a physical network interface; it exists solely in packet rewrite rules.",
     "iptables NAT tables (PREROUTING, KUBE-SERVICES), IPVS hash tables, eBPF maps.",
     "docker exec -it k8s-scratch-cluster-worker iptables -t nat -L KUBE-SERVICES -n -v"),
    (82, "etcd-failure-and-importance", "etcd Failure and Importance",
     "If etcd loses quorum, existing workloads keep running, but the control plane becomes read-only.",
     "Understanding what fails when etcd dies vs what continues operating.",
     "Raft quorum requirements ($2N+1$), split-brain protection, snapshot backups.",
     "kubectl get pods -n kube-system -l component=etcd"),
    (83, "custom-resources", "Custom Resources",
     "Extending the Kubernetes API with domain-specific schemas using CustomResourceDefinitions.",
     "When built-in Pods and Deployments do not express your high-level business abstractions.",
     "CustomResourceDefinition (CRD), OpenAPI v3 schema validation, custom resource instances.",
     "kubectl apply -f projects/10-custom-controller/manifests/01-crd.yaml\nkubectl get crd"),
    (84, "build-a-tiny-controller", "Build a Tiny Controller",
     "Writing a Python reconciliation loop that watches Custom Resources and creates Deployments.",
     "Understanding that Operators are not magic; they are simple reconciliation loops watching CRDs.",
     "CRD watching, generating child resources, updating custom resource status.",
     "python3 projects/10-custom-controller/code/webapp_controller.py"),
    (85, "operators", "Operators",
     "Packaging human operational domain knowledge into automated software reconcilers.",
     "Automating complex stateful operations: automated failover, backups, and schema upgrades.",
     "Operator pattern formula: CRD + Controller + Operational Domain Logic.",
     "cat projects/10-custom-controller/docs/README.md"),
    (86, "helm-from-first-principles", "Helm From First Principles",
     "Parameterizing manifests with templates and packaging applications as versioned charts.",
     "Managing copy-pasted YAML manifests across 20 microservices and 5 environments is unsustainable.",
     "Charts, values.yaml, Go text/template syntax, releases, Helm release storage in Secrets.",
     "helm version\nhelm template test-chart manifests/"),
    (87, "kustomize", "Kustomize",
     "Template-free configuration customization using declarative overlays.",
     "Customizing base manifests for dev, staging, and prod without template syntax or duplication.",
     "Base and overlays, kustomization.yaml, patches, configMapGenerator.",
     "kubectl kustomize --help"),
    (88, "gitops-concept", "GitOps Concept",
     "Git as the single source of truth; automated reconcilers sync Git to cluster state.",
     "Human operators running kubectl apply from their laptops leads to undocumented configuration drift.",
     "GitOps principles, automated pull synchronization, drift detection (ArgoCD / Flux concepts).",
     "git status"),
    (89, "observability", "Observability",
     "The four pillars of cluster observability: Metrics, Logs, Traces, and Events.",
     "Operating distributed systems blind causes prolonged incident response and MTTR.",
     "Cluster telemetry signals: pod restart spikes, node pressure, API latency, pending queues.",
     "kubectl get events -A"),
    (90, "prometheus", "Prometheus",
     "Pull-based time-series monitoring scraping /metrics HTTP endpoints.",
     "Collecting operational performance metrics from applications, nodes, and control plane actors.",
     "Prometheus metrics formats (Counter, Gauge, Histogram), scrape targets, PromQL queries.",
     "curl -s http://127.0.0.1:49818/metrics | head -n 20 || true"),
    (91, "application-metrics", "Application Metrics",
     "Instrumenting application code to expose throughput, latency, and error rates.",
     "Kubernetes knows if a process is alive; application metrics reveal if it is actually succeeding.",
     "RED method (Rate, Errors, Duration), HTTP request duration histograms, business counters.",
     "curl -s http://localhost:8080/metrics || true"),
    (92, "resource-metrics", "Resource Metrics",
     "Measuring actual CPU and memory utilization to optimize resource requests.",
     "Right-sizing workloads to eliminate cloud waste without risking OOMKilled evictions.",
     "Container cgroup accounting, working set memory vs RSS, CPU throttled periods.",
     "kubectl top pods -A"),
    (93, "alerts", "Alerts",
     "Alerting on symptoms affecting users rather than noisy infrastructure causes.",
     "Alert fatigue: engineers get paged for non-actionable warnings and ignore real outages.",
     "SLO-based alerting, burn rates, alerting on CrashLoopBackOff and unavailable replicas.",
     "cat docs/troubleshooting.md"),
    (94, "security-fundamentals", "Security Fundamentals",
     "Defense in depth across images, identities, networks, API permissions, and runtimes.",
     "Treating Kubernetes as a single trust boundary allows one compromised pod to take over the cluster.",
     "The 4Cs of cloud native security: Cloud, Cluster, Container, Code.",
     "cat docs/mental-models.md"),
    (95, "pod-security", "Pod Security Standards",
     "Enforcing baseline and restricted security standards to prevent host kernel compromises.",
     "Root containers and privileged capabilities allow attackers to escape containers onto worker nodes.",
     "Pod Security Standards (privileged, baseline, restricted), non-root execution, dropping capabilities.",
     "kubectl describe namespace production-tier | grep pod-security"),
    (96, "image-security", "Image Security",
     "Securing the software supply chain: registries, immutable digests, and vulnerability scanning.",
     "Using untrusted base images or latest tags pulls unvetted vulnerabilities and breaking changes.",
     "Image digests (sha256:...), non-root base images, distroless images, minimal attack surface.",
     "docker inspect nginx:1.27-alpine | grep RepoDigests"),
    (97, "resource-security", "Resource Security",
     "Principle of least privilege applied to RBAC, ServiceAccounts, Secrets, and NetworkPolicies.",
     "Default ServiceAccounts having wide API permissions allow container breaches to pivot into control plane takeover.",
     "Least privilege RBAC, automountServiceAccountToken: false, namespace network segmentation.",
     "kubectl get clusterrolebindings"),
    (98, "cluster-upgrades-concept", "Cluster Upgrades Concept",
     "Coordinating control plane and worker node version upgrades with zero workload downtime.",
     "Version skew policies and evicting workloads safely during host kernel updates.",
     "Kubernetes version skew policy (N-3 supported), kubeadm upgrade flow, node drain / cordon.",
     "kubectl get nodes -o wide"),
    (99, "high-availability-control-plane", "High Availability Control Plane",
     "Running multiple API servers behind a load balancer with multi-member etcd consensus.",
     "A single control-plane node failure halts all scheduling, autoscaling, and API deployments.",
     "HA topology: 3-member etcd cluster, active-active API servers, active-standby controllers/schedulers.",
     "kubectl get endpoints -n default kubernetes"),
    (100, "multi-node-failure-lab", "Multi-Node Failure Lab",
     "Killing a worker node and observing eviction, rescheduling, and traffic re-routing.",
     "A physical host experiences power failure; how long until pods are rescheduled on surviving nodes?",
     "node-monitor-grace-period (40s), pod eviction timeout, taint based eviction (node.kubernetes.io/unreachable).",
     "docker stop k8s-scratch-cluster-worker\nkubectl get nodes -w"),
    (101, "application-failure-lab", "Application Failure Lab",
     "Crashing multiple application dependencies and watching controller self-healing.",
     "Cascading failures across microservices when a central cache or authentication service drops.",
     "Dependency retry backoff, circuit breaking, controller pod recreation.",
     "kubectl delete pod -l app=redis"),
    (102, "deployment-failure-lab", "Deployment Failure Lab",
     "Triggering a bad rollout, diagnosing progress deadlines, and executing automated rollback.",
     "Deploying code with an invalid database migration or syntax error during business hours.",
     "ProgressDeadlineExceeded, maxUnavailable surge buffering, instant rollout undo.",
     "kubectl rollout undo deployment/web-deployment"),
    (103, "stateful-failure-lab", "Stateful Failure Lab",
     "Crashing a StatefulSet replica and verifying volume preservation and ordinal integrity.",
     "Database pod crash: verifying that the exact same persistent volume is safely reattached.",
     "OrderedReady reattachment, PVC binding lock, zero data loss verification.",
     "kubectl delete pod vault-1\nkubectl get pods -l app=vault -w"),
    (104, "capacity-planning", "Capacity Planning",
     "Calculating required cluster CPU and memory headroom based on aggregate workload requests.",
     "Scheduling 100 microservices without capacity planning causes sudden cascading scheduling failures.",
     "Capacity formula: Total Nodes = ceil[Sum(Requests) / (NodeAllocatable - Overhead)].",
     "python3 phases/105-bin-packing/01-simulator/code/bin_packing_sim.py"),
    (105, "bin-packing", "Bin Packing & Node Sizing",
     "Evaluating many small nodes vs few large nodes: fragmentation, overhead, and blast radius.",
     "Choosing between 20x 4-core nodes or 2x 40-core nodes for your production infrastructure.",
     "Multidimensional bin-packing algorithms, resource fragmentation, failure blast radius analysis.",
     "python3 phases/105-bin-packing/01-simulator/code/bin_packing_sim.py"),
    (106, "cost-thinking", "Cost Thinking",
     "Understanding cloud cost drivers: unallocated requests, idle nodes, and overprovisioned storage.",
     "Engineering teams setting 4 CPU requests for workloads consuming 100m cost companies millions annually.",
     "Request-to-usage ratio, cost of idle headroom, storage allocation costs.",
     "cat phases/105-bin-packing/01-simulator/code/bin_packing_sim.py"),
    (107, "kubernetes-anti-patterns", "Kubernetes Anti-Patterns",
     "18 catastrophic anti-patterns: giant pods, latest tags, missing probes, and hardcoded IPs.",
     "Cargo-culting patterns that create brittle, unmaintainable, and fragile clusters.",
     "Comprehensive catalog of 18 anti-patterns and their underlying engineering failure modes.",
     "cat phases/107-kubernetes-anti-patterns/docs/en.md"),
    (108, "when-k8s-is-the-wrong-tool", "When Kubernetes Is the Wrong Tool",
     "Recognizing when simpler primitives (Docker Compose, PaaS, VMs, serverless) are superior.",
     "Adopting Kubernetes for a single static website or 2-person team imposes crippling operational overhead.",
     "Complexity budget evaluation, total cost of ownership (TCO), alternative architectures.",
     "cat phases/108-when-k8s-is-the-wrong-tool/docs/en.md"),
    (109, "project-stateless-web-app", "Project: Stateless Web App",
     "Deploying a production-grade stateless web application with probes, config, HPA, and rollout.",
     "Consolidating stateless application delivery primitives into a cohesive architecture.",
     "Stateless architecture, anti-affinity node spreading, HPA auto-scaling.",
     "kubectl apply -f projects/01-stateless-web-app/manifests/"),
    (110, "project-app-plus-redis", "Project: App + Redis",
     "Connecting a web application to a stateful Redis cache with resilient retry logic.",
     "Cross-workload service discovery and surviving cache restarts without cascading failure.",
     "Multi-tier architecture, CoreDNS discovery, service virtual IP routing.",
     "kubectl apply -f projects/02-app-plus-redis/manifests/"),
    (111, "project-app-plus-postgresql", "Project: App + PostgreSQL",
     "Connecting a backend API to PostgreSQL backed by a PersistentVolumeClaim.",
     "Managing relational database state, credentials Secrets, and persistent disk mounting.",
     "Persistent volume mounting, subpath mounts, recreate deployment strategy.",
     "kubectl apply -f projects/03-app-plus-postgresql/manifests/"),
    (112, "project-background-worker-system", "Project: Background Worker System",
     "Asynchronous task workers polling a queue with graceful SIGTERM termination.",
     "Managing background batch consumption without dropping active in-flight jobs during rollouts.",
     "Worker deployment, SIGTERM signal handling, terminationGracePeriodSeconds.",
     "kubectl apply -f projects/04-background-worker-system/manifests/"),
    (113, "project-stateful-application", "Project: Stateful Application",
     "Deploying a 3-node clustered datastore using StatefulSet, headless service, and volume templates.",
     "Providing stable network hostnames and dedicated persistent disks per replica.",
     "StatefulSet ordinals, headless service direct A-records, volumeClaimTemplates.",
     "kubectl apply -f projects/05-stateful-application/manifests/"),
    (114, "project-multi-service-application", "Project: Multi-Service Application",
     "Multi-namespace distributed application with cross-namespace DNS discovery and NetworkPolicies.",
     "Coordinating web, API, cache, and database tiers across organizational namespace boundaries.",
     "Cross-namespace FQDN DNS discovery, multi-tier isolation, service-to-service routing.",
     "kubectl apply -f projects/06-multi-service-application/manifests/"),
    (115, "project-production-like-cluster", "Project: Production-Like Cluster",
     "Hardened multi-node production deployment with PSS restricted, PDB, HPA, and non-root UID.",
     "Synthesizing enterprise security, reliability, and autoscaling into a complete workload.",
     "Pod Security Standards restricted, PodDisruptionBudget, ResourceQuota, non-root user.",
     "kubectl apply -f projects/07-production-like-cluster/manifests/"),
    (116, "failure-day", "Failure Day Drills",
     "Executing the 8 canonical chaos engineering drills and diagnosing with the 11-step playbook.",
     "Validating that you can identify root causes under active production chaos.",
     "Chaos engineering, intentional fault injection, systematic triage, controller observation.",
     "./projects/08-failure-day/scenarios/run_all_drills.sh"),
    (117, "build-mini-kubernetes", "Build Mini Kubernetes",
     "Implementing an educational distributed orchestrator in Python from first principles.",
     "Connecting API Store -> Desired State -> Controller -> Scheduler -> Node Agent -> Process.",
     "Pure Python orchestrator architecture, control loops, node scheduling, agent health monitoring.",
     "python3 projects/09-build-mini-kubernetes/code/mini_k8s.py --test"),
    (118, "write-a-custom-controller", "Write a Custom Controller",
     "Building a custom Kubernetes controller in Python that watches CRDs and reconciles child resources.",
     "Mastering Kubernetes extensibility by writing real operator reconciliation logic.",
     "CustomResourceDefinitions, API watching, child resource reconciliation, declarative operators.",
     "python3 projects/10-custom-controller/code/webapp_controller.py"),
    (119, "kubernetes-in-system-design", "Kubernetes in System Design",
     "Evaluating 8 production system design scenarios: SaaS APIs, workers, streaming, ML inference.",
     "Answering: Why Kubernetes? Why not VMs? Why not serverless? What operational burden do we accept?",
     "Architectural trade-off analysis, workload classification, failure domain modeling.",
     "cat phases/119-kubernetes-in-system-design/docs/en.md"),
    (120, "final-mental-model", "Final Mental Model",
     "The complete trace: from 'kubectl apply' to the Linux kernel socket, and self-healing reconciliation.",
     "Internalizing Kubernetes as an API-driven distributed control system rather than a collection of YAML files.",
     "End-to-end distributed system mental model, reconciliation chain, distributed state machine.",
     "kubectl get all -A")
]

LESSON_DOC_TEMPLATE = """# Lesson {phase_num:02d}: {title}

## Motto
> "{motto}"

## Problem
{problem}

## Prediction
Before executing any commands or applying manifests, predict:
1. What will the client CLI send over the network to the control plane?
2. Which control plane component receives and validates the request?
3. Where is the desired state persisted?
4. Which controller reconciliation loop or node agent notices the difference between desired and observed state?
5. What intermediate conditions and status transitions will occur before the system reaches steady state?

## Why this matters
{first_principles}
Without understanding this primitive, engineers suffer from mysterious outages, unserviceable traffic drops, or accidental cluster-wide cascades.

## First principles
At the fundamental systems level:
- Declarative Desired State ($S_{{desired}}$) is stored in the persistent database.
- Observed Actual State ($S_{{actual}}$) is discovered via kernel telemetry and agent health checks.
- Reconciliation Loop executes: $\\Delta = S_{{desired}} - S_{{actual}}$.
- Action is taken if and only if $\\Delta \\neq 0$.

## Mental model

```text
       DECLARED DESIRED STATE
       (spec in etcd)
             │
             ▼
     CONTROLLER RECONCILER
             │ Observes difference
             ▼
     OBSERVED ACTUAL STATE
     (status in cluster)
             │
             ▼
      REMEDIATION ACTION
```

## Build the idea
Before relying on the Kubernetes abstraction, run the simulated primitive or inspect raw state:
```bash
{build_cmd}
```

## Use Kubernetes
Now apply the declarative Kubernetes API manifest representing this concept:

```bash
# Verify manifest syntax offline
kubectl apply --dry-run=client -f manifests/

# Apply to cluster
kubectl apply -f manifests/
```

## Inspect the objects
Inspect the live API state and conditions:
```bash
kubectl get all -o wide
kubectl describe <resource> <name>
```

## Observe reconciliation
Trace how the controller manager or kubelet acted:
```bash
kubectl get events --sort-by='.metadata.creationTimestamp'
```

## Break it
Inject a realistic failure into the working system:
- Intentionally terminate a component or container process
- Introduce a network or configuration mismatch
- Observe how the control plane reacts

## Debug it
Execute the 11-step diagnostic workflow:
```text
OBJECT -> STATUS -> CONDITIONS -> EVENTS -> OWNER -> POD -> CONTAINER -> LOGS -> NETWORK -> CONFIG -> STORAGE
```

## Recover it
Remediate the failure:
- Observe whether the controller self-heals automatically
- Apply the declarative correction if configuration was invalid

## Modify it
Alter a key parameter in the manifest, predict the delta, and observe the live transition with `kubectl diff` and `kubectl apply`.

## Evidence
Record your commands, verbatim outputs, events, and controller traces in `outputs/evidence-template.md`.

## Questions for mastery
1. What exact component in the control plane or node detects this state change?
2. What guarantee does Kubernetes provide for this abstraction under node failure?
3. What guarantee does Kubernetes NOT provide?

## What Kubernetes guarantees
- Continuous reconciliation toward declared desired state.
- Automated status reporting via `status.conditions`.
- Level-triggered self-healing when cluster state diverges.

## What Kubernetes does NOT guarantee
- Instantaneous zero-second recovery upon physical node hardware death.
- Application-level data consistency without appropriate stateful architecture.
- Prevention of bugs in application code or configuration.

## When to use this
Use this primitive when your architectural requirements match its design guarantees.

## When not to use this
Avoid this primitive when simpler abstractions (single process, raw container, basic systemd service, managed serverless) solve the problem without distributed systems overhead.

## What comes next
Proceed to the next phase in the curriculum roadmap.
"""

def generate_phase(phase_num, slug, title, motto, problem, first_principles, build_cmd):
    phase_dir = f"phases/{phase_num:02d}-{slug}"
    docs_dir = os.path.join(phase_dir, "docs")
    manifests_dir = os.path.join(phase_dir, "manifests")
    code_dir = os.path.join(phase_dir, "code")
    exp_dir = os.path.join(phase_dir, "experiments")
    out_dir = os.path.join(phase_dir, "outputs")

    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(manifests_dir, exist_ok=True)
    os.makedirs(code_dir, exist_ok=True)
    os.makedirs(exp_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    # 1. docs/en.md
    doc_content = LESSON_DOC_TEMPLATE.format(
        phase_num=phase_num,
        title=title,
        motto=motto,
        problem=problem,
        first_principles=first_principles,
        build_cmd=build_cmd
    )
    with open(os.path.join(docs_dir, "en.md"), "w") as f:
        f.write(doc_content)

    # 2. outputs/evidence-template.md
    with open("outputs/evidence-template.md", "r") as f_src:
        ev_template = f_src.read()
    with open(os.path.join(out_dir, "evidence-template.md"), "w") as f_dst:
        f_dst.write(f"# Evidence Log: Phase {phase_num:02d} - {title}\n\n" + ev_template)

    # 3. experiments/run_experiment.sh
    exp_script = f"""#!/usr/bin/env bash
set -euo pipefail

# Experiment runner for Phase {phase_num:02d}: {title}
echo "=========================================================="
echo "  Running Experiment: Phase {phase_num:02d} - {title}"
echo "=========================================================="

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

if [ -d "manifests" ] && [ "$(ls -A manifests 2>/dev/null)" ]; then
    echo "Applying manifests..."
    kubectl apply -f manifests/
    echo "Inspecting state:"
    kubectl get all -o wide
fi

echo ""
echo "Experiment completed. Inspect events and record evidence."
"""
    exp_path = os.path.join(exp_dir, "run_experiment.sh")
    with open(exp_path, "w") as f:
        f.write(exp_script)
    os.chmod(exp_path, 0o755)

def main():
    print(f"Generating all {len(PHASES_META)} curriculum phases...")
    for item in PHASES_META:
        phase_num, slug, title, motto, problem, first_principles, build_cmd = item
        generate_phase(phase_num, slug, title, motto, problem, first_principles, build_cmd)
    print("All 121 phases generated successfully!")

if __name__ == "__main__":
    main()
