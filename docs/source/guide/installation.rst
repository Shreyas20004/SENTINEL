.. _guide-installation:

============
Installation
============

Advanced installation options and environment setup.

System Requirements
====================

**Operating System:**
 - Linux (Ubuntu 20.04+, CentOS 8+, Debian 11+) - Recommended
 - macOS 12+ (Intel or Apple Silicon)
 - Windows 10/11 with WSL2

**Minimum Hardware:**

.. list-table::
   :widths: 20 20
   :header-rows: 1

   * - Component
     - Minimum
   * - CPU Cores
     - 4
   * - RAM
     - 8GB
   * - SSD Storage
     - 50GB
   * - Network
     - 1Gbps

**Recommended Hardware (for 10+ cameras):**

.. list-table::
   :widths: 20 20
   :header-rows: 1

   * - Component
     - Recommended
   * - CPU Cores
     - 8-16 (Intel Xeon / AMD EPYC)
   * - RAM
     - 32-64GB
   * - SSD Storage
     - 500GB-1TB (NVMe)
   * - GPU
     - NVIDIA T4 / A100
   * - Network
     - 10Gbps

**Software Dependencies:**

- Docker 20.10+ 
- Docker Compose 2.0+
- Python 3.11+ (for backend development)
- Node.js 20+ (for frontend development)
- Git 2.30+

Install Dependencies (Ubuntu)
==============================

.. code-block:: bash

   # Update package manager
   sudo apt-get update

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER

   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose

   # Install Git
   sudo apt-get install -y git

   # Verify installations
   docker --version
   docker-compose --version
   git --version

Install Dependencies (macOS)
=============================

.. code-block:: bash

   # Using Homebrew
   brew install docker
   brew install docker-compose
   brew install git

   # Start Docker daemon
   open -a Docker

   # Verify
   docker --version
   docker-compose --version

Install Dependencies (Windows 10/11)
=====================================

#. Install `Docker Desktop for Windows <https://www.docker.com/products/docker-desktop>`_
#. Enable WSL2 in Windows Features (Control Panel → Programs → Turn Windows Features On/Off)
#. Download and install `Git for Windows <https://git-scm.com/downloads>`_
#. Open PowerShell and verify:

.. code-block:: powershell

   docker --version
   git --version

Production Installation
=========================

**Using Docker Compose (Recommended for phases 1-3):**

.. code-block:: bash

   # Clone repository
   git clone https://github.com/your-org/sentinel.git
   cd sentinel

   # Create environment file
   cp .env.example .env

   # Edit .env with production settings
   nano .env

   # Start services
   docker-compose -f docker-compose.prod.yml up -d

   # Verify
   docker-compose ps

**Using Kubernetes (Phase 4):**

.. code-block:: bash

   # Install Helm
   curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

   # Add SENTINEL Helm chart repo
   helm repo add sentinel https://charts.sentinel-project.org
   helm repo update

   # Install
   helm install sentinel sentinel/sentinel \
     --namespace sentinel \
     --create-namespace \
     -f values.yaml

GPU Setup (Optional)
====================

**For NVIDIA GPU acceleration:**

#. Install NVIDIA Driver:

.. code-block:: bash

   ubuntu-drivers autoinstall

#. Verify installation:

.. code-block:: bash

   nvidia-smi

   # Expected output: GPU info, CUDA version

#. Install NVIDIA Container Toolkit:

.. code-block:: bash

   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
     sudo tee /etc/apt/sources.list.d/nvidia-docker.list

   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker

#. Update Docker Compose to use GPU:

Edit ``docker-compose.yml``:

.. code-block:: yaml

   services:
     backend:
       runtime: nvidia
       environment:
         - NVIDIA_VISIBLE_DEVICES=all
         - GPU_ENABLED=true

#. Restart services:

.. code-block:: bash

   docker-compose down
   docker-compose up -d

Health Verification
====================

.. code-block:: bash

   # Check containers running
   docker-compose ps

   # Health check API
   curl http://localhost:8000/health | jq .

   # Test database connection
   docker-compose exec postgres psql -U postgres -d sentinel -c "SELECT version();"

   # Test Redis
   docker-compose exec redis redis-cli ping

   # View logs
   docker-compose logs -f backend

Next Steps
==========

→ Continue to :ref:`guide-configuration` to set up your environment

→ See :ref:`guide-deployment` for production deployment

--------

**Last Updated:** March 29, 2026
