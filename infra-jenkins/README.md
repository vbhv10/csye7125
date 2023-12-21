# Terraform Configuration for Creating an AWS Infrastructure for Jenkins

This Terraform configuration file sets up a infrastructure in AWS with the following networking resources:

- 1 public subnets
- An Internet Gateway resource attached to the VPC
- A public route table with public subnet attached to it
- A public route in the public route table with the destination CIDR block 0.0.0.0/0 and the internet gateway created above as the target
- ec2 instance
- `aws_eip_association` to associate Elastic IP with EC2 instance
- Security group to define inbound and outbound rules


## Prerequisites

- An AWS account and access keys with permissions to create VPCs and related resources.
- Terraform installed on your local machine.
- AWS CLI installed on your local machine.

## Configuration

- Clone the repository to your local machine.
- In the command line, navigate to the directory where the main.tf file is located.
- add your creds json file path in terraform.tfvars 
- create terraform.tfvars file and set the following variables.
   1. profile
   2. public_subnet_cidr
   3. vpc_cidr_block
   4. region
   5. instance_type
   6. a_record_name
   7. loadbalancer_ip
   8. gateway_host
   
- Run the terraform init command to initialize the Terraform configuration file.
```shell
      make init
```
      
- Run the terraform plan command to see a preview of the resources that will be created.
```shell
      make plan
```
      
- Run the terraform apply command to create the resources.
```shell
      make apply
```
      
- After you are finished, run the terraform destroy command to delete the resources.
```shell
      make destroy
```

## Conclusion

This Terraform configuration file provides an easy and repeatable way to create a VPC with networking resources in AWS. By using this configuration file, you can create multiple VPCs with the same resources in the same AWS account and region.
