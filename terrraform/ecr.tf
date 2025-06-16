data "aws_ecr_repository" "attendance {
  name = "attendance"

}

data "aws_ecr_image" "latest" {
  repository_name = data.aws_ecr_repository.attendance.name
  most_recent     = true

}
