if [ "$(id -u)" -ne 0 ]; then
    echo "Not running as root. Rerunning with sudo..."
    exec sudo "$0" "$@"
fi

apt update -y
apt install at ffmpeg git -y
mkdir -p /opt
cd /opt
git clone https://
service atd start