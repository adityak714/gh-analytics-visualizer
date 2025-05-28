# Project Overview

This project is designed to analyze GitHub repositories using distributed systems and containerized environments. It fetches repositories, processes data, and answers specific questions related to repository statistics, such as the most popular languages used in repositories with unit tests and CI/CD configurations, and the repositories with the highest number of commits.

## Workspace Structure

The workspace is organized into three virtual machines (VMs), each with specific roles:

### VM1
- **Purpose**: Fetch repositories from GitHub and send them to Pulsar for processing.
- **Key Files**:
  - `run_ray.py`: Fetches repositories using Ray for distributed processing.
  - `run.py`: Sequentially fetches repositories and sends them to Pulsar.
  - `producer.py`: Sends repository data to Pulsar topics.
  - `count_languages.py`: Counts the occurrence of programming languages in repositories.
  - `Github_API_fetch.py`: Fetches repositories from GitHub API.
  - `Dockerfile`: Containerizes the VM1 functionality.

### VM2
- **Purpose**: Processes repository data to determine the repositories with the highest number of commits.
- **Key Files**:
  - `get_number_of_commits.py`: Fetches the number of commits for each repository.
  - `Q2.py`: Consumes repository data from Pulsar and answers the question about the most committed repositories.
  - `Dockerfile`: Containerizes the VM2 functionality.

### VM3
- **Purpose**: Analyzes repositories for unit tests and CI/CD configurations.
- **Key Files**:
  - `test_driven_development_analysis.py`: Checks repositories for test files and CI/CD configurations.
  - `Q3_Q4.py`: Consumes repository data from Pulsar and answers questions about popular languages in repositories with tests and CI/CD.
  - `Dockerfile`: Containerizes the VM3 functionality.

## Configuration Files

- `docker-compose.yaml`: Defines the services and their dependencies for the project.
- `dockerize.yml`: Sets up Docker Swarm and labels worker nodes.
- `configuration.yml`: Configures the environment, installs dependencies, and sets up Docker and Pulsar.
- `teardown.yml`: Cleans up the project environment.

## Requirements

The project uses the following Python dependencies:
- `DateTime`
- `pulsar`
- `pulsar-client`
- `requests`
- `urllib3`
- `ray`
- `docker`

These are listed in the `requirements.txt` file.

## How to Run

1. **Setup Environment**:
   - Ensure Docker and Pulsar are installed and configured.
   - Set the `GITHUB_TOKEN` environment variable with a valid GitHub token.

2. **Build and Deploy**:
   - Use the `docker-compose.yaml` file to build and deploy the services:
     ```sh
     docker-compose up --build
     ```

3. **Fetch and Process Data**:
   - VM1 fetches repositories and sends them to Pulsar.
   - VM2 and VM3 consume the data and perform analyses.

4. **Teardown**:
   - Use the `teardown.yml` file to clean up the environment:
     ```sh
     ansible-playbook teardown.yml
     ```

## Results

The project outputs:
- The top 10 most popular languages in repositories with unit tests and CI/CD configurations.
- The top 10 repositories with the highest number of commits.

## Notes

- Ensure the GitHub token has sufficient permissions to access the API.
- The project uses Ray for distributed processing, which requires a cluster setup.