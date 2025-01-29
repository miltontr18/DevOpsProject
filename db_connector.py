import pymysql

schema_name = "mydb"

# Establishing a connection to DB
conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', passwd='password', db=schema_name)
conn.autocommit(True)

# Getting a cursor from Database
cursor = conn.cursor()
# Inserting data into table

# # Table with created_date as VARCHAR(50)
# statementToExecute = "CREATE TABLE `" + schema_name + "`.`users2`(`user_id` INT NOT NULL , `user_name` VARCHAR(50) NOT NULL, `date_created` VARCHAR(50) , PRIMARY KEY (`user_id`))"

# # Table with created_date as DATETIME
# statementToExecute = "CREATE TABLE `" + schema_name + "`.`users2`(`user_id` INT NOT NULL , `user_name` VARCHAR(50) NOT NULL, `date_created` DATETIME DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`user_id`))"

# # Config table for testing
# statementToExecute = f"CREATE TABLE `{schema_name}`.`config`(`id` INT NOT NULL AUTO_INCREMENT, `backend_url` VARCHAR(50) NOT NULL ,`frontend_url` VARCHAR(50) NOT NULL, `user_name` VARCHAR(50) NOT NULL,  PRIMARY KEY (`id`))"
# cursor.execute(statementToExecute)

#
# backend_url = 'http://127.0.0.1:5000/users/'
# frontend_url = 'http://127.0.0.1:5001/users/get_user_data/'
# user_name = 'Gregory'
#
# # Inserting data into table
# cursor.execute(f"INSERT into mydb.config (backend_url, frontend_url, user_name) VALUES ('{backend_url}', '{frontend_url}', '{user_name}')")
#
# cursor.close()
# conn.close()
# # #
# cursor.close()
# conn.close()
