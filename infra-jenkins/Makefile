SHELL := /bin/zsh

init: 
	cd terraform && terraform init -upgrade

fmt: init
	cd terraform && terraform fmt

plan: init fmt
	cd terraform && terraform plan

apply: init fmt
	cd terraform && terraform apply

destroy:
	cd terraform && terraform destroy

planvar: init fmt
	cd terraform && terraform plan -var-file=terraform.tfvars

applyvar: init fmt
	cd terraform && terraform apply -var-file=terraform.tfvars

destroyvar:
	cd terraform && terraform destroy -var-file=terraform.tfvars