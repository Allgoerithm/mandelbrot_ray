# network
gcloud compute networks create ray-network --project=<your-project-id> --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional 
# subnetwork
gcloud compute networks subnets create ray-subnet-europe-west1 --project=<your-project-id> --range=10.10.10.0/24 --network=ray-network --region=europe-west1
gcloud compute --project=<your-project-id> firewall-rules create ray-network-allow-internal-egress --direction=EGRESS --priority=1000 --network=ray-network --action=ALLOW --rules=tcp:0-65535,udp:0-65535 --destination-ranges=10.10.10.0/24
gcloud compute --project=<your-project-id> firewall-rules create ray-network-allow-internal-ingress --direction=INGRESS --priority=1000 --network=ray-network --action=ALLOW --rules=tcp:0-65535,udp:0-65535 --source-ranges=10.10.10.0/24
gcloud compute --project=<your-project-id> firewall-rules create ray-dashboard --direction=INGRESS --priority=1000 --network=ray-network --action=ALLOW --rules=tcp:8265 --source-ranges=0.0.0.0/0
gcloud compute --project=<your-project-id> firewall-rules create ray-network-allow-ssh-ingress-from-iap --direction=INGRESS --priority=1000 --network=ray-network --action=ALLOW --rules=tcp:22,udp:3389 --source-ranges=35.235.240.0/20
# firewall rules
gcloud compute --project=<your-project-id> firewall-rules create ray-network-allow-internal-egress --direction=EGRESS --priority=1000 --network=ray-network --action=ALLOW --rules=tcp:0-65535,udp:0-65535 --destination-ranges=10.10.10.0/24
gcloud compute --project=<your-project-id> firewall-rules create ray-network-allow-internal-ingress --direction=INGRESS --priority=1000 --network=ray-network --action=ALLOW --rules=tcp:0-65535,udp:0-65535 --source-ranges=10.10.10.0/24
gcloud compute --project=<your-project-id> firewall-rules create ray-dashboard --direction=INGRESS --priority=1000 --network=ray-network --action=ALLOW --rules=tcp:8265 --source-ranges=0.0.0.0/0
gcloud compute --project=<your-project-id> firewall-rules create ray-network-allow-ssh-ingress-from-iap --direction=INGRESS --priority=1000 --network=ray-network --action=ALLOW --rules=tcp:22,udp:3389 --source-ranges=35.235.240.0/20
