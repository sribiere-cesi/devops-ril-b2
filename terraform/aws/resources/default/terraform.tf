terraform {
  backend "s3" {
    bucket         = "devop-ril-b2-terraform"
    key            = "fr/terraform.tfstate"
    region         = "eu-west-3"
    dynamodb_table = "devop-ril-b2-terraform-locks"
  }
}
