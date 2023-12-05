from dotenv import load_dotenv,dotenv_values
import os


dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)
env_vars=dotenv_values(dotenv_path)
# redis_host = os.getenv("redis_host")
# redis_port = int(os.getenv("redis_port"))
# redis_db = int(os.getenv("redis_db"))
# redis_socket_timeout = int(os.getenv("redis_socket_timeout"))
#
# hostname = os.getenv("hostname")
# db_name = os.getenv("db_name")
# username = os.getenv("username")
# password = os.getenv("password")
# db_port = os.getenv("db_port")
# basket_db = os.getenv("basket_db")
# basket_user = os.getenv("basket_user")
# basket_pass = os.getenv("basket_pass")
# shark_rds_db_name = os.getenv("shark_rds_db_name")
# shark_rds_username = os.getenv("shark_rds_username")
# shark_rds_password = os.getenv("shark_rds_password")
# shark_rds_hostname = os.getenv("shark_rds_hostname")
#
# rds_hostname = os.getenv("rds_hostname")
# rds_db_name = os.getenv("rds_db_name")
# rds_username = os.getenv("rds_username")
# rds_password = os.getenv("rds_password")
#
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# SESSION_TIME = os.getenv("SESSION_TIME")
#SESSION_TIME = os.getenv("SESSION_TIME")
redis_host = env_vars.get("redis_host")
redis_port = int(env_vars.get("redis_port"))
redis_db = int(env_vars.get("redis_db"))
redis_socket_timeout = int(env_vars.get("redis_socket_timeout"))

admin_hostname = env_vars.get("admin_hostname")
admin_password = env_vars.get("admin_password")
admin_username = env_vars.get("admin_username")
admin_db_name = env_vars.get("admin_db_name")
admin_port = env_vars.get("admin_port")
hostname = env_vars.get("hostname")
db_name = env_vars.get("db_name")
username = env_vars.get("username")
password = env_vars.get("password")
db_port = env_vars.get("db_port")
basket_db = env_vars.get("basket_db")
basket_user = env_vars.get("basket_user")
basket_pass = env_vars.get("basket_pass")
shark_rds_db_name = env_vars.get("shark_rds_db_name")
shark_rds_username = env_vars.get("shark_rds_username")
shark_rds_password = env_vars.get("shark_rds_password")
shark_rds_hostname = env_vars.get("shark_rds_hostname")

rds_hostname = env_vars.get("rds_hostname")
rds_db_name = env_vars.get("rds_db_name")
rds_username = env_vars.get("rds_username")
rds_password = env_vars.get("rds_password")

EMAIL_HOST_USER = env_vars.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env_vars.get('EMAIL_HOST_PASSWORD')
SESSION_TIME = env_vars.get("SESSION_TIME")
BACKEND_LINK = os.getenv('BACKEND_LINK')