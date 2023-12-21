resource "google_container_cluster" "primary" {
  name     = "webapp-gke"
  location = var.region
  project  = var.project_id

  remove_default_node_pool = true
  initial_node_count       = 1 #So that we delete the default node pool

  network    = google_compute_network.gke_vpcnetwork.id
  subnetwork = google_compute_subnetwork.gke_subnet.id
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block = "0.0.0.0/0"
    }
  }

  deletion_protection = false

  resource_labels = {
    name = "webapp_cluster"
  }
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  network_policy {
    enabled  = true
    provider = "CALICO"
  }
}

resource "google_container_node_pool" "primary_nodes" {
  name           = "cosmos-mds-primary-node-pool"
  location       = var.region
  cluster        = google_container_cluster.primary.name
  node_locations = var.node_locations
  project        = var.project_id
  node_config {
    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/devstorage.full_control"
    ]

    labels = {
      "name" : "webapp_node_pool"
    }
    image_type = "COS_CONTAINERD"

    preemptible = true
    metadata = {
      disable-legacy-endpoints = "true"
    }
    workload_metadata_config {
      mode = "GKE_METADATA"
    }
    disk_size_gb = var.node_disk_size
    machine_type = var.gke_machine_type
    tags         = ["gke-node"]
  }
  autoscaling {
    total_min_node_count = var.total_min_node_count
    total_max_node_count = var.total_max_node_count
    location_policy      = "BALANCED"
  }
}