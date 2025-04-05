data "aws_vpc" "main" {
  default = true

}
data "aws_subnets" "public_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }

#   filter {
#     name   = "tag:Type"
#     values = ["public"]
#   }

#   filter {
#     name   = "tag:ManagedBy"
#     values = ["terraform"]
#   }
}

output "public_subnet_ids" {
  value = data.aws_subnets.public_subnets.ids
}










# data "aws_subnets" "public-subnets" {
#   filter {
#     name = "vpc-id"
#     values = [ data.aws_vpc.main.id ]
#   }

  

#   filter {
#     name   = "tag:ManagedBy"
#     values = ["terraform"]
#   }

 
  

# }

# data "aws_subnet" "private" {
#   vpc_id = data.aws_vpc.main.id

# }