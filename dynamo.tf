data "terraform_remote_state" "network" {
  backend = "atlas"

  config {
    name = "${var.org}/${var.workspace_name}"
  }
}

provider "aws" {
  region = "${data.terraform_remote_state.network.region}"
}


variable "environment"{
   type = "string"
  }

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "jlinn-demo-CustomerData"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "UserId"
  range_key      = "customerId"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "customerId"
    type = "S"
  }


  tags = {
  }
}
