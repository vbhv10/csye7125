## Add terrform outputs here.
output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "public_route_id" {
  value = aws_route.public_route.id
}

output "instance_public_link" {
  value = "https://${var.a_record_name}"
}
