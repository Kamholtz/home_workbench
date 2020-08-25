import sqlalchemy as db


class LoggingDatabase:
    # replace the user, password, hostname and database according to your configuration according to your information
    engine = db.create_engine(
        "postgresql://read_write:simplepass1098@localhost:5432/logging"
    )

    def __init__(self):
        self.connection = self.engine.connect()
        print("DB Instance created")

    def fetchByQuery(self, query):
        fetchQuery = self.connection.execute(f"SELECT * FROM {query}")

        query_data = fetchQuery.fetchall()

        for data in query_data:
            print(data)

        return query_data


if __name__ == "__main__":
    db = LoggingDatabase()
    results = db.fetchByQuery("public.measurements")
    print(results)
