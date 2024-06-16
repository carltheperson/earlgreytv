ui.use_activity_cursor = true
touch stuff

gsettings set org.gnome.desktop.interface cursor-size 64

cp gtksettings.ini ~/.config/gtk-3.0/settings.ini

{
  "www.youtube.com": "(location.pathname.includes(`feed/history`) || location.pathname.includes(`/mail/u`)) && (location.href = `https://google.com`)",
  "youtube.com": "(location.pathname.includes(`feed/history`) || location.pathname.includes(`/mail/u`)) && (location.href = `https://google.com`)",
  "mail.google.com": "(location.pathname.includes(`feed/history`) || location.pathname.includes(`/mail/u`)) && (location.href = `https://google.com`)"
}

(location.pathname.includes(`feed/history`) || location.pathname.includes(`/mail/u`)) && (location.href = `https://google.com`)

wtype
xdotool

export SWAYSOCK="$(ls /run/user/1000/sway-ipc.1000.1816.sock | head -n 1)"
export SWAYSOCK="$(ls "$(find /run/user/1000/ -name "sway-ipc.1000*.sock" 2> /dev/null)" | head -n 1)"


https://github.com/ReimuNotMoe/ydotool/issues/25#issuecomment-535842993
sudo usermod -aG input tv
echo -e "KERNEL==\"uinput\", GROUP=\"users\", MODE=\"0660\", OPTIONS+=\"static_node=uinput\"" | sudo tee /etc/udev/rules.d/80-uinput.rules > /dev/null



udo apt install rsync