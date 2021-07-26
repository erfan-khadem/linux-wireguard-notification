#!/usr/bin/python3

import sys
import subprocess

from gi.repository import Notify, GdkPixbuf, GLib


def handle_down(notif, action_name, data) -> None:
    code = subprocess.call("/home/erfan/utils/wg_info down", shell=True)
    if code == 0:
        msg = Notify.Notification.new("wireguard disconnected",
                                      "",
                                      ""
                                      )
    else:
        msg = Notify.Notification.new("wireguard not disconnected",
                                      "Could not disconnect wireguard",
                                      ""
                                      )
    msg.set_timeout(5)
    msg.set_image_from_pixbuf(data)
    msg.show()

def handle_up(notif, action_name, data) -> None:
    code = subprocess.call("/home/erfan/utils/wg_info up", shell=True)
    if code == 0:
        msg = Notify.Notification.new("wireguard connected",
                                      "",
                                      ""
                                      )
    else:
        msg = Notify.Notification.new("wireguard not connected",
                                      "Could not connect wireguard",
                                      ""
                                      )
    msg.set_timeout(5)
    msg.set_image_from_pixbuf(data)
    msg.show()


def main() -> None:

    Notify.init("python wg_info")
    image = GdkPixbuf.Pixbuf.new_from_file("/home/erfan/utils/assets/wireguard.png")

    if len(sys.argv) == 2 and sys.argv[1] == "down":
        handle_down(None, None, image)
        exit(0)
    elif len(sys.argv) == 2 and sys.argv[1] == "up":
        handle_up(None, None, image)
        exit(0)

    try:
        rx, tx = map(
                int,
                subprocess.check_output("/home/erfan/utils/wg_info transfer", shell=True).split()
                )
    except:
        rx, tx = 0, 0

    rx = round(rx / (1024 * 1024), 1)
    tx = round(tx / (1024 * 1024), 1)

    msg = Notify.Notification.new("wireguard transfer",
            "received: {:,}MB   |   sent: {:,}MB".format(rx, tx),
            ""
            )

    msg.set_image_from_pixbuf(image)

    msg.add_action(
                "disconnect",
                "disconnect",
                handle_down,
                image
            )

    msg.add_action(
                "connect",
                "connect",
                handle_up,
                image
            )


    msg.set_timeout(20)
    msg.show()

    GLib.timeout_add_seconds(20, exit)
    GLib.MainLoop().run()


if __name__ == "__main__":
    main()
