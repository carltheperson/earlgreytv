
ssh tv << 'EOF'
export SWAYSOCK=$(find /run/user/1000/ -name "sway-ipc.1000*.sock" -print -quit)
swaymsg reload
systemctl --user daemon-reload
systemctl --user enable dunst.service casting.service
systemctl --user restart dunst.service casting.service
EOF

ssh tv -t "su -c 'systemctl link /home/tv/.config/systemd/system/after-suspend.service; systemctl daemon-reload; systemctl enable after-suspend'"