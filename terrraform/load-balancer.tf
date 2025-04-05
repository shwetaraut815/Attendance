resource "aws_lb" "red-green" {
  name               = "red"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.kartik_sg.id]
  subnets            = data.aws_subnets.public_subnets.ids

}


resource "aws_lb_target_group" "red-target" {
  name        = "red-target"
  port        = 5000
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.main.id
  target_type = "ip"

   health_check {
    path                = "/"  # Or any health check endpoint your app exposes
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200-399"  # Accept these status codes as healthy
  }

}

resource "aws_lb_listener" "lb-listener" {
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.red-target.arn
  }
  load_balancer_arn = aws_lb.red-green.arn
  port              = 80

  protocol = "HTTP"



}
