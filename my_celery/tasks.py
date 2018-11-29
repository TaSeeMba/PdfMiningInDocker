from __future__ import absolute_import
from my_celery.celery import app
import time, requests
import sqlalchemy

# credentials for cloud sql db
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_instance_name = os.environ.get("CLOUD_SQL_INSTANCE_NAME")
# connect to cloud sql instance
db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=db_user,
        password=db_pass,
        database=db_name,
        query={
            'unix_socket': '/cloudsql/{}'.format(cloud_sql_instance_name)
        }
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
)

@app.task
def mine_pdf(self, i):
    r = requests.get(i)
    # mine content from the pdf here
    
    # prepare insert statement for mined json
    insertStatement = sqlalchemy.text(
    "INSERT INTO invoices (invoice)"
    " VALUES (:minedInvoice)"
    )

    try:
    # Using a with statement ensures that the connection is always released
    # back into the pool at the end of statement (even if an error occurs)
    with db.connect() as conn:
        conn.execute(insertStatement)
    except Exception as e:
    # If something goes wrong, handle the error in this section. This might
    # involve retrying or adjusting parameters depending on the situation.
    # [START_EXCLUDE]
    logger.exception(e)
    return Response(
        status=500,
        response="Unable to successfully cast vote! Please check the "
                    "application logs for more details."
    )
