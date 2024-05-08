# message_board
***Flask message board application***<br />
Fallow these steps to begin.<br />
```bash
sudo apt update
sudo apt install git python3 python3-pip
python3 --version
sudo pip3 install flask
```
then:<br />
```bash
git clone https://github.com/pooyanazad/message_board.git
cd message_board
python3 app.py
```
you can see message board application on your ip:443<br />
Admin can delete users or change their password, you can reach the admin page https://ip:login username is "admin" and password is "123999" (you can change it in app.py file)<br />
<br />
Also you can launch app as a container: docker pull pooyanazad/message_board:v2.2 <br />
For certificate you can use cerbot its standalone and free<br />

<br />
pooyan.azadparvar@gmail.com for any question
