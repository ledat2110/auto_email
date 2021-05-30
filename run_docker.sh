sudo docker run -dit --name auto_email ledat2110/auto_email:latest
sudo docker cp ./template_email.json auto_email:/app
sudo docker cp ./customers.csv auto_email:/app
sudo docker exec auto_email python send_email.py
sudo docker cp auto_email:/app/output_emails ./
sudo docker cp auto_email:/app/errors.csv ./
