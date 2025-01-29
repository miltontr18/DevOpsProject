from flask import Flask
import pymysql



schema_name = "mydb"

# Establishing a connection to DB
conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', passwd='password', db=schema_name)
conn.autocommit(True)

app = Flask(__name__)

@app.route('/users/get_user_data/<user_id>')  # This route remains for HTML display
def get_user_data_html(user_id):
    cursor = conn.cursor()
    db_user = "SELECT user_name FROM users WHERE user_id = %s"
    cursor.execute(db_user, (user_id,))
    result = cursor.fetchone()

    if result:
        user_name = result[0]
        return f"<H1 id='user'>{user_name}</H1>"
    else:
        return "<H1 id='user'>User not found</H1>"  # More informative message

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

