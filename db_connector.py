import pymysql

# # Creating a Table with created_date as VARCHAR(50)
# statementToExecute = "CREATE TABLE `" + schema_name + "`.`users2`(`user_id` INT NOT NULL , `user_name` VARCHAR(50) NOT NULL, `date_created` VARCHAR(50) , PRIMARY KEY (`user_id`))"

# # Creating a Table with created_date as DATETIME
# statementToExecute = "CREATE TABLE `" + schema_name + "`.`users2`(`user_id` INT NOT NULL , `user_name` VARCHAR(50) NOT NULL, `date_created` DATETIME DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`user_id`))"

# # Creating a Config table for testing
# statementToExecute = f"CREATE TABLE `{schema_name}`.`config`(`id` INT NOT NULL AUTO_INCREMENT, `backend_url` VARCHAR(50) NOT NULL ,`frontend_url` VARCHAR(50) NOT NULL, `user_name` VARCHAR(50) NOT NULL,  PRIMARY KEY (`id`))"
# cursor.execute(statementToExecute)

# cursor.close()
# conn.close()



def mysql_users():
    schema_name = 'mydb'
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='user',
            passwd='password',
            db= schema_name  # Hardcoded database name here
        )
        conn.autocommit(True)
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

if __name__ == "__main__":  # Important for reusability!
    conn = mysql_users()


