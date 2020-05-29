resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.vpc.id

  ingress {
    self      = true
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  ingress {
    self      = true
    from_port = 8080
    to_port   = 8080
    protocol  = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
  ingress {
    self      = true
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }


  egress {
    self      = true
    from_port = 0
    to_port   = 0
    protocol  = -1

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  egress {
    description = "NTP"
    from_port   = 123
    to_port     = 123
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

