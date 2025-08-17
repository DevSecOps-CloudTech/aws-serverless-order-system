# AWS Serverless Order System  

[![AWS](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/lambda/)  
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue?logo=githubactions&logoColor=white)](https://github.com/features/actions)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  

A fully serverless **Order Management System** built on AWS.  
This project demonstrates **event-driven microservices** with AWS Lambda, DynamoDB, API Gateway, and S3, designed for scalability, cost-effectiveness, and real-world business use cases.  

---

## 🚀 Features
- **Order Processing** – Create and manage orders.  
- **Inventory Management** – Track and update stock.  
- **Payment Handling** – Process transactions securely.  
- **Shipping Workflow** – Manage shipping and delivery updates.  
- **Infrastructure as Code (IaC)** – Deployable with AWS CloudFormation.  

---

## 📐 Architecture
The system follows an **event-driven serverless design**:  

![AWS Serverless Architecture](docs/architecture-diagram.png)  
*(Replace with your uploaded PNG — put it in a `/docs` folder)*  

**Main Components:**
- `orders_handler.py` → Manages orders  
- `inventory_handler.py` → Tracks inventory  
- `payments_handler.py` → Handles payments  
- `shipping_handler.py` → Processes shipping updates  
- `inventory_seed.py` → Seeds DynamoDB with sample data  
- `aws-composer-complex-architecture.yaml` → CloudFormation template  

---

## 🛠️ Prerequisites
- [AWS CLI](https://docs.aws.amazon.com/cli/) configured with appropriate IAM permissions  
- [Python 3.9+](https://www.python.org/)  
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli.html) *(optional for local testing)*  

---

## ⚡ Deployment

### 1. Clone the repository
```bash
git clone https://github.com/DevSecOps-CloudTech/aws-serverless-order-system.git
cd aws-serverless-order-system

