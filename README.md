# Kync - SSH Key Synchronization and Access Control

Welcome to Kync, a straightforward and flexible tool designed to simplify the management of authorized SSH keys across
multiple  servers and enhance the security of your projects. Kync is your go-to solution for keeping your servers and
project access synchronized effortlessly.

Obviously, Kync stands for `Key sYNC`...

## Key Features

### 1. Keep SSH Keys in Sync

Kync offers seamless synchronization of authorized SSH keys across all your configured servers. No more manual key
updates, ensuring that your authorized keys are always up-to-date and secure.

### 2. Team Member Management

Register team members and associate their public keys with ease. You can effortlessly assign team members to specific
projects, streamlining access control and improving collaboration.

### 3. Group Management

Kync allows you to create groups of team members and attach these groups to projects. Managing access for various teams
within your projects has never been more straightforward.

### 4. Multiple Environments

Projects often require different environments or servers. Kync supports the management of multiple environments for a
single project, ensuring that your keys are synchronized across various server configurations.

### 5. Automated Synchronization

Kync is designed to work in the background, synchronizing keys both on save and daily. This means you can focus on your
work while Kync takes care of access control and key management.

## Getting Started

To setup and start using Kync, do the following:

1. Copy the `.env.example` file to `.env`
2. Copy the `docker-compose.example.yml` file to `docker-compose.yml`
3. Run `docker-compose up -d`
4. **IMPORTANT**: go to `http://<your host>/custom_auth/user/1/password/` and change the password
   - The default credentials are `admin@smf.ai:admin`

## Contribute

Kync is an open-source project, and we welcome contributions from the community. Whether you want to report issues,
suggest improvements, or contribute code, your input is valuable in making Kync an even more robust tool for SSH key
management.

### Local setup for development

Prerequisites: docker, docker-compose, pipenv

For the very first setup, do the following:

1. Install the python dependencies: `pipenv install --dev`
2. Install the pre-commit hooks: `pipenv run pre-commit install`
3. Run `docker-compose -f docker-compose.dev.yml up --build -d db redis backend`
4. Run the migrations `docker-compose -f docker-compose.dev.yml exec backend ./manage.py migrate`
5. Run the remaining services `docker-compose -f docker-compose.dev.yml up -d`

For further startups, you can just do the following:

1. Run all the services: `docker-compose -f docker-compose.dev.yml up -d`
2. If there are some migrations, run them: `docker-compose -f docker-compose.dev.yml exec backend ./manage.py migrate`

## Support

If you encounter any problems or have questions while using Kync, please don't hesitate to open an issue. Try to be
descriptive as much as possible (of course obfuscate any security related data in your message).

We hope Kync simplifies your SSH key management, enhances security, and streamlines your project collaboration. Thank
you for choosing Kync!
