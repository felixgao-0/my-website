## Nest Resource Monitor

A monitor to view your live usage of CPU, memory, and storage. Features very nice graphs :D.

View a functional demo here on [replit](https://replit.com/@CoolDude9000/Nest-Website), or on Nest on [my website](https://monitor.felixgao.hackclub.app)! 

![image](https://github.com/user-attachments/assets/009cdd46-7d6b-4614-a8aa-025321479dcd)

![image](https://github.com/user-attachments/assets/a2dba072-0742-4fc0-a5d9-1f814d9d5330)

## How to use

Sit back, relax, and watch Nest implode (/hj)! You can view global usage, aka the important bit, or if you feel _extra nosy_ you can see how my usages compare.

*disclaimer: the cpu graph for my usage is based on a count of usages by pid, it doesn't appear to be very accurate and can spike above global sometimes. I promise I'm not nuking Nest!

## How to host it yourself

Add everything in `resource_monitor/` into Nest. Run `nest get_port` to obtain a port on Nest. Run the flask app on that port and setup systemd to keep the flask app running. Open your Caddyfile and  setup a reverse proxy to the port. Go onto the site and watch your very own resources implode!

```
www.example.com {
  reverse_proxy :1000 # Example port
}
```
