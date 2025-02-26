<h1 align="center">EarlGreyTV</h1>
<p align="center">This repository explains how I run my smart TV setup EarlGreyTV.</p>

<div align="center">
		<img alt="TV" src="images/front.png">
</div>

<br/>

> [!TIP]
> I wrote a [blog post](https://carltheperson.com/posts/earlgreytv) about this too. And recorded a quick [YouTube video](https://www.youtube.com/watch?v=836VlTPxnFc).

Summary: I use a Linux-running laptop (which I spilled tea on) to render a browser in constant fullscreen. I then have a homepage with a smart TV-like look. The "apps" are simply links to websites.

Warning: This is mostly a collection of my notes. I haven't tested if these steps work perfectly on a fresh install. You should be able to debug things yourself if anything goes wrong.

I encourage you to customize this as much as possible. Please make it *your* perfect setup, not mine.


# Configuring and Running Locally

The main "homepage" of EarlGreyTV is the `earlgreytv.html` file found in `config_files/home/tv/earlgreytv/`. This is where you tweak the homepage appearance and, importantly, configure the "apps".

In this repo, I have my own example with my apps. Maybe I'm paranoid, but I'm too scared of copyright to have logo files hosted here. I made this script so you can download them yourself:

```sh
# Download the logos in the logos.txt file
# E.g Netflix logo
./download_logos.sh
```

Now you should be able to open the HTML file in a browser. e.g.:

```
firefox config_files/home/tv/earlgreytv/earlgreytv.html
```

## Adding Your Own Apps

The apps are defined in the JavaScript portion of the `earlgreytv.html` file. Specify your app name, URL, and logo (which should exist in the `images/` folder).

```js
const APPS = [
  { name: "App name", url: "https://example.org", image: "app.png" },
  /* ... */
]
```
Tip: You can add a shortcut icon in the top-right corner by specifying `shortcut: true`.

# Hardware Setup Notes

## TV

Get yourself something you can use as a screen for your setup. Ideally, it should be as dumb as possible - simply showing the output of the computer you plug into it.

I couldn't find a dumb TV, so I got a smart TV and used settings to dumb it down a bit.

I got a `SAMSUNG 55" 4K UHD LED TV TU55CU7105KXXC` (3840x2160), and connected it with HDMI.

I did this setting change:

- \> All Settings
- \> General & Privacy
- \> Start Screen Options
- "Autorun Last App"

My HDMI connection is considered an "App".

Side note: Some TVs have hidden menus that can allow you to dumb them down even more, [example](https://youtu.be/LGngUs30dh0). The regular settings seemed to work okay for me, though.

## Computer

You need a computer to power your setup. An old used laptop is perfect.

I used a 5-year-old Lenovo laptop with a broken keyboard (because I spilled Earl Grey tea into it).

![Back of TV with computer](images/back.png)

## Remote

Since this setup is a regular desktop setup disguised as a smart TV, you need something to be your mouse. You also need a keyboard too (although maybe you can trigger an on-screen keyboard).

I chose the `WECHIP W3 2.4G 3-i-1 2.4G Air Mouse`. It uses a small gyroscope as input for the mouse and has a small keyboard on the back. It's good but a bit flimsy.

![Remote front and back](images/remote.png)

## Optional Extras

### HDMI USB CEC Adapter

I use [CEC](https://en.wikipedia.org/wiki/Consumer_Electronics_Control) to allow my computer to suspend my TV. I need an adapter because the laptop doesn't support the CEC protocol itself.

I use the `Pulse Eight USB-CEC Adapter`.

![CEC adapter](images/cec.png)

### USB Extender

For your mouse, you'll likely get a very small USB receiver, [example](https://upload.wikimedia.org/wikipedia/commons/7/7d/Logitech_unifying_receiver.jpg). Depending on where you place your laptop, you might need to extend the receiver.

I use a generic USB extender, [example](https://commons.wikimedia.org/wiki/File:USB_extender_cable.jpg).

# Software Setup Notes

## Operating System

I went with [Debian Linux](https://www.debian.org/). I named my user `tv`.

## Desktop Environment

I chose [Sway](https://swaywm.org/). I needed something I could easily configure with a config file and that would be highly minimal.

In retrospect, maybe regular [i3](https://i3wm.org/) would have been better. The automation tools that exist for the [X Window System](https://en.wikipedia.org/wiki/X_Window_System) are more documented.

Run:

```sh
sudo apt install sway -y
```

Then log out of GNOME and log into Sway.

## Packages

These are the packages I could gather from my notes. There may be a couple I forgot, and some that are not needed.

```Sh
sudo apt install rsync pulseaudio pulseaudio-utils playerctl pamixer xdotool ydotool input-util xbindkeys wtype udev cec-utils -y
```

## SSH notes

The next steps depend on an SSH connection to your TV. I recommend adding your TV computer to your `~/.ssh/config`. This is how I connect to my TV:

```sh
ssh tv
```

**Tip: Sway Commands Over SSH:**

Interacting with Sway over SSH might give you an error like this: `swaymsg/main.c:419] Unable to retrieve socket path`.

This is my fix:

```sh
export SWAYSOCK=$(find /run/user/1000/ -name "sway-ipc.1000*.sock" -print -quit)
# Now you should be able to e.g. reload Sway:
swaymsg reload
```

## Firefox Manual Settings

### Set Zoom

You likely need some extra zoom on the website you visit. How much depends on how big your screen is. 200% looks good on my TV.

Navigate to `about:preferences`.

Set "Default zoom" to 200%.

![Zoom](images/zoom.png)

### Create Profile

The profile is used for a predictable path to place a config file.

Navigate to `about:profiles`.

Make sure to click "Choose Folder..." and set it to `/home/tv/.mozilla/firefox/earlgreytv`.

![profile wizard](images/profile_wizard.png)

"Default Profile" should be set to "Yes"

### Set Homepage

Navigate to `about:preferences#home`.

For the homepage, pick "Custom URLs...". Then set it to `file:///home/tv/earlgreytv/earlgreytv.html`.

![home page settings](images/homepage.png)

### Enable Stylesheets

Navigate to `about:config`, and set `toolkit.legacyUserProfileCustomizations.stylesheets` to `true`.

![stylesheets option](images/stylesheets.png)

### Enable Activity Cursor

This will indicate on the cursor if the page is loading.

Navigate to `about:config`, and set `ui.use_activity_cursor` to `true`.

![activity cursor](images/activity_cursor.png)


## Sync Configs

Run `./sync.sh` in this directory, to sync files needed for the EarlgreyTV setup.

```sh
# Make sure you have rsync
sudo apt install rsync -y
# Sync files 
./sync.sh
```

## Apply Configs

Run `./apply.sh` to restart any services that use config files. It doesn't restart Firefox.

```sh
./apply.sh
```

## Casting via iPhone Shortcut

EarlGreyTV implements a very simple casting mechanism. A server will receive a URL from an HTTP request, and paste it into the Firefox address bar. The script for the casting server can be found here: `config_files/home/tv/casting_server.py`.

To make calls to the casting server easily from my iPhone, I created a shortcut that shows up in the Sharing Sheet when sharing a link from any app.

If you want to recreate the shortcut yourself, you can refer to these screenshots:

![Casting shortcut](images/casting.png)


## Further Notes

- I ran into some issues with `ydotool`. This [solution](https://github.com/ReimuNotMoe/ydotool/issues/25#issuecomment-535842993) helped.
- Your TV screen might not be primary on the initial Debian login screen. [This](https://askubuntu.com/a/1467005) can correct that.

# Thanks To

- Cup drawing logo: [BorogoveLM](https://www.deviantart.com/borogovelm/gallery), https://www.deviantart.com/borogovelm/art/Not-My-Cup-Of-Tea-297646401
- Background drawing: [Rebecca](https://krita-artists.org/u/rebecca/summary), https://krita-artists.org/t/drawing-with-water-soluble-ink/3069
- Web SVG icon by HASTA ICON from <a href="https://thenounproject.com/browse/icons/term/web/" target="_blank" title="web Icons">Noun Project</a> (CC BY 3.0)
- Folder SVG icon by Waldiz Production from <a href="https://thenounproject.com/browse/icons/term/folder/" target="_blank" title="Folder Icons">Noun Project</a> (CC BY 3.0) 
- Document SVG icon by Adiyogi from <a href="https://thenounproject.com/browse/icons/term/document/" target="_blank" title="Document Icons">Noun Project</a> (CC BY 3.0)
- Send/shortcut SVG icon by HideMaru from <a href="https://thenounproject.com/browse/icons/term/send/" target="_blank" title="send Icons">Noun Project</a> (CC BY 3.0)
- [Kevin Balicot](https://github.com/kevinbalicot) for making https://cataas.com (used as example "app")
- [Igor Chubin](https://github.com/chubin) for making https://wttr.in (used as example "app")

# License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details