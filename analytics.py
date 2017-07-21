import psycopg2

# top three articles
def top_three_articles():
  conn = psycopg2.connect("dbname=news user=postgres")

  curr = conn.cursor()

  curr.execute("SELECT * FROM articles")

  print(curr.fetchall())
  print("hello")
  curr.close()
  conn.close()

  return

# popular authors
def top_authors():
  return

# days with more than 1% of errors
def error_days():
  return
