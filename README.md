# Movie Recommendation Final Project

Welcome to the Movie Recommendation Final Project! This project involves creating a simple web service using Docker and Kubernetes to display movie recommendations. The goals of this project include understanding Docker and Kubernetes, creating a containerized web application, and deploying it on a Kubernetes cluster.

## Table of Contents

- [Introduction](#introduction)
- [Project Goals](#project-goals)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Dataset](#dataset)

## Introduction

This project utilizes the MovieLens dataset to provide movie recommendations. The web service is containerized using Docker and deployed on a Kubernetes cluster set up on an AWS server.

## Project Goals

1. Understand Docker and Kubernetes.
2. Create a containerized web application.
3. Deploy the application on a Kubernetes cluster.
4. Utilize the MovieLens dataset for movie recommendations.

## Technologies Used

- Docker
- Kubernetes
- AWS
- Python
- Flask (for the web service)
- MovieLens dataset
- Web Scraping for more recent movies on Wikipedia

## Setup Instructions

### Prerequisites

- Docker installed on your local machine.
- Kubernetes cluster set up (preferably on AWS).
- Git installed on your local machine.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/sc4311/Movie-recommendation-Final-Project.git
   cd Movie-recommendation-Final-Project
2. **Build Docker Image**
   ```bash
   docker build -t movie-recommendation-app .
3. **Push Docker Image to a Container Registry**
   Make sure you have a container registry set up (e.g., Docker Hub, AWS ECR).
   ```bash
   docker tag movie-recommendation-app:latest <your_container_registry>/movie-recommendation-app:latest
   docker push <your_container_registry>/movie-recommendation-app:latest
4. **Deploy on Kubernetes**
   Ensure your Kubernetes cluster is up and running. Then apply the Kubernetes deployment and service configurations.
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   
  ## Usage
  Once the application is deployed, you can access it via the service's external IP. The web interface will allow you to get movie recommendations based on the MovieLens dataset.
  
  ## Dataset
  The project uses the MovieLens dataset for providing movie recommendations. The dataset should be downloaded and placed in the appropriate directory specified in the application.
