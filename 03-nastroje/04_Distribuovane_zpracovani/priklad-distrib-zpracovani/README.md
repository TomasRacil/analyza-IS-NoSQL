# Praktická Ukázka: Distribuované Zpracování - Komunikace Služeb

Tento adresář obsahuje dvě ukázky demonstrující komunikaci mezi službami:
1.  **Pomocí Docker Compose:** Jednoduché škálování a load balancing s Nginx.
2.  **Pomocí Kubernetes:** Manuální škálování Deploymentu a využití Kubernetes Service pro load balancing.

## Ukázka 1: Docker Compose se škálováním a Nginx Load Balancerem

Tato ukázka demonstruje komunikaci mezi dvěma nezávislými službami (`service_a` a `service_b`) spuštěnými v Docker kontejnerech. Ukazuje, jak lze škálovat jednu ze služeb (`service_b`) na více instancí a jak před ně postavit jednoduchý Nginx load balancer pro rozložení zátěže.

### Struktura adresáře (pro Docker Compose)

```
priklad-distrib-zpracovani/
├── README.md (Tento soubor)
├── docker-compose.yml
├── service_a/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── service_b/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py (upraveno pro zpoždění a identifikaci instance)
└── nginx/
    └── nginx.conf
```

### Předpoklady (pro Docker Compose)

* Nainstalovaný Docker a Docker Compose.

### Spuštění (Docker Compose)

1.  Otevřete terminál.
2.  Přejděte do adresáře `analyza-IS-NoSQL/03-nastroje/04_Distribuovane_zpracovani/priklad-distrib-zpracovani/`.
3.  Spusťte služby. Můžete škálovat `service_b` na požadovaný počet instancí (např. 3):
    ```bash
    docker-compose up --build --scale service_b=3 -d
    ```
Služby by nyní měly běžet:
* `service_a` je dostupná na portu `5001` hostitelského systému.
* `nginx_lb` (load balancer pro `service_b`) je dostupný na portu `5050` hostitelského systému.

### Testování (Docker Compose)

1.  **Ověřte `service_b` přes Nginx:**
    ```bash
    curl http://localhost:5050/data
    ```
    Při opakovaném volání byste měli v odpovědi vidět různá `processed_by_pod` (pokud je `service_b` upravena, aby vracela hostname kontejneru) nebo alespoň v logách Nginx a `service_b` vidět distribuci.

2.  **Zavolejte `service_a`:**
    ```bash
    curl http://localhost:5001/call_service_b
    ```
    Odpověď by měla obsahovat data ze `service_b`, zpracovaná jednou z instancí.

### Zastavení (Docker Compose)
```bash
docker-compose down
```

---

## Ukázka 2: Kubernetes - Manuální Škálování

Tato ukázka demonstruje nasazení a manuální škálování služeb `service_a` a `service_b` v Kubernetes.

### Struktura adresáře (pro Kubernetes)

```
priklad-distrib-zpracovani/
└── kubernetes/
    ├── service_a-deployment.yaml
    ├── service_a-service.yaml
    ├── service_b-deployment.yaml
    └── service_b-service.yaml
```
(Soubory `service_a/app.py`, `service_b/app.py` a jejich `Dockerfile` a `requirements.txt` jsou stejné jako pro Docker Compose ukázku. `service_b/app.py` by měla být upravena pro zpoždění a identifikaci podu.)

### Předpoklady (pro Kubernetes)

* Funkční Kubernetes cluster (Minikube, Kind, Docker Desktop Kubernetes, atd.).
* `kubectl` nakonfigurovaný pro přístup k vašemu clusteru.
* Docker image `service-a-distrib:latest` a `service-b-distrib:latest` sestavené a dostupné vašemu Kubernetes clusteru.
    * Pro Minikube: `eval $(minikube -p minikube docker-env)` a pak `docker build -t service-a-distrib:latest ./service_a/` (a podobně pro service-b).
    * Nebo nahrajte image do registru.
    * V YAML souborech je `imagePullPolicy: IfNotPresent` (nebo `Never`) vhodné pro lokální image.

### Nasazení do Kubernetes

1.  **Přejděte do adresáře s YAML soubory:**
    ```bash
    cd analyza-IS-NoSQL/03-nastroje/04_Distribuovane_zpracovani/priklad_distrib_zpracovani/kubernetes/
    ```

2.  **Aplikujte Kubernetes manifesty:**
    ```bash
    kubectl apply -f service_b-deployment.yaml
    kubectl apply -f service_b-service.yaml
    kubectl apply -f service_a-deployment.yaml
    kubectl apply -f service_a-service.yaml
    ```

3.  **Ověřte stav podů a služeb:**
    ```bash
    kubectl get pods -l app=service-b
    kubectl get pods -l app=service-a
    kubectl get services
    ```
    Měli byste vidět běžící pody a vytvořené služby.

### Testování (Kubernetes)


**Pomocí `kubectl port-forward`**

1.  **Spusťte port-forwarding v novém terminálu:**
    Tím se vytvoří tunel z vašeho lokálního portu (např. `5001`) na port služby `service-a-svc` uvnitř clusteru.
    ```bash
    kubectl port-forward service/service-a-svc 5001:5001
    ```
    Nechte tento terminál běžet.

2.  **Zavolejte `service_a` přes `localhost`:**
    V jiném terminálu:
    ```bash
    curl http://localhost:5001/call_service_b
    ```
    Měli byste vidět odpověď obsahující data ze `service_b`, včetně `processed_by_pod`, což by měl být název jednoho z podů `service-b`.

### Manuální Škálování `service_b` v Kubernetes

1.  **Zvyšte počet replik `service_b` (např. na 3):**
    ```bash
    kubectl scale deployment service-b-deployment --replicas=3
    ```

2.  **Ověřte, že běží více podů:**
    ```bash
    kubectl get pods -l app=service-b -o wide
    ```
    Měli byste vidět 3 pody pro `service-b`, každý s unikátní IP adresou a běžící na (potenciálně) různých uzlech.

3.  **Opakovaně testujte volání `service_a`:**
    Použijte stejnou metodu jako předtím (NodePort nebo port-forward) k volání `http://<URL_SERVICE_A>/call_service_b` několikrát za sebou.
    ```bash
    # Příklad s port-forward běžícím na localhost:5001
    for i in {1..10}; do curl http://localhost:5001/call_service_b; echo ""; sleep 0.5; done
    ```
    Sledujte pole `processed_by_pod` v odpovědích. Měli byste vidět, že se názvy podů střídají, což demonstruje, že Kubernetes Service (`service-b-svc`) provádí load balancing mezi dostupnými replikami `service_b`. Díky umělému zpoždění ve `service_b` je efekt lépe viditelný.

4.  **Snížení počtu replik (volitelné):**
    ```bash
    kubectl scale deployment service-b-deployment --replicas=1
    ```

### Vyčištění (Kubernetes)

Pro odstranění všech vytvořených Kubernetes zdrojů:
```bash
kubectl delete service service-a-svc
kubectl delete deployment service-a-deployment
kubectl delete service service-b-svc
kubectl delete deployment service-b-deployment
# Nebo rychleji, pokud jste v adresáři s YAML soubory:
# kubectl delete -f .
```

## Diskuse o Adaptivním Škálování

Zatímco tento příklad ukazuje manuální škálování, plně **adaptivní (automatické) škálování** v Kubernetes se typicky realizuje pomocí **Horizontal Pod Autoscaler (HPA)**. HPA automaticky upravuje počet podů v Deploymentu nebo ReplicaSetu na základě sledovaných metrik, jako jsou:

* Využití CPU
* Využití paměti
* Vlastní metriky (např. počet zpráv ve frontě, počet aktivních uživatelů, délka fronty požadavků na aplikaci).

Pro škálování na základě délky fronty požadavků by bylo potřeba:
1.  **Exportovat metriku:** Vaše aplikace (`service_b`) by musela nějakým způsobem vystavovat metriku o délce své interní fronty požadavků.
2.  **Metrics Server:** V clusteru musí běžet Metrics Server.
3.  **Custom Metrics Adapter/API:** Pro vlastní metriky by byl potřeba adaptér (např. Prometheus Adapter).
4.  **Konfigurace HPA:** Vytvořili byste HPA objekt cílící na `service-b-deployment`.