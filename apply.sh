
ssh tv << 'EOF'
export SWAYSOCK=$(find /run/user/1000/ -name "sway-ipc.1000*.sock" -print -quit)
swaymsg reload
systemctl --user daemon-reload
systemctl --user restart dunst.service
EOF

ssh tv -t "sudo systemctl link /home/tv/.config/systemd/system/after-suspend.service; sudo systemctl daemon-reload; sudo systemctl enable after-suspend"