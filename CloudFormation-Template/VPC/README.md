# AWS CloudFormation Template: VPC with Public and Private Subnets

This CloudFormation template provisions a **Virtual Private Cloud (VPC)** with multiple **public and private subnets**, an **internet gateway**, and a **public route table**. It’s designed to establish a foundational network setup suitable for most AWS deployments.


## Features

- **VPC**
  - CIDR block: `10.0.0.0/16`
  - DNS hostnames and support enabled
- **Subnets**
  - 2 public subnets across 2 Availability Zones
  - 6 private subnets across 2 Availability Zones
- **Internet Gateway**
  - Attached to the VPC
- **Routing**
  - Public subnets are associated with a public route table for internet access
  - Private subnets do not map public IPs


## File Structure

```bash
.
├── My-VPC.yml              # CloudFormation template
└── README.md               # Project documentation (this file)

