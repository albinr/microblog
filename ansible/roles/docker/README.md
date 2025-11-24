# Docker Role

This Ansible role installs Docker CE (Community Edition) on Ubuntu systems.

## Requirements

- Ubuntu-based system
- Ansible 2.9+
- Root/sudo access on target machines

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# List of users to add to the docker group
docker_users: []

# Docker service configuration
docker_service_enabled: true
docker_service_state: started

# Docker package versions (set to 'present' for latest)
docker_ce_version: present
docker_ce_cli_version: present
containerd_version: present
docker_compose_plugin_version: present

# Repository configuration
docker_apt_repository: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
docker_apt_key_url: https://download.docker.com/linux/ubuntu/gpg

# Package cache update interval in seconds
apt_cache_valid_time: 3600
```

## Example Playbook

### Basic Installation

```yaml
- hosts: servers
  roles:
    - docker
```

### Custom Configuration

```yaml
- hosts: servers
  vars:
    docker_users:
      - ubuntu
      - deploy
    docker_service_enabled: true
    docker_service_state: started
  roles:
    - docker
```

### Install Specific Versions

```yaml
- hosts: servers
  vars:
    docker_ce_version: "5:20.10.21~3-0~ubuntu-jammy"
    docker_ce_cli_version: "5:20.10.21~3-0~ubuntu-jammy"
    containerd_version: "1.6.6-1"
    docker_compose_plugin_version: "2.6.0~ubuntu-jammy"
  roles:
    - docker
```

## What This Role Does

1. Updates apt package cache
2. Installs required packages for Docker repository
3. Adds Docker's official GPG key
4. Adds Docker repository to apt sources
5. Installs Docker CE, CLI, containerd, and Docker Compose plugin
6. Starts and enables Docker service
7. Optionally adds specified users to the docker group
8. Verifies the installation

## Handlers

The role includes the following handlers:

- `restart docker` - Restarts the Docker service
- `start docker` - Starts the Docker service
- `stop docker` - Stops the Docker service
- `reload docker` - Reloads the Docker daemon configuration
