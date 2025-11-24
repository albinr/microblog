# Deploy App Docker Role

This Ansible role deploys the microblog application using Docker containers on app servers.

## Requirements

- Docker installed on target machines (use the `docker` role first)
- Access to Docker Hub to pull images
- Target machines should be part of the `appserver` group

## Role Variables

Available variables with their default values (see `defaults/main.yml`):

```yaml
# Docker image configuration
app_docker_image: albinr/microblog
app_docker_tag: latest

# Container configuration
app_container_name: microblog-app
app_host_port: 8000
app_container_port: 5000

# Application run command
app_run_command: prod

# Container restart policy
app_restart_policy: always
```

## Dependencies

- `docker` role (for Docker CE installation)

## Example Playbook

### Basic Usage

```yaml
- hosts: appserver
  remote_user: "deploy"
  become: yes
  roles:
    - docker
    - deploy_app_docker
```

### Custom Configuration

```yaml
- hosts: appserver
  remote_user: "deploy"
  become: yes
  vars:
    app_docker_tag: "v1.2.3"
    app_host_port: 9000
    app_container_name: "my-microblog"
  roles:
    - docker
    - deploy_app_docker
```

## What This Role Does

1. Pulls the specified Docker image from Docker Hub
2. Stops and removes any existing container with the same name
3. Runs a new container with proper port mapping
4. Waits for the application to start
5. Verifies the container is running successfully

## Usage

Run the playbook:
```bash
ansible-playbook -i hosts deploy_app.yml
```

The application will be available on port 8000 (or your configured `app_host_port`) on each app server.
