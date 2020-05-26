data "aws_security_group" "default" {
  vpc_id = var.vpc_id
  name   = "default"
}
