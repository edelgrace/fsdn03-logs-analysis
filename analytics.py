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
                SELECT date_trunc('day', time) as day, count(*) as num FROM log
                WHERE STATUS != '200 OK'
                GROUP BY day),
              max_error AS (
                SELECT day, num as total FROM error_counts
                ORDER BY num DESC
                LIMIT 1),
              sum_count AS (
                SELECT COUNT(*) as summed
                FROM log
                WHERE status != '200 OK')
              SELECT max_error.day, max_error.total, sum_count.summed,  (max_error.total / sum_count.summed)
              FROM error_counts, max_error, sum_count
              '''

  curr.execute(query_avg)

  results = curr.fetchall()

  for result in results:
    print(result)

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
