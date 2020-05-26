module "global" {
  source                        = "../../modules/global"
  vpc_id                        = aws_vpc.vpc.id
  availability_zone             = var.availability_zone
  cidr_block                    = cidrsubnet(var.cidr_block, 8, 1)
  complete_cidr_block           = var.cidr_block
  ami                           = var.ami
  key_name                      = var.key_name
}

