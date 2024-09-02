# CTVA_weather_data
- Step to start, test and remove the service (expecting the docker is configured )
   - docker-compose up # For building and starting the services.
   - (Optional) Make an GET API call to /load to load data into database # Can make this much more dynamic and realistic.
   - Can make use of testing.py # To load the data into db, test all scenarios and to ensure API behaves as expected. Also for checking the server status
   - docker-compose down --rmi all -v # To Stop all Docker containers and images

## Best Practices
   - To make dynamic entries from s3/gitrepo in reality, I follow the udpates through API call, So added '/load' to update the data into db. For better dynamic updation I tried a different method/logic but with the given time frame unable to add
   - Health check, its a good practice to have a 'health'/'health_check' GET API call, so that to monitor the status of application will be easy and also can be used for real time monitoring.
   - Having good structured code maintaing all configs seperately in independent file handling different ENVs.
   - Maintain neat and ordered code with comments and Docs (I added for many but missed due to limited time for me): Recommended black to make code neat and ordered.

### Deployment Strategy

#### 1. **Database: Amazon RDS (PostgreSQL)**
   - Start with medium instance for a balance between cost and performance.
   - Enable automated backups and configure backup retention policies. Set up regular snapshots for point-in-time recovery.
   - Use AWS Security Groups to restrict access to the database only from your application instances. Enable encryption at rest using AWS KMS and encrypt data in transit using SSL.
#### 2. **API: Flask App Deployment**
   - Dockerize the Flask application to ensure consistency across environments. This involves creating a `Dockerfile` to define the environment in which the application will run.
#### 3. **Pushing Docker Image to Amazon ECR**
   - Create a new ECR repository to store your Docker images.
   - Build your Docker image with a version tag:
   - Tag your image to match your ECR repository URI:
   - Push your Docker image to the ECR repository
#### 4. **Deploying to Amazon ECS with Fargate**
   - Create a new ECS cluster 
   - Create a new task definition in ECS.
   - Task definition includes specifying 
     - The Docker image URL from ECR
     - Container name
     - CPU and memory requirements
     - Environment variables and networking details.
   - Set up an ECS service that uses your task definition. 
      - This service manages the deployment, scaling, and availability of your containers.
   - Deploy the ECS service into a VPC (Virtual Private Cloud)
#### 5. **Data Ingestion:**
   - For more complex ingestion processes that require higher memory or processing power, deploy a dedicated EC2 instance. 
   - Use CloudWatch Events to schedule cron jobs that run the ingestion script. 
#### 6. **Load Balancing:**
   - Integrate the ECS service with an AWS Application Load Balancer (ALB) 
   - Can also Create mediater ALB app between user and application which uses NGINIX or some other to distribute incoming traffic.
   - Configure health checks on the ALB to monitor the health of your Flask application instances.
#### 7. **CI/CD Pipeline:**
   - Use GitHub for source code version control.
   - Can use jenkins to monitor and for Continous Integration
   - Incorporate unit tests, integration tests, and end-to-end tests into the CI/CD pipeline to ensure code quality and application stability. 
   - Use AWS Secrets Manager or AWS Systems Manager Parameter Store to securely manage sensitive configuration values such as database credentials, API keys, and other environment-specific settings.
#### 8. **Logging and Monitoring:**
   - Can use datadog/watchdog to monitor the logs and for logging
#### 9. **Security Best Practices:**
   - Define least-privilege IAM roles for your application instances to restrict access to only the resources they need.
   - Ensure all sensitive data is encrypted in transit using HTTPS and SSL/TLS. Use AWS KMS to manage encryption keys for data at rest.
   - Integrate a vulnerability scanner into your CI/CD pipeline to detect and remediate security issues early.
#### 10. **Backup and Disaster Recovery:**
   - Ensure automated backups are configured for the RDS PostgreSQL database. Set a retention policy that meets your recovery point objectives (RPO).
   - Develop a disaster recovery plan that includes regular testing of backups and failover processes to ensure quick recovery in case of a disaster.

### Conclusion: 
   - By Following the strategy of push Docker images to ECR and deploy them to ECS, along with the existing deployment strategies, you can achieve a highly scalable, secure, and automated deployment process for this Flask application.

# Recomendations:
## FastAPI
   - I have used Flask here as requested in the assignment; otherwise, I would use FastAPI.
   due to Performance,Type Checking,Automatic Docs and supports Asynchronous.
