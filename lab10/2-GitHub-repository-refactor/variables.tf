variable "github_token" {
  type      = string
  sensitive = true
}

variable "repository_name" {
  type    = string
  default = "terraform-managed-repo"
}

variable "repository_description" {
  type    = string
  default = "Repository managed by Terraform"
}

variable "publicly_visible" {
  type    = bool
  default = false
}