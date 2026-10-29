if [ "$(id -u)" -ne 0 ]; then
    echo "Not running as root. Rerunning with sudo..."
    exec sudo "$0" "$@"
fi

apt update -y
apt install at ffmpeg git -y
service atd start
mkdir -p /opt
cd /opt
git clone https://github.com/VoipDaily
cd VoipDaily

chmod a+rx schedule-wakeup.py
rm /usr/local/sbin/schedule-wakeup
ln -s schedule-wakeup.py /usr/local/sbin/schedule-wakeup

if grep -q "\[wakeup-call\]" /etc/asterisk/extensions_custom.conf; then
    echo "Dialplan found!"
else
    cat dialplan >> /etc/asterisk/extensions_custom.conf
fi

curl -L https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx?download=true -o /opt/VoipDaily/en_US-amy-medium.onnx
curl -L https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json?download=true -o /opt/VoipDaily/en_US-amy-medium.onnx.json

python3 -m venv .
source bin/activate
pip install -r requirements.txt
