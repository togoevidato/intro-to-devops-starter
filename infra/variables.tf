variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "project_name" {
  type    = string
  default = "fruitapi"
}

variable "container_image" {
  type = string
}

variable "allowed_cidr" {
  type        = string
  description = "Your public IP CIDR, for example 1.2.3.4/32"
}

variable "db_name" {
  type    = string
  default = "fruitapi"
}

variable "db_user" {
  type    = string
  default = "fruitapi"
}

variable "db_password" {
  type      = string
  sensitive = true
}