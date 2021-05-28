# Stock Notifications

   Django app for creating notifications for stocks that notifies the user with a Whatsapp message when it reached a certain percentage. It lists information about stocks with historical graph, current price, company description etc. and after registration gives access to setting up notifications.

   It includes a cloud function that can be scheduled to run at any interval - possibly each second to provide accurate results. Fuction checks if each notification reached it's notification value and if so it sends a massage using Twillio Whatsapp API. It's ready to be deployed at cloud resources like Google Fuctions or AWS Lambda. For this app to work it needs connection to a Mongo database  
   
   

####   To run this app with gunicorn in a production environment run command:  
   
   ```python
   python manage.py makemigrations && python manage.py migrate && gunicorn --worker-tmp-dir /dev/shm stockalert.wsgi. 
   ```  
   You will need these environment variables set:  
   DB_HOST - MongoDB url connection string to your database, DB_USERNAME, DB_PASSWORD and DJANGO_SECRET_KEY

---

### Sample:
<img src="https://stock-notifications-app.s3.eu-central-1.amazonaws.com/stock.png" alt="here should be a photo but there is nothing for some reason" height=200px width=320px>
