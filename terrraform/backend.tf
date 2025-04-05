terraform {
  backend "s3" {
    bucket = "attandance-1"
    key    = "ecs/terraform.tfstate"
    region = "us-east-1"

  }
}