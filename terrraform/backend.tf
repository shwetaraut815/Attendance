terraform {
  backend "s3" {
    bucket = "attandance-12"
    key    = "ecs/terraform.tfstate"
    region = "us-east-1"

  }
}
