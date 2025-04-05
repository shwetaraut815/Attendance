variable "region" {
  default = "us-east-1"

}


variable "task_count" {
  type    = number
  default = 1


}

# variable "image" {
#     type = string
#     default = "value"

# }                                

# variable "container_port" {
#   type    = number
#   default = 5000

# }

variable "cpu" {
  type    = number
  default = 1024

}

variable "memory" {
  type    = number
  default = 2048

}

# variable "host_port" {
#   type    = number
#   default = 5000

# }

# variable "container_name" {
#     type = string
#     default = "attendance"
  
# }