# Capy.life
Capy.life is the official daily Capybara site approved by many Zoos & Scientists. 1/10 Endocrinologist say that viewing a Capybara each day drastically improves your mental state.

## Previews
### Home
![home page preview](https://i.imgur.com/2EQsfb1.png)
### Admin
![admin page preview](https://i.imgur.com/QV7Av5w.png)

## Setup
### Production with Docker
- `git clone --branch Production https://github.com/capylife/capyend`
- Configure `docker-compose.yml`
- Proxy exposed ports using Nginx (or whatever reverse proxy you prefer.)
- `sudo docker-compose build; sudo docker-compose up -d`

#### Using Rclone
[Using rclone with Docker Compose](https://rclone.org/docker/#getting-started)

Basically the most important part is to install `fuse`, create `/var/lib/docker-plugins/rclone/config` & `/var/lib/docker-plugins/rclone/cache`, install the docker plugin `docker plugin install rclone/docker-volume-rclone:amd64 args="-v" --alias rclone --grant-all-permissions`, configure the `rclone.conf` for the storage service you want to use & then configure your docker compose to use the rclone volume. [Example rclone docker compose](/rclone-docker-example.yml).
