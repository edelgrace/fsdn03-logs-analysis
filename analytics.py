import psycopg2

# top three articles
def top_three_articles():
  conn = psycopg2.connect("dbname=news user=postgres")

  curr = conn.cursor()

  # reference: https://stackoverflow.com/questions/15378216/postgresql-contains-in-where-clause 
  query = '''SELECT articles.title, count(*) as num FROM log, articles
             WHERE log.path = '/article/' || articles.slug 
                 AND log.status = '200 OK'
             GROUP BY articles.title 
             ORDER BY num DESC LIMIT 3;'''

  curr.execute(query)

  results = curr.fetchall()

  for result in results:
    title = result[0] 
    views = str(result[1])

    print(title + " (" + views + " views)")

  curr.close()
  conn.close()

  return

# popular authors
def top_authors():
  conn = psycopg2.connect("dbname=news user=postgres")

  curr = conn.cursor()

  # reference: https://stackoverflow.com/questions/15378216/postgresql-contains-in-where-clause 
  query = '''SELECT authors.name, count(*) as num FROM log, articles, authors
             WHERE log.path = '/article/' || articles.slug 
                 AND authors.id = articles.author
                 AND log.status = '200 OK'
             GROUP BY authors.name 
             ORDER BY num DESC LIMIT 3;'''

  curr.execute(query)

  results = curr.fetchall()

  for result in results:
    title = result[0] 
    views = str(result[1])

    print(title + " (" + views + " views)")

  curr.close()
  conn.close()

  return

# days with more than 1% of errors
def error_days():
  conn = psycopg2.connect("dbname=news user=postgres")

  curr = conn.cursor()

  # reference: https://stackoverflow.com/questions/15378216/postgresql-contains-in-where-clause 
  query_avg = '''
              WITH error_counts AS (
                SELECT date_trunc('day', time) as day, 
                  CAST(COUNT(*) AS FLOAT) as num
                FROM log
                WHERE STATUS != '200 OK'
                GROUP BY day),
              total_counts AS (
                SELECT date_trunc('day', time) AS day,
                   CAST(COUNT(*) AS FLOAT) AS total_num
                FROM log
                GROUP BY day)
              SELECT 
                to_char(total_counts.day, 'Month DD YYYY') AS day,
                (error_counts.num / total_counts.total_num * 100) as percent
              FROM total_counts, error_counts
              WHERE error_counts.day = total_counts.day
              ORDER BY percent DESC
              LIMIT 1;
              '''

  curr.execute(query_avg)

  results = curr.fetchall()

  for result in results:
    date = result[0].replace("     ", "")
    percent = result[1]
    print(date + " (" + str(percent) + "% errors)")

  curr.close()
  conn.close()

  return


print("Top Three Articles")
print("------------------")

top_three_articles()


print("\nTop Authors")
print("-----------")

top_authors()

print("\nDays With >1% Errors")
print("--------------------")
error_days()
