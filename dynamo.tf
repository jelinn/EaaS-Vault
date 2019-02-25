
provider "aws" {
  region = "us-east-2"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "jlinn-demo-CustomerData"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "UserId"
  
  attribute {
    name = "UserId"
    type = "S"
  }
}
