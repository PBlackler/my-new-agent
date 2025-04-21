############################################################
# agent_endpoint.tf — expose your AgentEngine as a /predict
############################################################

############################################################
# agent_endpoint.tf — expose your AgentEngine as a /predict
############################################################

resource "google_vertex_ai_agent_endpoint" "dev_ep" {
  provider     = google-beta
  project      = var.dev_project_id
  location     = var.location
  agent        = "projects/${var.dev_project_id}/locations/${var.location}/reasoningEngines/4588754603918491648"
  display_name = "dev-agent-endpoint"
}

resource "google_vertex_ai_agent_endpoint_deployment" "dev_dep" {
  provider      = google-beta
  project       = var.dev_project_id
  location      = var.location
  endpoint      = google_vertex_ai_agent_endpoint.dev_ep.name
  model         = google_vertex_ai_agent_endpoint.dev_ep.agent
  deployed_name = "dev-deployment"
}

output "dev_endpoint_id" {
  description = "Fully‑qualified name of the AgentEndpoint"
  value       = google_vertex_ai_agent_endpoint.dev_ep.name
}
