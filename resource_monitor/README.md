## Nest Resource Monitor

A monitor to view your live usage of CPU, memory, and storage. Features very nice graphs :D.

<<<<<<< Updated upstream
View a functional demo here on [replit](https://replit.com/@CoolDude9000/Nest-Website), or on Nest on [my website](https://monitor.felixgao.hackclub.app)!

![image](https://github.com/user-attachments/assets/009cdd46-7d6b-4614-a8aa-025321479dcd)

![image](https://github.com/user-attachments/assets/a2dba072-0742-4fc0-a5d9-1f814d9d5330)

## How to use

Sit back, relax, and watch Nest implode (/hj)! You can view global usage, aka the important bit, or if you feel _extra nosy_ you can see how my usages compare.

\*disclaimer: the cpu graph for my usage is based on a count of usages by pid, it doesn't appear to be very accurate and can spike above global sometimes. I promise I'm not nuking Nest!

## How to host it yourself

1. Add everything in `resource_monitor/` into Nest.
2. Run `nest get_port` to obtain a port on Nest.
3. Make sure to [install redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/) and that the server is running at `localhost:6379`.
4. Run the flask app on that port and setup `systemd` to keep the flask app running.
5. Install [caddy](https://caddyserver.com/docs/install), open your `Caddyfile` and setup a reverse proxy to the port.
6. Go onto the site and watch your very own resources implode!

```
www.example.com {
  reverse_proxy :1000 # Example port
}
```

=======

## TODO:

### My stuff:

- [x] Show mem usage & limit
- [x] Show CPU usage
- [x] Show storage usage & limit

### More nest related:

- [x] Show global utlization
- [ ] Stashed changes
