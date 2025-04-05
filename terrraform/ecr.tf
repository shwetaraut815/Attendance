data "aws_ecr_repository" "attendance-app" {
  name = "attendance-app"

}

data "aws_ecr_image" "latest" {
  repository_name = data.aws_ecr_repository.attendance-app.name
  most_recent     = true

}