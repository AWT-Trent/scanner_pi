echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
sudo echo "libcomposite" | sudo tee -a /etc/modules
cp -r ../scanner_pi /usr/bin/scanner_pi
cp ./scanner_pi_usb /usr/bin/scanner_pi_usb
chmod +x /usr/bin/scanner_pi/scanner_pi_usb
sed -i -e '$i \bash /usr/bin/scanner_pi_usb # libcomposite configuration\n' /etc/rc.local
sed -i -e '$i \python /usr/bin/scanner_pi/scanner_flask.py --host $_IP\n' /etc/rc.local
apt-get install pip git -y
pip install flask
reboot