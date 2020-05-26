resource "aws_instance" "sbayon" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }

  tags = {
    Name              = "sbayon"
    Env              = "global"
  }
}
output "sbayon_dns" {
  value = aws_instance.sbayon.public_dns
}
output "sbayon_ip" {
  value = aws_instance.sbayon.public_ip
}
resource "aws_instance" "lborel" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "lborel"
    Env              = "global"
  }
}

output "lborel_dns" {
  value = aws_instance.lborel.public_dns
}
output "lborel_ip" {
  value = aws_instance.lborel.public_ip
}
resource "aws_instance" "jboully" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "jboully"
    Env              = "global"
  }
}
output "jboully_dns" {
  value = aws_instance.jboully.public_dns
}
output "jboully_ip" {
  value = aws_instance.jboully.public_ip
}
resource "aws_instance" "rchevallier" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "rchevallier"
    Env              = "global"
  }
}
output "rchevallier_dns" {
  value = aws_instance.rchevallier.public_dns
}
output "rchevallier_ip" {
  value = aws_instance.rchevallier.public_ip
}
resource "aws_instance" "qcordiero" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "qcordiero"
    Env              = "global"
  }
}
output "qcordiero_dns" {
  value = aws_instance.qcordiero.public_dns
}
output "qcordiero_ip" {
  value = aws_instance.qcordiero.public_ip
}
resource "aws_instance" "rcouturier" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "rcouturier"
    Env              = "global"
  }
}
output "rcouturier_dns" {
  value = aws_instance.rcouturier.public_dns
}
output "rcouturier_ip" {
  value = aws_instance.rcouturier.public_ip
}
resource "aws_instance" "kdossantos" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "kdossantos"
    Env              = "global"
  }
}
output "kdossantos_dns" {
  value = aws_instance.kdossantos.public_dns
}
output "kdossantos_ip" {
  value = aws_instance.kdossantos.public_ip
}
resource "aws_instance" "jferreira" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "jferreira"
    Env              = "global"
  }
}

output "jferreira_dns" {
  value = aws_instance.jferreira.public_dns
}
output "jferreira_ip" {
  value = aws_instance.jferreira.public_ip
}
resource "aws_instance" "afigueiredo" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "afigueiredo"
    Env              = "global"
  }
}
output "afigueiredo_dns" {
  value = aws_instance.afigueiredo.public_dns
}
output "afigueiredo_ip" {
  value = aws_instance.afigueiredo.public_ip
}
resource "aws_instance" "dheliot" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "dheliot"
    Env              = "global"
  }
}
output "dheliot_dns" {
  value = aws_instance.dheliot.public_dns
}
output "dheliot_ip" {
  value = aws_instance.dheliot.public_ip
}
resource "aws_instance" "fladouce" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "fladouce"
    Env              = "global"
  }
}
output "fladouce_dns" {
  value = aws_instance.fladouce.public_dns
}
output "fladouce_ip" {
  value = aws_instance.fladouce.public_ip
}
resource "aws_instance" "glefebvre" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "glefebvre"
    Env              = "global"
  }
}
output "glefebvre_dns" {
  value = aws_instance.glefebvre.public_dns
}
output "glefebvre_ip" {
  value = aws_instance.glefebvre.public_ip
}
resource "aws_instance" "amorin" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "amorin"
    Env              = "global"
  }
}
output "amorin_dns" {
  value = aws_instance.amorin.public_dns
}
output "amorin_ip" {
  value = aws_instance.amorin.public_ip
}
resource "aws_instance" "npereira" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "npereira"
    Env              = "global"
  }
}
output "npereira_dns" {
  value = aws_instance.npereira.public_dns
}
output "npereira_ip" {
  value = aws_instance.npereira.public_ip
}
resource "aws_instance" "jrakic" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "jrakic"
    Env              = "global"
  }
}
output "jrakic_dns" {
  value = aws_instance.jrakic.public_dns
}
output "jrakic_ip" {
  value = aws_instance.jrakic.public_ip
}
resource "aws_instance" "ytata" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "ytata"
    Env              = "global"
  }
}
output "ytata_dns" {
  value = aws_instance.ytata.public_dns
}
output "ytata_ip" {
  value = aws_instance.ytata.public_ip
}
resource "aws_instance" "athazet" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "athazet"
    Env              = "global"
  }
}
output "athazet_dns" {
  value = aws_instance.athazet.public_dns
}
output "athazet_ip" {
  value = aws_instance.athazet.public_ip
}
resource "aws_instance" "svallet" {
  ami                     = var.ami
  instance_type           = "t2.micro"
  key_name                = var.key_name
  subnet_id               = aws_subnet.subnet.id

  root_block_device {
    volume_size           = "8"
  }

  vpc_security_group_ids = [
    data.aws_security_group.default.id,
  ]

  lifecycle {
    ignore_changes = [
      ami,
    ]
  }


  tags = {
    Name              = "svallet"
    Env              = "global"
  }
}
output "svallet_dns" {
  value = aws_instance.svallet.public_dns
}
output "svallet_ip" {
  value = aws_instance.svallet.public_ip
}