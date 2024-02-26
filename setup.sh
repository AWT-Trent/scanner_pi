echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
sudo echo "libcomposite" | sudo tee -a /etc/modules
cp ./scanner_pi_usb /usr/bin/scanner_pi_usb
cp ./scanner_flask.py /usr/bin/scanner_flask.py
sudo chmod +x /usr/bin/scanner_pi_usb
sed -i -e '$i \n/usr/bin/scanner_pi_usb # libcomposite configuration\n' rc.local
sed -i -e '$i \npython /usr/bin/scanner_flask.py\n' rc.local
apt-get install pip git
pip install flask
reboot