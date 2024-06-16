ssh tv << 'EOF'
export SWAYSOCK=$(find /run/user/1000/ -name "sway-ipc.1000*.sock" -print -quit)
swaymsg reload
EOF